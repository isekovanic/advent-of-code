import sys

sys.path.append('../../')

from Core import SolverCore

directions = [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

removed = set([])
class Solver(SolverCore):
    def remove_rolls(self, grid):
        w, h = len(grid), len(grid[0])
        
        result = 0
        
        for i in range(w):
            for j in range(h):
                rolls = 0
                
                if grid[i][j] != '@' or (i, j) in removed:
                    continue
                
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    
                    if 0 <= ni < w and 0 <= nj < h:
                        rolls += (grid[ni][nj] == '@' and (ni, nj) not in removed)
                
                if rolls < 4:
                    removed.add((i, j))
                    result += 1
        
        return result

    def _solve(self, problem_input):
        grid = [line.strip() for line in problem_input]
        
        while True:
            if self.remove_rolls(grid) == 0:
                break

        return len(removed)


solver = Solver(43)
solver.solve()