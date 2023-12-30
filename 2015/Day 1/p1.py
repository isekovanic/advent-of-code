import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        instructions = problem_input[0]

        return sum([1 if x == '(' else -1 for x in instructions])


solver = Solver(3)
solver.solve()