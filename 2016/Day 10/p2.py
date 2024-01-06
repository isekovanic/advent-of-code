import sys
import re
from collections import defaultdict
from functools import reduce

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        
        bots = defaultdict(list)
        rules = defaultdict(list)
        outputs = defaultdict(list)
        
        for line in problem_input:
            numbers = re.findall('[0-9]+', line)
            if 'goes' in line:
                value, bot = numbers
                value = int(value)
                bots[bot] += [value]
            else:
                bot, lo, hi = numbers
                if 'low to output' in line:
                    lo = 'o' + lo
                if 'high to output' in line:
                    hi = 'o' + hi
                rules[bot] = [lo, hi]
                
        while True:
            found = False
            for bot, vals in bots.items():
                if bot[0] != 'o' and len(vals) == 2:
                    lo, hi = min(vals), max(vals)
                    found = True
                    r_lo, r_hi = rules[bot]

                    if r_lo[0] != 'o':
                        bots[r_lo] += [lo]
                    else:
                        outputs[r_lo] += [lo]

                    if r_hi[0] != 'o':
                        bots[r_hi] += [hi]
                    else:
                        outputs[r_hi] += [hi]
                    
                    bots[bot] = []
                    break
                    
            if not found:
                break
        
        return reduce(lambda x, y: x * y, [int(x) for x in outputs['o0'] + outputs['o1'] + outputs['o2']])


solver = Solver(30)
solver.solve()
