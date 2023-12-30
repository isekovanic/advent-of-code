import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            line = line.strip()
            
            result += line.count('\\') + line.count('"') + 2

        return result


solver = Solver(19)
solver.solve()