import sys

sys.path.append('../../')

from Core import SolverCore

# has to be (anti)clockwise for this to work
moves = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
        
        dim = len(grid)
        result = 0
        
        for i in range(dim):
            for j in range(dim):
                if grid[i][j] == 'A':
                    accumulated = ''
                    for move in moves:
                        dx, dy = move
                        di, dj = i + dx, j + dy
                        
                        if 0 <= di < dim and 0 <= dj < dim:
                            accumulated += grid[di][dj]
                    
                    # crossing letters produce SAS and MAM rather than MAS
                    result += ''.join(sorted(accumulated)) == 'MMSS' and accumulated != 'SMSM' and accumulated != 'MSMS'
                
        return result


solver = Solver(9, { 'test': 'input_test_p2.txt' })
solver.solve()