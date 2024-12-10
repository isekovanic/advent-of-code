import sys

sys.path.append('../../')

from Core import SolverCore

# We backtrack on the number of ways each node is reachable. If in a single step we can
# go in multiple directions, we add up the number of ways each one of them is reachable.
# We memoize the already known ways to each each one too for performance reasons.

ways = {}
class Solver(SolverCore):
    def bfs(self, start, grid):
        global ways
        
        x, y = start
        dimx = len(grid)
        dimy = len(grid[0])
        
        if start in ways:
            return ways[start]
        
        if grid[x][y] == 0:
            return 1
        
        ways[start] = 0
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < dimx and 0 <= ny < dimy and grid[x][y] - 1 == grid[nx][ny]:
                ways[start] += self.bfs((nx, ny), grid)
        
        return ways[start]
    def _solve(self, problem_input):
        grid = [list([int(c) for c in x.strip()]) for x in problem_input]
        result = 0
        
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 9:
                    result += self.bfs((i, j), grid)
                    
        return result


solver = Solver(81)
solver.solve()