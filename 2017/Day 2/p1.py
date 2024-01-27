import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        spreadsheet = [[int(x) for x in re.findall('[0-9]+', line.strip())] for line in problem_input]
        
        result = 0
        for row in spreadsheet:
            result += max(row) - min(row)

        return result


solver = Solver(18)
solver.solve()