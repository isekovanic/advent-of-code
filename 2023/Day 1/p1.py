import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		result = 0

		for line in problem_input:
			digits = list(filter(lambda x: x.isdigit(), line))
			result += int('{}{}'.format(digits[0], digits[-1]))
		
		return result

solver = Solver(142, { 'test': 'input_test_p1.txt' })
solver.solve()