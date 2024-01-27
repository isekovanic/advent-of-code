import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        spreadsheet = [[int(x) for x in re.findall('[0-9]+', line.strip())] for line in problem_input]
        
        result = 0
        for row in spreadsheet:
            for i_f, first in enumerate(row):
                for i_s, second in enumerate(row):
                    if i_f != i_s and max(first, second) % min(first, second) == 0:
                        result += max(first, second) // min(first, second)

        # we could each pair twice, hence the division
        return result // 2


solver = Solver(9)
solver.solve()