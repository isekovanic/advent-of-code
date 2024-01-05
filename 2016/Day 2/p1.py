import sys

sys.path.append('../../')

from Core import SolverCore

keypad = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
directions = {
    'U': (-1, 0),
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0)
}
class Solver(SolverCore):
    def is_valid(self, position):
        x, y = position
        
        return 0 <= x < 3 and 0 <= y < 3
    def _solve(self, problem_input):
        position = (1, 1)
        result = ''
        
        for line in problem_input:
            for move in line.strip():
                x, y = position
                dx, dy = directions[move]
                
                new_position = (x + dx, y + dy)
                if self.is_valid(new_position):
                    position = new_position
            x, y = position
            result += str(keypad[x][y])

        return int(result)


solver = Solver(1985)
solver.solve()