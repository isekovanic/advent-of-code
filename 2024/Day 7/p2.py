import sys
import re

sys.path.append('../../')

from Core import SolverCore
from itertools import product

# I'm sure there's some clever DP to solve this, but the number of combinations is not that large. The
# solution works in ~15 seconds so there's no need.
class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            solution, *parts = [int(x) for x in re.findall('[0-9]+', line.strip())]
            
            combinations = [list(c) for c in product(['*', '+', '||'], repeat = len(parts) - 1)]
            
            for combination in combinations:
                equation_result = parts[0]
                for i in range(1, len(parts)):
                    if combination[i - 1] == '||':
                        equation_result = int(f'{equation_result}{parts[i]}')
                    else:
                        equation_result = equation_result * parts[i] if combination[i - 1] == '*' else equation_result + parts[i]
                    
                    if equation_result > solution:
                        break
                
                if equation_result == solution:
                    result += solution
                    break
            
        return result


solver = Solver(0)
solver.solve()