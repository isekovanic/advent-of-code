import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

cache = {}

class Solver(SolverCore):
    def dfs(self, current, graph):
        if current in cache:
            return cache[current]
        
        node, state = current
        
        if node == 'out':
            result = state == 3
            cache[current] = result
            return result
        
        neighbours = graph[node]
        result = 0
        
        new_state = state
        
        if node == 'dac':
            new_state |= 1 << 0
        
        if node == 'fft':
            new_state |= 1 << 1
        
        for neighbour in neighbours:
            result += self.dfs((neighbour, new_state), graph)
        
        cache[current] = result
        
        return result
    def _solve(self, problem_input):
        graph = defaultdict(list)
        cache.clear()
        
        for line in problem_input:
            start, ends = line.split(':')
            
            for end in ends.strip().split():
                graph[start].append(end)
            
        return self.dfs(('svr', 0), graph)


solver = Solver(2, { 'test': 'input_test_p2.txt' })
solver.solve()