import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def bfs(self, start, grid):
        visited = set([])
        queue = [start]
        
        dimx = len(grid)
        dimy = len(grid[0])
        
        result = 0
        
        while len(queue):
            current = queue.pop()
            x, y = current
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if grid[x][y] == 9:
                result += 1
                continue
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = (x + dx, y + dy)
                neighbour = (nx, ny)
                
                if 0 <= nx < dimx and 0 <= ny < dimy and neighbour not in visited and grid[x][y] + 1 == grid[nx][ny]:
                    queue.append(neighbour)
        
        return result
        
    def _solve(self, problem_input):
        grid = [list([int(c) for c in x.strip()]) for x in problem_input]
        result = 0
        
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 0:
                    result += self.bfs((i, j), grid)
                    
        return result


solver = Solver(36)
solver.solve()