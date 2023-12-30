import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        for line in problem_input:
            l, w, h = [int(x) for x in line.split('x')]
            
            area = 2 * l * w + 2 * w * h + 2 * l * h
            slack = min(l * w, w * h, l * h)
            
            result += area + slack
            
        return result


solver = Solver(101)
solver.solve()