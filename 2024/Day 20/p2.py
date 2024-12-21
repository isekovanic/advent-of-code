import sys

sys.path.append('../../')

from Core import SolverCore

# Everything that we've mentioned in part 1 still stands, however we need to take
# into account the number of steps we can spend into walls too. We run a stateful
# BFS from each node on the track which flood fills the grid but only going through
# walls (since if we reach another part of the track the cheat stops). Care to also
# subtract the distance travelled by the cheat, as that counts as well into the final
# sum of picoseconds.

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
class Solver(SolverCore):
    def bfs(self, distances, grid, start):
        x, y = start
        queue = [(x, y, 0)]
        visited = set([])
        dimx = len(grid)
        dimy = len(grid[0])
        result = 0
        
        while queue:
            current = queue.pop(0)
            cx, cy, dist = current
            
            current_node = (cx, cy)
            
            if current_node in visited or dist > 20:
                continue
            
            visited.add(current_node)
            
            if grid[cx][cy] != '#':
                save = distances[(cx, cy)] - distances[(x, y)] - dist
                if save >= 100:
                    result += 1
            
            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < dimx and 0 <= ny < dimy:
                    queue.append((nx, ny, dist + 1))
        
        return result
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
      
        start = (0, 0)
        end = (0, 0)
        
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 'S':
                    start = (i, j)
                if val == 'E':
                    end = (i, j)
        
        distances = { start: 0 }
        current = start
        
        while current != end:
            x, y = current
            
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                
                if grid[nx][ny] in ['.', 'E'] and (nx, ny) not in distances:
                    distances[(nx, ny)] = distances[(x, y)] + 1
                    current = (nx, ny)
                    break
        
        result = 0
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val != '#':
                    result += self.bfs(distances, grid, (i, j))
       
        return result


solver = Solver(0)
solver.solve()