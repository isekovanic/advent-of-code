import sys

sys.path.append('../../')

from Core import SolverCore

# Note: I was really convinced that Part 2 would be the same task but with a much, much larger
# input; hence the over-engineered Part 1. Part 2 would've been a 2-liner change had I gone
# with the "just do it" approach.

directions = {
    0: (1, 0),
    1: (0, -1),
    2: (-1, 0),
    3: (0, 1)
}
class Solver(SolverCore):
    def calculate_value(self, point, values):
        value = 0
        x, y = point
        for n_x, n_y in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
            neighbour = (x + n_x, y + n_y)
            if neighbour in values:
                value += values[neighbour]
        
        return value
        
    def _solve(self, problem_input):
        number = int(problem_input[0].strip())
        
        idx = 0
        pos = (0, 0)
        values = { pos: 1 }
        direction = 3
        
        while values[pos] < number:
            x, y = pos
            dx, dy = directions[direction]
            pos = (x + dx, y + dy)
            if pos in [(idx, idx), (idx, -idx), (-idx, -idx), (-idx, idx + 1)]:
                direction = (direction + 1) % 4
            
            if pos == (-idx, idx + 1):
                idx += 1
            
            values[pos] = self.calculate_value(pos, values)
            
        return values[pos]
 

solver = Solver(1968)
solver.solve()