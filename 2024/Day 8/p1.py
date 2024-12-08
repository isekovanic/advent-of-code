import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict
from itertools import combinations

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [x.strip() for x in problem_input]
        antenna_coordinates = defaultdict(list)
        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != '.':
                    antenna_coordinates[grid[i][j]].append((i, j))
        
        antinodes = set([])
        
        for type, vals in antenna_coordinates.items():
            for pair in combinations(vals, 2):
                f, s = pair
                
                if s[1] > f[1] or s[1] == f[1] and s[0] > f[0]:
                    f, s = s, f
                    
                dx, dy = s[0] - f[0], s[1] - f[1]
                new_antinodes = [(f[0] - dx, f[1] - dy), (s[0] + dx, s[1] + dy)]
                
                for new_antinode in new_antinodes:
                    nx, ny = new_antinode
                    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                        antinodes.add(new_antinode)
                
        return len(antinodes)


solver = Solver(14)
solver.solve()