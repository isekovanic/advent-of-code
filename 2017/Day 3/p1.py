import sys

sys.path.append('../../')

from Core import SolverCore

directions = {
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
    4: (0, 1)
}
class Solver(SolverCore):
    def _solve(self, problem_input):
        number = int(problem_input[0].strip())
        
        idx = 0
        last = 1
        while last + 8 * idx < number:
            last += 8 * idx
            idx += 1
        
        last += 1
        pos = (-idx + 1, idx)
        direction = 1
        while last + idx * 2 < number:
            diff = idx * 2 - (direction == 1)
            last += diff
            x, y = pos
            dx, dy = directions[direction]
            pos = (x + dx * diff, y + dy * diff)
            direction += 1
        
        x, y = pos
        dx, dy = directions[direction]
        pos = (x + dx * (number - last), y + dy * (number - last))

        return abs(pos[0]) + abs(pos[1])
 

solver = Solver(0)
solver.solve()