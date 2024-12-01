import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        left_list = []
        right_list = []
        
        for line in problem_input:
            left, right = re.findall('[0-9]+', line.strip())
            
            left_list.append(int(left))
            right_list.append(int(right))
        
        result = 0
        
        for left in left_list:
            result += right_list.count(left) * left

        return result


solver = Solver(31)
solver.solve()