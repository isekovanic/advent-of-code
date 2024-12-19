import sys

sys.path.append('../../')

from Core import SolverCore

cache = {}
class Solver(SolverCore):
    def check_if_valid_design(self, design, patterns):
        global cache
        
        if len(design) == 0:
            return True
        
        if design in cache:
            return cache[design]

        cache[design] = False
        for pattern in patterns:
            if design.startswith(pattern) and self.check_if_valid_design(design[len(pattern):], patterns):
                cache[design] = True
                break
                
        return cache[design]
    def _solve(self, problem_input):
        global cache
        patterns = problem_input[0][0].split(', ')
        designs = [x.strip() for x in problem_input[1]]
        cache = {}
        
        return sum([self.check_if_valid_design(design, patterns) for design in designs])
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(6)
solver.solve()