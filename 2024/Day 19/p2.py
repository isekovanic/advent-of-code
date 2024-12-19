import sys

sys.path.append('../../')

from Core import SolverCore

cache = {}
class Solver(SolverCore):
    def count_valid_combinations(self, design, patterns):
        global cache
        
        if len(design) == 0:
            return 1
        
        if design in cache:
            return cache[design]
        
        cache[design] = 0
        for pattern in patterns:
            if design.startswith(pattern):
                cache[design] += self.count_valid_combinations(design[len(pattern):], patterns)
                
        return cache[design]
    def _solve(self, problem_input):
        global cache
        patterns = problem_input[0][0].split(', ')
        designs = [x.strip() for x in problem_input[1]]
        cache = {}
        
        return sum([self.count_valid_combinations(design, patterns) for design in designs])
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(6)
solver.solve()