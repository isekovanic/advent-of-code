import sys

sys.path.append('../../')

from Core import SolverCore

directions = {
    'n': (1, 0),
    'e': (0, 1),
    'w': (0, -1),
    's': (-1, 0),
    'ne': (0.5, 0.5),
    'nw': (0.5, -0.5),
    'se': (-0.5, 0.5),
    'sw': (-0.5, -0.5),
}
class Solver(SolverCore):
    def _solve(self, problem_input):
        steps = problem_input[0].strip().split(',')
        
        current = (0, 0)
        result = 0
        
        for step in steps:
            dx, dy = directions[step]
            
            x, y = current
            current = (x + dx, y + dy)
            
            result = max(result, int(abs(current[0]) + abs(current[1])))

        return result

solver = Solver(3)
solver.solve()