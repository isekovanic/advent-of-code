import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):
		nb_cards = len(problem_input)
		card_cnt = {}

		for i in range(nb_cards):
			card_cnt[i] = 1

		for idx, card in enumerate(problem_input):
			winning, inventory = map(lambda x: x.split(), card[7:].split(' | '))

			card_result = 0
			for item in inventory:
				card_result += item in winning

			for i in range(idx, idx + card_result):
				card_cnt[i + 1] += card_cnt[idx]

		return sum(card_cnt.values())

solver = Solver(30)
solver.solve()