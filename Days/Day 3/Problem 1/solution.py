import sys
import re

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def is_part_number(self, number_location, symbols):
		location, number = number_location
		for sym_i, sym_j in symbols:
			if location[0] - 1 <= sym_i <= location[0] + 1 and location[1] - 1 <= sym_j <= location[1] + len(number):
				return True

		return False

	def _solve(self, problem_input):
		# engine row, index of item start
		number_locations = {}
		# symbols are always 1 character, no need for a map
		symbol_locations = set({})

		for row, line in enumerate(problem_input):
			numbers = re.findall('[0-9]+', line)

			consumed = 0
			for number in numbers:
				start = line[consumed:].index(number)
				number_locations[(row, start + consumed)] = number
				consumed += start + len(number)

			for col, char in enumerate(line.strip()):
				if not (char.isdigit() or char == '.'):
					symbol_locations.add((row, col))

		result = 0
		for number_location in number_locations.items():
			if self.is_part_number(number_location, symbol_locations):
				result += int(number_location[1])
		
		return result

solver = Solver()
solver.solve()