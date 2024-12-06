import sys

sys.path.append('../../')

from Core import SolverCore

moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
start_map = {
    '^': 0,
    '>': 1,
    '<': 2,
    'v': 3,
}
class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [x.strip() for x in problem_input]
        
        current = (0, 0)
        dir = 0
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] in start_map.keys():
                    current = (i, j)
                    dir = start_map[grid[i][j]]
                    break
        
        visited = set([])
        
        while True:
            visited.add(current)
            
            i, j = current
            
            di, dj = moves[dir]
            
            ni, nj = i + di, j + dj
            
            if ni < 0 or ni >= len(grid) or nj < 0 or nj >= len(grid[0]):
                break
            
            if grid[ni][nj] == '#':
                dir = (dir + 1) % 4
            else:
                current = (ni, nj)
            
        return len(visited)


solver = Solver(0)
solver.solve()