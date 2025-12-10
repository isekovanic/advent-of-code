import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        points = [tuple([int(x) for x in line.strip().split(',')]) for line in problem_input]
        
        result = 0
        
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                (x1, y1), (x2, y2) = points[i], points[j]
                result = max(result, (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1))
        
        return result


solver = Solver(50)
solver.solve()