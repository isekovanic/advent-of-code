import sys

sys.path.append('../../')

from Core import SolverCore

# In order to quickly be able to calculate how much time we save by taking a shortcut
# and activating the cheat mechanism, we calculate the distance from the start to each
# node in the grid first and only then start checking the cheats. A cheat can be activated
# if we have a neighbouring '#' character to the node we're currently sitting at that
# extends into something that we can move to (so basically 'E' or '.').
# With that observation, after we've precalculated all of the distances we can go through
# each node in the grid and check for each one that belongs to the track. The time we save
# is essentially the distance between our current node subtracted from the node we want to
# move to.

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
        dimx = len(grid)
        dimy = len(grid[0])
        
        start = (0, 0)
        end = (0, 0)
        
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == 'S':
                    start = (i, j)
                if val == 'E':
                    end = (i, j)
        
        distances = { start: 0 }
        current = start
        
        while current != end:
            x, y = current
            
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                
                if grid[nx][ny] in ['.', 'E'] and (nx, ny) not in distances:
                    distances[(nx, ny)] = distances[(x, y)] + 1
                    current = (nx, ny)
                    break
        
        result = 0
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val not in ['.', 'S']:
                    continue
                for dx, dy in dirs:
                    nx, ny = i + dx, j + dy
                    nnx, nny = nx + dx, ny + dy
                    
                    if grid[nx][ny] == '#' and 0 <= nnx < dimx and 0 <= nny < dimy and grid[nnx][nny] in ['.', 'E']:
                        result += distances[(nnx, nny)] - distances[(i, j)] - 1 >= 100
        
        return result


solver = Solver(0)
solver.solve()