import sys
import heapq

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# Grossly overengineered this one. Part 2 is actually simpler that part 1 here.
# Essentially, I was under the impression that running Dijkstra's across the entire
# grid would be suboptimal so I decided to compress the entire graph. Each straight
# line is compressed into a single weighted edge, while turns are handled as normal.
# What we get is a graph with far less nodes as well as edges. It turns out that the
# large input just seems big and can easily be handled.
# But hey, it runs fast !

# clockwise
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Solver(SolverCore):
    def dijkstra(self, graph, start, end):
        distances = defaultdict(lambda: sys.maxsize)
        distances[start] = 0
        priority_queue = [(0, start)]
    
        visited = set([])
    
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            cx, cy, _ = current_node
            
            if (cx, cy) == end:
                return current_distance
            
            if current_node in visited:
                continue
    
            visited.add(current_node)
    
            for neighbor, weight in graph[current_node].items():
                if neighbor in visited:
                    continue
                
                new_distance = current_distance + weight
    
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))
    
        return -1
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
        
        start = (0, 0, 0)
        end = (0, 0)
        dimx = len(grid)
        dimy = len(grid[0])
        
        for i in range(dimx):
            for j in range(dimy):
                if grid[i][j] == 'S':
                    start = (i, j, 0)
                if grid[i][j] == 'E':
                    end = (i, j)
        
        edges = defaultdict(dict)
        stack = [start]
        visited = set([])
        
        while stack:
            current = stack.pop()
            cx, cy, dir = current
            
            if current in visited:
                continue
            
            visited.add(current)
            
            dx, dy = dirs[dir]
            weight = 0
            
            nx, ny = cx, cy
            last = (nx, ny, dir)
            
            while True:
                for i, cdir in enumerate(dirs):
                    if i in [dir, (dir + 2) % 4]:
                        continue
                    cdx, cdy = cdir
                    new_node = (nx, ny, i)
                    if grid[nx + cdx][ny + cdy] != '#':
                        stack.append(new_node)
                        edges[(nx, ny, dir)][new_node] = 1000
                        if weight > 0:
                            edges[current][(nx, ny, dir)] = weight
                        
                nx, ny = nx + dx, ny + dy
                if grid[nx][ny] == '#':
                    break
                
                last = (nx, ny, dir)
                
                weight += 1
            
            if weight > 0:
                edges[current][last] = weight
        
        return self.dijkstra(edges, start, end)


solver = Solver(11048)
solver.solve()