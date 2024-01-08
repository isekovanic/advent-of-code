import sys
from hashlib import md5

sys.path.append('../../')

from Core import SolverCore

directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}
class Solver(SolverCore):
    def is_valid(self, point):
        x, y = point
        
        return 0 <= x < 4 and 0 <= y < 4
    def get_neighbours(self, password):
        md5_hash = md5(password.encode()).hexdigest()[:4]
        
        neighbours = []
        
        for idx, neighbour in enumerate(md5_hash):
            if neighbour in ['b', 'c', 'd', 'e', 'f']:
                neighbours.append('UDLR'[idx])
                
        return neighbours
    def _solve(self, problem_input):
        password = problem_input[0].strip()
        
        current_room = (0, 0)
        end = (3, 3)
        
        queue = [(current_room, '')]
        
        while queue:
            current_room, path = queue.pop(0)
            
            if current_room == end:
                return path
            
            current_password = password + path
            x, y = current_room
            
            for neighbour in self.get_neighbours(current_password):
                dx, dy = directions[neighbour]
                next_room = (x + dx, y + dy)
                
                if self.is_valid(next_room):
                    queue.append((next_room, path + neighbour))
                
        return -1


solver = Solver('DRURDRUDDLLDLUURRDULRLDUUDDDRR')
solver.solve()