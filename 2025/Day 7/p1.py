import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [list(x) for x in problem_input]
        start = (0, grid[0].index('S'))
        
        beams = { start: 0 }
        
        result = set([])
        
        while len(beams):
            items = list(beams.items())[:]
            for k, v in items:
                v += 1
                _, y = k
                
                if v >= len(grid):
                    del beams[k]
                    continue
                
                if grid[v][y] == '^':
                    del beams[k]
                    beams[(v, y - 1)] = v
                    beams[(v, y + 1)] = v
                    result.add((v, y))
                    
                    continue
                
                beams[k] = v
                
        return len(result)


solver = Solver(21)
solver.solve()