import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def subset_sum(self, numbers, target, partial = [], partial_sum = 0):
        if partial_sum == target:
            yield partial
        if partial_sum >= target:
            pass
        for i, n in enumerate(numbers):
            remaining = numbers[i + 1:]
            yield from self.subset_sum(remaining, target, partial + [n], partial_sum + n)
    def _solve(self, problem_input):
        numbers = [int(x) for x in problem_input]
        target = 150
        
        return len(list(self.subset_sum(numbers, target)))


solver = Solver(0)
solver.solve()