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
                adder = dial != 0
                dial -= value
                if dial <= 0:
                    result += abs(dial) // 100 + adder
                dial %= 100
            else:
                dial += value
                result += dial // 100
                dial %= 100
            
        return result


solver = Solver(6)
solver.solve()