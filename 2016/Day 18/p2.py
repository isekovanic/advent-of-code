import sys

sys.path.append('../../')

from Core import SolverCore

valid_traps = ['^^.', '.^^', '^..', '..^']
class Solver(SolverCore):
    def _solve(self, problem_input):
        current_row = problem_input[0].strip()
        
        repetitions = 400000
        result = 0
        
        for _ in range(repetitions):
            result += current_row.count('.')
            new_row = ''
            
            current_row = '.' + current_row + '.'
            for j in range(1, len(current_row) - 1):
                if current_row[j - 1:j + 2] in valid_traps:
                    new_row += '^'
                else:
                    new_row += '.'
            current_row = new_row
        
        return result


solver = Solver(1935478)
solver.solve()