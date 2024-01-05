import sys

sys.path.append('../../')

from Core import SolverCore

keypad = ['...1...', '..234..', '.56789.', '..ABC..', '...D...',]
directions = {
    'U': (-1, 0),
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0)
}
class Solver(SolverCore):
    def is_valid(self, position):
        x, y = position
        
        return 0 <= x < len(keypad) and 0 <= y < len(keypad[0]) and keypad[x][y] != '.'
    def _solve(self, problem_input):
        position = (2, 1)
        result = ''
        
        for line in problem_input:
            for move in line.strip():
                x, y = position
                dx, dy = directions[move]
                
                new_position = (x + dx, y + dy)
                if self.is_valid(new_position):
                    position = new_position
            x, y = position
            result += keypad[x][y]

        return result


solver = Solver('5DB3')
solver.solve()