import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        sides = [[int(x.strip()) for x in list(filter(lambda x: x != '', line.strip().split(' ')))] for line in problem_input]
        
        for i in range(len(sides[0])):
            for j in range(0, len(sides), 3):
                x, y, z = sides[j][i], sides[j + 1][i], sides[j + 2][i]
                if x + y > z and x + z > y and y + z > x:
                    result += 1

        return result


solver = Solver(3)
solver.solve()