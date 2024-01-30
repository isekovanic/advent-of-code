import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        stream = problem_input[0].strip()
        
        prev = '#'
        in_garbage = False
        result = 0
        
        for char in stream:
            if prev == '!':
                prev = '#'
                continue
            if in_garbage and char not in '!>':
                result += 1
            if char == '<':
                in_garbage = True
            if char == '>':
                in_garbage = False
            
            prev = char
            
        return result


solver = Solver(13)
solver.solve()