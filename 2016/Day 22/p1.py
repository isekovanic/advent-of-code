import sys

sys.path.append('../../')

from Core import SolverCore

class Node:
    def __init__(self, name, size, used, available, use_percentage):
        size, used, available, use_percentage = [int(nb[:-1]) for nb in [size, used, available, use_percentage]]
        
        self.size = size
        self.used = used
        self.available = available
        self.use_percentage = use_percentage
        
        _, index_string = name.split('-x')
        self.name = tuple([int(x) for x in index_string.split('-y')])

class Solver(SolverCore):
    def _solve(self, problem_input):
        problem_input.pop(0)
        problem_input.pop(0)
        
        nodes = []
        
        for line in problem_input:
            name, size, used, available, use_percentage = list(filter(lambda x: len(x), line.strip().split(' ')))
            nodes.append(Node(name, size, used, available, use_percentage))
        
        result = 0
        
        for A in nodes:
            for B in nodes:
                if A.name != B.name and 0 < A.used <= B.available:
                    result += 1
        
        return result


solver = Solver(7)
solver.solve()