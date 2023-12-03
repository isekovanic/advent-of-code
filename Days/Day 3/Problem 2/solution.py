import sys
import re

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def get_adj_numbers(self, potential_gear_location, number_locations):
		adj_numbers = []
		gear_i, gear_j = potential_gear_location
		for number_location in number_locations.items():
			location, number = number_location

			if location[0] - 1 <= gear_i <= location[0] + 1 and location[1] - 1 <= gear_j <= location[1] + len(number):
				adj_numbers += [int(number)]

		return adj_numbers

	def _solve(self, problem_input):
		# engine row, index of item start
		number_locations = {}
		# symbols are always 1 character, no need for a map
		potential_gear_locations = set({})

		for row, line in enumerate(problem_input):
			numbers = re.findall('[0-9]+', line)

			consumed = 0
			for number in numbers:
				start = line[consumed:].index(number)
				number_locations[(row, start + consumed)] = number
				consumed += start + len(number)

			for col, char in enumerate(line.strip()):
				if char == '*':
					potential_gear_locations.add((row, col))

		result = 0
		for potential_gear in potential_gear_locations:
			adj_numbers = self.get_adj_numbers(potential_gear, number_locations)
			if len(adj_numbers) == 2:
				result += adj_numbers[0] * adj_numbers[1]
		
		return result

solver = Solver()
solver.solve()