import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        for report in problem_input:
            numbers = [int(x) for x in report.strip().split(' ')]
            
            dir = -1 if numbers[0] - numbers[1] <= 0 else 1
            result += all([0 < dir * (i - j) <= 3 for i, j in zip(numbers, numbers[1:])])

        return result


solver = Solver(2)
solver.solve()