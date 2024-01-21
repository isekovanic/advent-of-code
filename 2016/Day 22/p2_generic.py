import sys
from copy import deepcopy

sys.path.append('../../')

from Core import SolverCore

# Please have a look at the explanation in p2.py first before reading this as some of the things
# will overlap.
# Assumptions:
# - Each one of the nodes has enough memory allocated to it so that there is no case where you can consume the
#   data of a node while the previous data still exists there. This is actually heavily hinted to us by the solution
#   to the first part of this problem, where the exact result is the number of walls subtracted by the number of nodes.
#   Another hint about this is the fact that there is in fact an empty node that we can use to move around some data
#   every time and get a solution.
# - Each node can be one of two things, either a node we can go to or a wall. A node we can go to is typically
#   any node that we can freely shift towards our empty one, thus generating movement. Here's the catch though; every
#   node we can move to is interchangeable with any other one of the same kind. This means that we can load the capacity
#   of any node that is NOT a wall inside any other node that is not a wall (their size is large enough to contain it).
#   Walls are also constructed in a very obvious way (again, also hinted in the problem description) since their values
#   are 5 times larger than any other value that is not also a wall.
# Unlike the other solution which heavily relies on the input data, this one is a more generic one - actually honoring
# the rules described in the problem (despite the fact that they're meaningless).
# Here is a quick rundown of the solution as well as some of the optimizations that are done here:
# - Instead of writing a BFS that would move the empty node around until the first time the wanted data reaches node
#   (0, 0) (this is way too slow as it explodes in complexity by a couple of steps in), let's do something else. The
#   issue with that solution is the fact that the empty node can easily "drift away" in a completely counter productive
#   direction, making the number of states truly huge. In order to be able to "hint" to the empty node where we want it
#   to go, let us do the following. We will try to move the data of the top right node around to its neighbours (if
#   possible). In order to move this value, we need to move the empty node first to that new position. So, each time we
#   decide where to move the wanted data we will run an additional BFS from the location of the empty node to the new
#   location. Then, the number of steps would be whatever the BFS returns + 1 (because we need to actually move it).
# - To make sure that the number of steps is minimized, we decide on the moves for the wanted data in another flood
#   fill fashion (basically another BFS). So, we run BFS to calculate where we want the wanted data to go and run BFS
#   again to calculate how many steps the empty node needs to do. If we get stuck somewhere (for example between walls)
#   we backtrack for the wanted data and find another path. This is guaranteed to always provide a correct solution,
#   regardless of what the data looks like.

class Node:
    def __init__(self, name, size, used, available, use_percentage):
        size, used, available, use_percentage = [int(nb[:-1]) for nb in [size, used, available, use_percentage]]
        
        self.size = size
        self.used = used
        self.available = available
        self.use_percentage = use_percentage
        
        _, index_string = name.split('-x')
        self.name = tuple([int(x) for x in index_string.split('-y')][::-1])
    def __repr__(self):
        return '{{Name: {}, Used: {}, Available: {}}}'.format(self.name, self.used, self.available)

class Solver(SolverCore):
    def get_neighbours(self, node, nodes, wanted_moving = False):
        x, y = node.name
        neighbours = []
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_x, n_y = x + dx, y + dy
            if 0 <= n_x < len(nodes) and 0 <= n_y < len(nodes[0]):
                neighbour = nodes[n_x][n_y]
                
                if neighbour.used <= node.available or wanted_moving and node.used <= neighbour.size:
                    neighbours.append(neighbour)
        
        return neighbours
    
    def bfs(self, start, destination, blocked_node, nodes):
        visited = set([])
        queue = [(start, nodes, 0)]
        
        while queue:
            current_node, current_nodes, steps = queue.pop(0)
            
            if current_node.name == destination.name:
                return steps, deepcopy(current_nodes)
                
            if current_node.name in visited:
                continue
            visited.add(current_node.name)
            
            x, y = current_node.name
            
            for neighbour in self.get_neighbours(current_node, current_nodes):
                if neighbour == blocked_node or neighbour.name in visited:
                    continue
                    
                n_x, n_y = neighbour.name
                new_nodes = deepcopy(current_nodes)

                new_nodes[x][y].used = new_nodes[n_x][n_y].used
                new_nodes[x][y].available -= new_nodes[x][y].used
                new_nodes[n_x][n_y].used = 0
                new_nodes[n_x][n_y].available += new_nodes[x][y].used
                
                queue.append((new_nodes[n_x][n_y], new_nodes, steps + 1))
        
        # cannot get there, possibly blocked by or into high memory nodes
        return -1, deepcopy(nodes)
    def _solve(self, problem_input):
        problem_input.pop(0)
        problem_input.pop(0)
        
        nodes = []
        blank_node = ()
        
        for line in problem_input:
            name, size, used, available, use_percentage = list(filter(lambda x: len(x), line.strip().split(' ')))
            node = Node(name, size, used, available, use_percentage)
            if node.used == 0:
                blank_node = node
            x, y = node.name
            if len(nodes) - 1 < x:
                nodes.append([])
            nodes[x].append(node)
        
        end_node = nodes[0][0]
        visited = set([])

        # current_blank_node, wanted_data_node, nodes, steps
        queue = [(blank_node, nodes[0][len(nodes[0]) - 1], nodes, 0)]
        
        while queue:
            current_blank_node, wanted_data_node, nodes, steps = queue.pop(0)
            
            if end_node.name == wanted_data_node.name:
                return steps
                
            if wanted_data_node.name in visited:
                continue
            visited.add(wanted_data_node.name)
            
            x, y = wanted_data_node.name
            
            for neighbour in self.get_neighbours(wanted_data_node, nodes, True):
                extra_steps, new_nodes = self.bfs(current_blank_node, neighbour, wanted_data_node, nodes)
                if extra_steps != -1 and current_blank_node != neighbour and neighbour not in visited:
                    n_x, n_y = neighbour.name
                    wanted_used = new_nodes[x][y].used
                    new_nodes[n_x][n_y].used = wanted_used
                    new_nodes[n_x][n_x].available = new_nodes[n_x][n_y].size - new_nodes[n_x][n_x].used
                    new_nodes[x][y].used = 0
                    new_nodes[x][y].available = new_nodes[x][y].size - new_nodes[x][y].used
                    
                    queue.append((new_nodes[x][y], new_nodes[n_x][n_y], new_nodes, steps + extra_steps + 1))
        
        # no solution found, should not happen
        return -1


solver = Solver(7)
solver.solve()