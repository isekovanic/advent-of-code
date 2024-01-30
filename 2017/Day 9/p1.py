import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        stream = problem_input[0].strip()
        
        depth = 0
        prev = '#'
        in_garbage = False
        result = 0
        
        for char in stream:
            if prev == '!':
                prev = '#'
                continue
            if not in_garbage:
                if char == '{':
                    depth += 1
                if char == '}':
                    result += depth
                    depth = max(depth - 1, 0)
            if char == '<':
                in_garbage = True
            if char == '>':
                in_garbage = False
            
            prev = char
            
        return result


solver = Solver(3)
solver.solve()