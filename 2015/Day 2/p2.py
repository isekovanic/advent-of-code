import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        for line in problem_input:
            l, w, h = [int(x) for x in line.split('x')]
            
            ribbon = 2 * min(l + w, w + h, l + h)
            bow = l * w * h
            
            result += ribbon + bow
            
        return result


solver = Solver(48)
solver.solve()