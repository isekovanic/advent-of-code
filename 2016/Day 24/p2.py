import sys
from itertools import permutations

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def is_valid(self, node, grid):
        x, y = node
        
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'
    
    def get_neighbours(self, node, grid):
        x, y = node
        neighbours = []
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            n_x, n_y = x + dx, y + dy
            
            if self.is_valid((n_x, n_y), grid):
                neighbours.append((n_x, n_y))
        
        return neighbours
    def _solve(self, problem_input):
        grid = []
        wire_indices = {}
        
        for i, line in enumerate(problem_input):
            row = []
            for j, char in enumerate(line.strip()):
                if char.isnumeric():
                    wire_indices[char] = (i, j)
                row.append(char)
            grid.append(row)
        
        distances = {}
        wires = list(wire_indices.keys())
        
        for node in wires:
            x, y = wire_indices[node]
            distances[node] = {}
            
            queue = [((x, y), 0)]
            visited = set([])
            
            while queue:
                current_node, steps = queue.pop(0)
                
                if current_node in visited:
                    continue
                visited.add(current_node)
                
                c_x, c_y = current_node
                val = grid[c_x][c_y]
                
                if val.isnumeric():
                    distances[node][val] = steps
                
                for neighbour in self.get_neighbours(current_node, grid):
                    queue.append((neighbour, steps + 1))
        
        result = sys.maxsize
        wires.pop(wires.index('0'))
        
        for permutation in permutations(wires):
            current_result = distances['0'][permutation[0]] + distances[permutation[-1]]['0']
            for s, e in zip(permutation, permutation[1:]):
                current_result += distances[s][e]
            
            result = min(current_result, result)
            
        return result


solver = Solver(20)
solver.solve()