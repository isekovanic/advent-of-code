import sys

sys.path.append('../../')

from Core import SolverCore

directions = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}
class Solver(SolverCore):
    def _solve(self, problem_input):
        moves = problem_input[0].strip()
        start = (0, 0)
        visited = set([start])
        
        for char in moves:
            x, y = directions[char]
            
            s_x, s_y = start
            start = (s_x + x, s_y + y)
            visited.add(start)
        
        return len(visited)


solver = Solver(2)
solver.solve()