import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict
from itertools import combinations

class Solver(SolverCore):
    def get_antinodes(self, antenna, dx, dy, dimx, dimy):
        antinodes = set([])
        
        nx, ny = antenna
        
        while True:
            nx, ny = nx + dx, ny + dy
            print(antenna, nx, ny)
            if 0 <= nx < dimx and 0 <= ny < dimy:
                antinodes.add((nx, ny))
            else:
                break
        
        return antinodes
    def _solve(self, problem_input):
        grid = [x.strip() for x in problem_input]
        antenna_coordinates = defaultdict(list)
        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != '.':
                    antenna_coordinates[grid[i][j]].append((i, j))
        
        dimx, dimy = len(grid), len(grid[0])
        antinodes = set([])
        
        for type, vals in antenna_coordinates.items():
            for pair in combinations(vals, 2):
                f, s = pair
                
                if s[1] > f[1] or s[1] == f[1] and s[0] > f[0]:
                    f, s = s, f
                    
                dx, dy = s[0] - f[0], s[1] - f[1]
                
                antinodes |= self.get_antinodes(f, -dx, -dy, dimx, dimy) | self.get_antinodes(s, dx, dy, dimx, dimy)
                antinodes.add(f)
                antinodes.add(s)
                
        return len(antinodes)


solver = Solver(34)
solver.solve()