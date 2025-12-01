import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        dial = 50
        
        for cmd in problem_input:
            direction, *rest = cmd
            value = int(''.join(rest))
            
            if direction == 'L':
                dial = (dial - value) % 100
            else:
                dial = (dial + value) % 100
                
            if dial == 0:
                result += 1
            
        return result

solver = Solver(3)
solver.solve()