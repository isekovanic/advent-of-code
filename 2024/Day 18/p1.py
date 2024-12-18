import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        first_x = 1024
        # uncomment the next line for the test input
        # first_x = 12
        bytes = set([tuple([int(x) for x in line.split(',')]) for line in problem_input][:first_x])
        
        dimx, dimy = 71, 71
        # uncomment the next line for the test input
        # dimx, dimy = 7, 7
        
        queue = [(0, 0)]
        visited = set([])
        distances = { (0, 0): 0 }
        
        while queue:
            current = queue.pop(0)
            
            if current == (dimx - 1, dimy - 1):
                break
            
            if current in visited:
                continue
            
            visited.add(current)
            x, y = current
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < dimx and 0 <= ny < dimy and (nx, ny) not in visited and (nx, ny) not in bytes:
                    distances[(nx, ny)] = distances[(x, y)] + 1
                    queue.append((nx, ny))

        return distances[(dimx - 1, dimy - 1)]


solver = Solver(146)
solver.solve()