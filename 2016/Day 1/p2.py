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
        visited = set([position])
        
        for command in commands:
            turn, steps = command[0], int(command[1:])
            
            if turn == 'R':
                direction = (direction + 1) % 4
            else:
                direction = (direction - 1) % 4
            
            dx, dy = directions[direction]
            
            for _ in range(steps):
                x, y = position
                position = (x + dx, y + dy)
                if position in visited:
                    return abs(position[0]) + abs(position[1])
                visited.add(position)
                
        # no such location, should not happen
        return -1


solver = Solver(4)
solver.solve()