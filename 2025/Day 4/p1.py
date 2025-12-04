import sys

sys.path.append('../../')

from Core import SolverCore

directions = [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [line.strip() for line in problem_input]
        
        w, h = len(grid), len(grid[0])
        
        result = 0
        
        for i in range(w):
            for j in range(h):
                rolls = 0
                
                if grid[i][j] != '@':
                    continue
                
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    
                    if 0 <= ni < w and 0 <= nj < h:
                        rolls += grid[ni][nj] == '@'
                
                if rolls < 4:
                    result += 1

        return result


solver = Solver(13)
solver.solve()