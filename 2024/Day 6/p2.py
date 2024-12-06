import sys

sys.path.append('../../')

from Core import SolverCore

# This solution runs pretty slowly (around 20s) because it bruteforces through all of the
# possible places where you can place a # in order to put the guard into a loop. I couldn't
# think of something more clever than this.

moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
start_map = {
    '^': 0,
    '>': 1,
    '<': 2,
    'v': 3,
}
class Solver(SolverCore):
    def check_grid(self, grid, start, dir, obstacle):
        current = start
        visited = set([])
        while True:
            i, j = current
 
            state = (i, j, dir)
            if state in visited:
                return True
 
            visited.add(state)
            
            di, dj = moves[dir]
            
            ni, nj = i + di, j + dj
            
            if ni < 0 or ni >= len(grid) or nj < 0 or nj >= len(grid[0]):
                break
            
            if grid[ni][nj] == '#' or (ni, nj) == obstacle:
                dir = (dir + 1) % 4
            else:
                current = (ni, nj)
        
        return False
    def _solve(self, problem_input):
        grid = [x.strip() for x in problem_input]
        
        start = (0, 0)
        dir = 0
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] in start_map.keys():
                    start = (i, j)
                    dir = start_map[grid[i][j]]
                    break
        
        result = 0
        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != '.':
                    continue

                new_obstacle = (i, j)
                result += self.check_grid(grid, start, dir, new_obstacle)

        return result


solver = Solver(6)
solver.solve()