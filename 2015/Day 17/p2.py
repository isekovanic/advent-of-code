import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def subset_sum(self, numbers, target, partial = [], partial_sum = 0):
        if partial_sum == target:
            yield partial
        if partial_sum >= target:
            return
        for i, n in enumerate(numbers):
            remaining = numbers[i + 1:]
            yield from self.subset_sum(remaining, target, partial + [n], partial_sum + n)
    def _solve(self, problem_input):
        numbers = [int(x) for x in problem_input]
        target = 150
        
        subsets = list(self.subset_sum(numbers, target))
        if len(subsets) == 0:
            return 0
        
        minimum_length = min([len(subset) for subset in subsets])
        
        return len([subset for subset in subsets if len(subset) == minimum_length])


solver = Solver(0)
solver.solve()