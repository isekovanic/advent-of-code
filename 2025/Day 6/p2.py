import sys
from itertools import zip_longest

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        # replace all newlines with empty spaces - it won't really change anything
        # while zipping later and it takes care of lower length lines which we want
        # to avoid
        problem_input = [x.replace('\n', ' ') for x in problem_input]
        # the last line (containing the operations) is naturally shorter as the operands
        # are left padded; while there are many smarter ways to solve this, hacking
        # it by padding it with a ton of empty spaces at the end (which we'll anyway strip
        # away) does the trick
        problem_input[len(problem_input) - 1] += ' ' * 100
        
        result = 0
        intermediary_result = 0
        current_operation = ''
        
        # we transpose the entire input intentionally in order to get exactly what we need,
        # while making sure that we count and parse all instances of operands
        for line in [''.join(item) for item in zip_longest(*problem_input, fillvalue='')]:
            *val, operation = line
            if operation in '*+':
                result += intermediary_result
                intermediary_result = 0 if operation == '+' else 1
                current_operation = operation
            
            joined = ''.join(val).strip()
            if len(joined) == 0:
                continue
            int_val = int(joined)
            if current_operation == '*':
                intermediary_result *= int_val
            else:
                intermediary_result += int_val
        
        # we add the last intermediary_result as the string ended before we have a chance to count it
        return result + intermediary_result


solver = Solver(3263827)
solver.solve()