import sys

sys.path.append('../../')

from Core import SolverCore

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
class Solver(SolverCore):
    def is_valid(self, point, favourite_number):
        x, y = point
        
        magic_number = x * x + 3 * x + 2 * x * y + y + y * y + favourite_number
        
        binary = bin(magic_number)
        
        if binary.count('1') % 2 == 0 and x >= 0 and y >= 0:
            return True
        return False
    
    def get_neighbours(self, point, favourite_number):
        x, y = point
        neighbours = []
        
        for d_x, d_y in zip(dx, dy):
            neighbour = (x + d_x, y + d_y)
            
            if self.is_valid(neighbour, favourite_number):
                neighbours.append(neighbour)
        
        return neighbours
    def _solve(self, problem_input):
        favourite_number = int(problem_input[0].strip())
        end = (31, 39)
        # end = (7, 4) # uncomment for test input
        
        queue = [((1, 1), 0)]
        visited = set([])
        
        while queue:
            current_point, steps = queue.pop(0)
            
            if current_point == end:
                return steps
            
            if current_point in visited:
                continue
            visited.add(current_point)
            
            for neighbour in self.get_neighbours(current_point, favourite_number):
                queue.append((neighbour, steps + 1))
            
        return -1


solver = Solver(-1)
solver.solve()