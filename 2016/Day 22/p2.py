import sys

sys.path.append('../../')

from Core import SolverCore

# This was a pretty interesting one for me. I have 2 solutions written, one generic one (that would work
# on any possible test case) and this one, which makes quite a lot of (probably correct) assumptions about
# the test cases. You can find the generic solution under p2_generic.py for this day. I will cover each
# solution in its file respectfully.
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
# - Following from the previous point, we can safely assume WLoG that the capacity means nothing and we can ignore it
#   completely. We only care whether a node is a free one (one we can move into the empty node) or a wall.
# - If we think about it, if the first 2 rows contain no walls and are reachable by the empty node, the solution becomes
#   trivial. Why is this ? This is due to the fact that the shortest path to move the wanted value into (0, 0) is always
#   going to be: the distance to reach the node on the left of the node containing the wanted value (or
#   (0, len(nodes[0]) - 2), so the second to last one from the left) however much it amounts to and the distance between
#   (0, 0) and this node multiplied by 5. The second bit is due to the fact that once we reach the left node, the most
#   optimal path is always going to be down, left, left, up, right (for the empty node). This will move the wanted value
#   one step to the left. We repeat this process len(nodes[0]) - 2 times and we'll reach (0, 0). There is an assertion
#   in this solution which makes sure this is true and it indeed was for 4 other inputs I found, which makes be believe
#   that this was the intended trick for this problem.
# From this point onward, we do a simple BFS to find the shortest path to the node left of the wanted one and then
# calculate the remainder of the steps in constant time. The reason the generic solution was also added is because I
# did not like the number of assumptions I needed to do to get this one. It will always be correct, but much, much
# slower (executes in about 9 minutes for my input).

# Feel free to change this value in case there are non-wall nodes
# that are higher than this.
WALL_BREAKPOINT = 150
class Solver(SolverCore):
    def get_neighbours(self, node, nodes):
        x, y = node
        neighbours = []
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_x, n_y = x + dx, y + dy
            if 0 <= n_x < len(nodes) and 0 <= n_y < len(nodes[0]):
                neighbour = nodes[n_x][n_y]
                
                if neighbour != '#':
                    neighbours.append((n_x, n_y))
        
        return neighbours
    def _solve(self, problem_input):
        problem_input.pop(0)
        problem_input.pop(0)
        
        nodes = []
        blank_node = ()
        
        for line in problem_input:
            name, size, used, available, use_percentage = list(filter(lambda x: len(x), line.strip().split(' ')))
            
            size, used, available, use_percentage = [int(nb[:-1]) for nb in [size, used, available, use_percentage]]
            _, index_string = name.split('-x')
            name = tuple([int(x) for x in index_string.split('-y')][::-1])
            
            if used == 0:
                blank_node = name
            x, y = name
            if len(nodes) - 1 < x:
                nodes.append('')
                
            representation = '#' if size > WALL_BREAKPOINT else '.'
            nodes[x] += representation
        
        # the one left of the actual node containing the wanted data
        end_node = (0, len(nodes[0]) - 2)
        visited = set([])

        # current_node, steps
        queue = [(blank_node, 0)]
        
        # make sure that our assumptions are correct
        assert not any([x == '#' for x in nodes[0]]) and not any([x == '#' for x in nodes[1]])
        
        while queue:
            current_node, steps = queue.pop(0)
            
            if end_node == current_node:
                return steps + 1 + (len(nodes[0]) - 2) * 5
                
            if current_node in visited:
                continue
            visited.add(current_node)
            
            for neighbour in self.get_neighbours(current_node, nodes):
                if neighbour not in visited:
                    queue.append((neighbour, steps + 1))
                    
        # no solution found, should not happen based on the assertion
        return -1


solver = Solver(7)
solver.solve()