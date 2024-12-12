import sys

sys.path.append('../../')

from Core import SolverCore

# As per the instructions in this part, we increase the perimeter of the shape every time
# a point in it has a neighbour that is not the same value as the starting node. In other
# words, this roughly translates to finding the number of neighbours of each vertex in a
# connected component whose direct neighbours do not have the same value as the rest of
# the vertices in said connected component. The area is simply the number of vertices in
# it.
class Solver(SolverCore):
    def _solve(self, problem_input):
        grid = [list(x.strip()) for x in problem_input]
        
        dimx = len(grid)
        dimy = len(grid[0])
        
        visited = set([])
        result = 0
        
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                start = (i, j)
                
                if start in visited:
                    continue
                
                perimeter = 0
                area = 0
                queue = [start]
                
                while queue:
                    current = queue.pop()
                    ci, cj = current
                    
                    if current in visited:
                        continue
                    
                    visited.add(current)
                    area += 1
                    
                    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                        ni, nj = ci + dx, cj + dy
                        
                        if 0 <= ni < dimx and 0 <= nj < dimy and grid[ni][nj] == val:
                            queue.append((ni, nj))
                        else:
                            perimeter += 1
                    
                result += perimeter * area
        
        return result


solver = Solver(1930)
solver.solve()