import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):
		return 'Merry Christmas !'

solver = Solver()
solver.solve()