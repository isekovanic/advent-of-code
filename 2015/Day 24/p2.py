import sys
from functools import reduce

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def find_groups_with_size(self, size, wanted_weight, weights, group = []):
        if len(group) > size or (len(group) == size and sum(group) != wanted_weight):
            return
        
        if len(group) == size and sum(group) == wanted_weight:
            yield group
        
        for i, weight in enumerate(weights):
            yield from self.find_groups_with_size(size, wanted_weight, weights[i + 1:], group + [weight])
            
        
    def _solve(self, problem_input):
        weights = [int(x.strip()) for x in problem_input]
        group_weight = sum(weights) // 4
        
        result = sys.maxsize
        
        for size in range(1, len(weights)):
            for group in self.find_groups_with_size(size, group_weight, weights):
                quantum_entaglement = reduce(lambda x, y: x * y, group)
                result = min(result, quantum_entaglement)
            
            if result != sys.maxsize:
                break
            
        return result


solver = Solver(44)
solver.solve()