import sys

sys.path.append('../../')

from Core import SolverCore

# up, right, down, left
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Solver(SolverCore):
    def _solve(self, problem_input):
        commands = problem_input[0].strip().split(', ')
        position = (0, 0)
        direction = 0
        
        for command in commands:
            turn, steps = command[0], int(command[1:])
            
            if turn == 'R':
                direction = (direction + 1) % 4
            else:
                direction = (direction - 1) % 4
            
            dx, dy = directions[direction]
            x, y = position
            position = (x + dx * steps, y + dy * steps)
        
        x, y = position
        
        return abs(x) + abs(y)


solver = Solver(8)
solver.solve()