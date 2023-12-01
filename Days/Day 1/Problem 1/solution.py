import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		result = 0

		for line in problem_input:
			digits = list(filter(lambda x: x.isdigit(), line))
			result += int('{}{}'.format(digits[0], digits[-1]))
		
		return result

solver = Solver()
solver.solve()