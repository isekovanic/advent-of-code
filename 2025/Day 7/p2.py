import sys
from collections import defaultdict

sys.path.append('../../')

from Core import SolverCore

# This one is a simple memoization problem. Since the direction we'll always go in
# is downwards (i.e it works like a tree rather than a graph), it's easy to conclude
# that by the time we reach a new splitter we'll have known all of the possible ways
# to reach all of the splitters above it (since we would know their "parents" by the
# time we get to them). After that, it's a matter of adding the up all of the ways in
# which we can get to the splitter before doing the actual splitting (which means
# proceeding to the next line for us) and add up the number of ways every time we reach
# the end of the grid.
class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [list(x) for x in problem_input]
        start = (0, grid[0].index('S'))
        
        beams = { start: 0 }
        
        cache = defaultdict(int)
        cache[start] = 1
        
        result = 0
        
        while len(beams):
            items = list(beams.items())[:]
            for k, v in items:
                v += 1
                _, y = k
                
                if v >= len(grid):
                    del beams[k]
                    result += cache[k]
                    continue
                
                if grid[v][y] == '^':
                    del beams[k]
                    beams[(v, y - 1)] = v
                    beams[(v, y + 1)] = v
                    cache[(v, y - 1)] += cache[k]
                    cache[(v, y + 1)] += cache[k]
                    
                    continue
                
                beams[k] = v
        
        return result


solver = Solver(40)
solver.solve()