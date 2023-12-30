import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        instructions = problem_input[0]
        
        result = 0
        
        for idx, instruction in enumerate(instructions):
            result += 1 if instruction == '(' else -1
            
            if result < 0:
                return idx + 1
            
        return -1


solver = Solver(1)
solver.solve()