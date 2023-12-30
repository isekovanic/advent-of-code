import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            line = line.strip()
            
            result += len(line) - len(str(eval(line)))

        return result


solver = Solver(12)
solver.solve()