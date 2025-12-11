import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

cache = {}
class Solver(SolverCore):
    def dfs(self, current, graph):
        if current in cache:
            return cache[current]
        
        if current == 'out':
            cache[current] = 1
            return 1
        
        neighbours = graph[current]
        result = 0
        
        for neighbour in neighbours:
            result += self.dfs(neighbour, graph)
        
        cache[current] = result
        
        return result
    def _solve(self, problem_input):
        graph = defaultdict(list)
        cache.clear()
        
        for line in problem_input:
            start, ends = line.split(':')
            
            for end in ends.strip().split():
                graph[start].append(end)
            
        return self.dfs('you', graph)


solver = Solver(5, { 'test': 'input_test_p1.txt' })
solver.solve()