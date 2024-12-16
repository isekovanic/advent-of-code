import sys

sys.path.append('../../')

from Core import SolverCore

# We use a map of coordinates -> characters since modifying list elements directly
# would be quite slow. It's a nice performance boost.

move_map = {
    '>': (0, 1),
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0),
}

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid_input = [list(x) for x in problem_input[0]]
        moves = ''.join(problem_input[1])
        
        dimx, dimy = len(grid_input), len(grid_input[0])
        grid = {}
        
        current = (0, 0)
        for i in range(dimx):
            for j in range(dimy):
                point = (i, j)
                grid[point] = grid_input[i][j]
                if grid[point] == '@':
                    current = point
        
        for move in moves:
            cx, cy = current
            dx, dy = move_map[move]
            
            new_point = (cx + dx, cy + dy)
            
            if grid[new_point] == '#':
                continue
            
            if grid[new_point] == '.':
                grid[new_point] = '@'
                grid[current] = '.'
                current = new_point
            
            if grid[new_point] == 'O':
                new_box_point = new_point
                while grid[new_box_point] == 'O':
                    nx, ny = new_box_point
                    new_box_point = (nx + dx, ny + dy)
                    
                if grid[new_box_point] == '.':
                    grid[current] = '.'
                    grid[new_point] = '@'
                    grid[new_box_point] = 'O'
                    current = new_point
        
        result = 0
        for point, val in grid.items():
            if val == 'O':
                x, y = point
                result += 100 * x + y

        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(10092)
solver.solve()