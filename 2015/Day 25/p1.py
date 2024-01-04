import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def next_code(self, code):
        return (code * 252533) % 33554393
    def _solve(self, problem_input):
        row, col = [int(x) for x in list(re.findall('[0-9]+', problem_input[0].strip()))]
        
        diagonal = row + col - 1
        diagonal_start = diagonal * (diagonal - 1) // 2
        wanted_number = diagonal_start + col
        
        code = 20151125
        
        for i in range(2, wanted_number + 1):
            code = self.next_code(code)
        
        return code


solver = Solver(7981243)
solver.solve()