import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        banks = [int(x) for x in re.findall('[0-9]+', problem_input[0].strip())]
        
        seen = set([])
        current = tuple(banks)
        
        while current not in seen:
            seen.add(current)
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

        return len(seen)


solver = Solver(5)
solver.solve()