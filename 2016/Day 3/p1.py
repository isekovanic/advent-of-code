import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        for line in problem_input:
            sides = [int(x.strip()) for x in list(filter(lambda x: x != '', line.strip().split(' ')))]
            
            x, y, z = sides
            if x + y > z and x + z > y and y + z > x:
                result += 1

        return result


solver = Solver(0)
solver.solve()