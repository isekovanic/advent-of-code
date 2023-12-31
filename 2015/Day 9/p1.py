import sys
from itertools import permutations

sys.path.append('../../')

from Core import SolverCore

# Typical Travelling Salesman problem. Since the number of vertices is really small,
# we can simply generate all possible routes and find the smallest one.
class Solver(SolverCore):
    def _solve(self, problem_input):
        graph = {}
        
        for line in problem_input:
            edge, weight = line.split(' = ')
            weight = int(weight)
            start, end = edge.split(' to ')
            
            if start not in graph:
                graph[start] = {}
            if end not in graph:
                graph[end] = {}
            
            graph[start][end] = weight
            graph[end][start] = weight
        
        result = sys.maxsize
        
        paths = list(permutations(list(graph.keys())))
        
        for path in paths:
            distance = 0
            prev_node = path[0]
            for node in path[1:]:
                distance += graph[prev_node][node]
                prev_node = node
            
            result = min(result, distance)
            
        return result


solver = Solver(605)
solver.solve()