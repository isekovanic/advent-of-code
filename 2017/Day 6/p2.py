import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        banks = [int(x) for x in re.findall('[0-9]+', problem_input[0].strip())]
        
        seen = {}
        current = tuple(banks)
        steps = 0
        
        while current not in seen:
            seen[current] = steps
            next_val = max(banks)
            next_idx = banks.index(next_val)
            banks[next_idx] = 0
            
            idx = next_idx + 1
            while next_val > 0:
                idx %= len(banks)
                banks[idx] += 1
                next_val -= 1
                idx += 1
            
            current = tuple(banks)
            steps += 1

        return steps - seen[current]


solver = Solver(4)
solver.solve()