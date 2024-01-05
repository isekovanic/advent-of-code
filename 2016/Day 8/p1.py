import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        m, n = 6, 50
        
        screen = [['.' for _ in range(n)] for _ in range(m)]
        
        for line in problem_input:
            if 'rotate' in line:
                idx, steps = [int(x) for x in re.findall('[0-9]+', line)]
                if 'row' in line:
                    steps %= n
                    screen[idx] = screen[idx][-steps:] + screen[idx][:-steps]
                else:
                    screen = list(zip(*screen))
                    steps %= m
                    screen[idx] = screen[idx][-steps:] + screen[idx][:-steps]
                    screen = [list(row) for row in list(zip(*screen))]
            else:
                _, dimensions = line.split(' ')
                dim_x, dim_y = [int(x) for x in dimensions.split('x')]
                for i in range(dim_y):
                    for j in range(dim_x):
                        screen[i][j] = '#'

        return sum([row.count('#') for row in screen])


solver = Solver(6)
solver.solve()