import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		result = 0

		for card in problem_input:
			winning, inventory = map(lambda x: x.split(), card[7:].split(' | '))

			card_result = 0
			for item in inventory:
				card_result += item in winning

			result += 2 ** (card_result - 1) if card_result else 0

		return int(result)

solver = Solver()
solver.solve()