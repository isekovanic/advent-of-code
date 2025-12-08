import sys
import math

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def euclidean_dist(self, p1, p2):
        return math.sqrt(sum((c2 - c1) ** 2 for c1, c2 in zip(p1, p2)))
    
    def connected_components(self, graph):
        visited = set([])
        components = []
        
        def dfs(start, component):
            stack = [start]
            visited.add(start)
            
            while stack:
                v = stack.pop()
                component.append(v)
                
                for w in graph[v]:
                    if w not in visited:
                        visited.add(w)
                        stack.append(w)
        
        for node in graph:
            if node not in visited:
                component = []
                dfs(node, component)
                components.append(component)
        
        return components
    def _solve(self, problem_input):
        points = [tuple([int(x) for x in line.split(',')]) for line in problem_input]
        connections = []
        
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1, p2 = points[i], points[j]
                connections.append((p1, p2, self.euclidean_dist(p1, p2)))
                
        graph = {}
        
        for point in points:
            graph[point] = [point]
            
        for edge in sorted(connections, key=lambda x: x[2]):
            p1, p2, _ = edge
            
            graph[p1].append(p2)
            graph[p2].append(p1)
            
            if len(self.connected_components(graph)) == 1:
                return p1[0] * p2[0]
        
        # no such solution, should not happen
        return -1


solver = Solver(25272)
solver.solve()