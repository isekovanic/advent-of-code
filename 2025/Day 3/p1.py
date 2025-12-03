import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            joltages = [int(x) for x in line.strip()]
            
            max_left_jolt = max(joltages[:-1])
            max_left_jolt_idx = joltages.index(max_left_jolt)
            
            max_right_jolt = max(joltages[max_left_jolt_idx + 1:])
            
            result += max_left_jolt * 10 + max_right_jolt

        return result


solver = Solver(357)
solver.solve()