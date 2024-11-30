import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

class Solver(SolverCore):
    def _solve(self, problem_input):
        connections = defaultdict(set)
        
        for line in problem_input:
            start, ends = line.strip().split(' <-> ')
            
            for end in ends.split(', '):
                connections[start].add(end)
                connections[end].add(start)
        
        groups = 0
        
        visited = set([])
        for start in connections:
            if start in visited:
                continue
            groups += 1
            queue = [start]
            
            while len(queue):
                current = queue.pop()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                for connection in connections[current]:
                    if connection not in visited:
                        queue.append(connection)

        return groups


solver = Solver(2)
solver.solve()