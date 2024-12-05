import sys

sys.path.append('../../')

from Core import SolverCore

moves = [(0, 1), (1, 0), (1, 1), (-1, 1)]

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
        
        dim = len(grid)
        result = 0
        
        for i in range(dim):
            for j in range(dim):
                for move in moves:
                    accumulated = ''
                    dx, dy = move
                    
                    di, dj = i, j
                    
                    while 0 <= di < dim and 0 <= dj < dim:
                        accumulated = (accumulated + grid[di][dj])
                        if len(accumulated) == 4:
                            break
                        di += dx
                        dj += dy
                    
                    if accumulated == 'XMAS' or accumulated == 'SAMX':
                        result += 1
                        
        return result


solver = Solver(18, { 'test': 'input_test_p1.txt' })
solver.solve()