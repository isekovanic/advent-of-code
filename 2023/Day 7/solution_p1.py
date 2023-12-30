import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
	def find_rank(self, cards):
		card_map = {}
		for char in cards:
			if char in card_map:
				card_map[char] += 1
			else:
				card_map[char] = 1

		nb_keys = len(card_map.keys())
		
		# 5 of a kind
		if nb_keys == 1:
			return 7

		if nb_keys == 2:
			# 4 of a kind
			if 4 in card_map.values():
				return 6
			# full house
			return 5
		if nb_keys == 3:
			# 3 of a kind
			if 3 in card_map.values():
				return 4
			# two pair
			return 3
		# 1 pair
		if nb_keys == 4:
			return 2

		# high card
		return 1

	def get_card_val(self, card):
		card_values = '0 1 2 3 4 5 6 7 8 9 T J Q K A'.split()

		return card_values.index(card)

	def _solve(self, problem_input):

		ranks = {}

		for hand in problem_input:
			cards, bid = hand.strip().split(' ')
			rank = self.find_rank(cards)

			card_bid_pair = (cards, int(bid))

			if rank in ranks:
				ranks[rank] += [card_bid_pair]
			else:
				ranks[rank] = [card_bid_pair]

		final = []
		for i in range(7):
			key = 7 - i
			if key not in ranks:
				continue

			mapped_rank = []

			for hand in ranks[key]:
				hand_list = [self.get_card_val(x) for x in list(hand[0])]

				mapped_rank += [(hand_list, hand[1])]

			sorted_rank = sorted(mapped_rank, key=lambda x: x[0])

			final = sorted_rank + final

		result = 0

		for i in range(len(final)):
			result += final[i][1] * (i + 1)

		return result

solver = Solver(6440)
solver.solve()