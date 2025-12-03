import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def calculate_max(self, joltages, depth):
        if depth >= 12:
            return 0
        
        to_pick = 12 - depth - 1
        
        max_left_jolt = max(joltages[:-to_pick]) if to_pick > 0 else max(joltages)
        max_left_jolt_idx = joltages.index(max_left_jolt)
        
        return max_left_jolt * 10 ** to_pick + self.calculate_max(joltages[max_left_jolt_idx + 1:], depth + 1)
        
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            joltages = [int(x) for x in line.strip()]
            
            result += self.calculate_max(joltages, 0)

        return result


solver = Solver(3121910778619)
solver.solve()