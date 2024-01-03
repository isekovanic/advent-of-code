import sys
from copy import deepcopy

sys.path.append('../../')

from Core import SolverCore

directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
class Solver(SolverCore):
    def is_valid(self, node, grid):
        x, y = node
        
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])
    def get_neighbours(self, node, grid):
        x, y = node
        neighbours = []
        
        for d_x, d_y in directions:
            neighbour = (x + d_x, y + d_y)
            if self.is_valid(neighbour, grid):
                neighbours += [neighbour]
                
        return neighbours
    def _solve(self, problem_input):
        grid = [list(row.strip()) for row in problem_input]
        steps = 100
        
        for _ in range(steps):
            new_grid = deepcopy(grid)
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    on_neighbours = sum([1 if grid[n_x][n_y] == '#' else 0 for n_x, n_y in self.get_neighbours((i, j), grid)])

                    if grid[i][j] == '.' and on_neighbours == 3:
                        new_grid[i][j] = '#'
                    elif grid[i][j] == '#' and on_neighbours != 2 and on_neighbours != 3:
                        new_grid[i][j] = '.'
            
            if grid == new_grid:
                break
            grid = deepcopy(new_grid)

        return sum([row.count('#') for row in grid])


solver = Solver(4)
solver.solve()