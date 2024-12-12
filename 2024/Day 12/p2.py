import sys

sys.path.append('../../')

from Core import SolverCore

# Firstly, let us make an observation that the number of sides in a polygon is equal to the
# number of corners of said polygon. A corner could be defined as a turn whenever we move
# across the exact sides of the polygon (in our case we turn by 90 degrees). Essentially,
# what we need to do is find all of these corners and we should have the answer easily.
# Since the polygons' sides are only vertical or horizontal (according to the problem statement),
# we can define what a corner means in this context. Another observation that we can make
# is the fact that the corners can be convex or concave.
# For the concave corners, we have the following variations (using A for illustration purposes):
#
# BBB
# BAA
# BAA
#
# BBB
# AAB
# AAB
#
# BAA
# BAA
# BBB
#
# AAB
# AAB
# BBB
#
# We can notice in this instance that a corner can be derived as the instance of a vertex having
# it's neighbouring vertical and horizontal sides NOT be the same value as the connected component
# value of the polygon it forms. So, if the neighbours to the bottom-left, top-left, top-right and
# bottom-right are BOTH different from the connected component, we can safely assume that this is a
# corner.
# The convex use-case on the other hand can also be derived from the above observation. If we think
# about it, a convex corner essentially means that another polygon (or unified polygons) form a concave
# corner on the other side of it. This basically means that we need the bottom-left, top-left, top-right
# and bottom-right need to BOTH be the same value as the value in the connected component, AND also
# the adequate diagonal neighbour on the respective sides needs to strictly be different. Using these
# 2 clauses, we can find all of the corners easily.
# PS: Calling it right now that one of the later days is going to be this same thing but in multiple
#     dimensions :^)


# these have to be clockwise
deltas = [(1, 0), (0, -1), (-1, 0), (0, 1)]
class Solver(SolverCore):
    def _solve(self, problem_input):
        # since we'd have to do many clamping checks, it's better to fill the outer
        # edges of the grid with some random character that we know will not appear
        # in the problem input and work in the inner content of it.
        grid = [['.'] + list(x.strip()) + ['.'] for x in problem_input]
        empty_row = ['.' for _ in range(len(grid[0]))]
        grid = [empty_row] + grid + [empty_row]
        
        dimx = len(grid)
        dimy = len(grid[0])
        
        visited = set([])
        result = 0

        for i, row in enumerate(grid[1:dimx - 1]):
            for j, val in enumerate(row[1:dimy - 1]):
                start = (i + 1, j + 1)
                
                if start in visited:
                    continue
                    
                area = 0
                corners = 0
                queue = [start]
                
                while queue:
                    current = queue.pop()
                    ci, cj = current
                    
                    if current in visited:
                        continue
                    
                    visited.add(current)
                    area += 1
                    
                    # first, we append all valid neighbours to the queue
                    for dx, dy in deltas:
                        ni, nj = ci + dx, cj + dy
                        
                        if grid[ni][nj] == val:
                            queue.append((ni, nj))
                    
                    for c in range(4):
                        # We take each pair of deltas (carefully arranged in a clockwise manner) so
                        # that we can easily look through all of the concave corners. The convex corners
                        # are the non-zero values of those same deltas for each coordinate.
                        f, s = deltas[c], deltas[(c + 1) % 4]
                        
                        # concave corners
                        
                        fi, fj = f
                        si, sj = s
                        
                        if grid[ci + fi][cj + fj] != val and grid[ci + si][cj + sj] != val:
                            corners += 1
                        
                        # convex corners, diagonals
                        
                        ddi = fi if fi != 0 else si
                        ddj = fj if fj != 0 else sj
                        
                        if grid[ci + fi][cj + fj] == grid[ci + si][cj + sj] == val and grid[ci + ddi][cj + ddj] != val:
                            corners += 1
         
                result += corners * area
        
        return result


solver = Solver(1206)
solver.solve()