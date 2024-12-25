import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        keys = []
        locks = []
        
        max_height = len(problem_input[0])
        
        for schematic in problem_input:
            configuration = []
            for row in list(zip(*schematic)):
                configuration.append(row.count('#') - 1)
                
            configuration = tuple(configuration)
            if schematic[0] == len(schematic[0]) * '#':
                locks.append(configuration)
            else:
                keys.append(configuration)
        
        result = 0
        for key in keys:
            for lock in locks:
                result += all([x + y < max_height - 1 for x, y in zip(key, lock)])
            
        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(3)
solver.solve()