import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
	def calculate_hash(self, entry):
		current_result = 0
		for char in entry:
			current_result += ord(char)
			current_result *= 17
			current_result %= 256

		return current_result

	def _solve(self, problem_input):

		result = 0
		for entry in problem_input[0].strip().split(','):
			result += self.calculate_hash(entry)
		
		return result

solver = Solver(1320)
solver.solve()