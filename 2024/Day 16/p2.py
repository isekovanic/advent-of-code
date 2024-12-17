import sys
import heapq

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# Unfortunately, I wasn't really able to make the part 1 solution work so that I could
# salvage at least a part of it. Basically had to redo the entire thing from scratch more
# or less.
# In essence, what we do here is:
# - We run Dijkstra's, but we do not stop once we find the solution but rather continue going
# - Each solution we find we add to a backtracking set (paths) so that we can easily reconstruct
#   it later
# - Once we have all of the linked paths, we run BFS over them so that we get the actual nodes
#   and we deduplicate them for the correct answer

# clockwise
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Solver(SolverCore):
    def dijkstra(self, graph, start, end):
        sx, sy = start
        ex, ey = end
        start_node = (sx, sy, 0)
        priority_queue = [(0, start_node, (None, None, None))]
        distances = defaultdict(lambda: sys.maxsize)
        distances[start_node] = 0
        paths = defaultdict(set)
        reachable = set([])
        
        while priority_queue:
            current_distance, current_node, previous_node = heapq.heappop(priority_queue)
            cx, cy, d = current_node
            
            if current_distance > distances[current_node]:
                continue
            
            distances[current_node] = current_distance

            if (cx, cy) == end:
                if current_distance > min([distances[(ex, ey, x)] for x in range(4)]):
                    break
                reachable.add(current_node)
            
            paths[current_node].add(previous_node)
            
            for nd, cdir in enumerate(dirs):
                if nd == (d + 2) % 4:
                    continue
                
                dx, dy = cdir
                new_distance = current_distance + 1 if d == nd else current_distance + 1000
                
                nx, ny = cx + dx, cy + dy
                neighbour = (nx, ny, nd)
                
                if graph[nx][ny] == "#":
                    continue
                
                if current_distance <= distances[neighbour]:
                    heapq.heappush(priority_queue, (new_distance, neighbour, current_node))
        
        return paths, reachable
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
        
        start = (0, 0)
        end = (0, 0)
        dimx = len(grid)
        dimy = len(grid[0])
        
        for i in range(dimx):
            for j in range(dimy):
                if grid[i][j] == 'S':
                    start = (i, j)
                if grid[i][j] == 'E':
                    end = (i, j)
        
        paths, reachable = self.dijkstra(grid, start, end)
        
        queue = list(reachable)
        visited = set([])
        result = set([])
        
        while queue:
            node = queue.pop(0)
            
            if node in visited:
                continue
            
            x, y, _ = node
            visited.add(node)
            result.add((x, y))
            
            for last in paths[node]:
                queue.append(last)
        
        # We subtract 1 because (None, None) is there since the start node does not
        # have a predecessor.
        return len(result) - 1


solver = Solver(64)
solver.solve()