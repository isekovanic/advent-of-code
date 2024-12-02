import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        for report in problem_input:
            original_numbers = [int(x) for x in report.strip().split(' ')]
            
            safe = False
            
            for i in range(len(original_numbers)):
                numbers = original_numbers[:]
                numbers.pop(i)
                
                dir = -1 if numbers[0] - numbers[1] <= 0 else 1
                if all([0 < dir * (i - j) <= 3 for i, j in zip(numbers, numbers[1:])]):
                    safe = True
                    break
            
            if (safe):
                result += 1
            
        return result


solver = Solver(4)
solver.solve()