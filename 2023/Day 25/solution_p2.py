import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):
		return 'Merry Christmas !'

solver = Solver('Merry Christmas !')
solver.solve()