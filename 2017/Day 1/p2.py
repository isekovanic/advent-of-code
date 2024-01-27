import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        digits = [int(x) for x in problem_input[0].strip()]
        
        result = 0
        
        for idx, digit in enumerate(digits):
            new_idx = (idx + len(digits) // 2) % len(digits)
            if digit == digits[new_idx]:
                result += digit
        
        return result


solver = Solver(4)
solver.solve()