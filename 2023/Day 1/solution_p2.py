import sys

sys.path.append('../../')

from Core import SolverCore

digits = {
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9,
}

class Solver(SolverCore):
	def _solve(self, problem_input):

		result = 0

		for line in problem_input:
			filtered_digits = []

			for i in range(len(line)):
				char = line[i]
				if char.isdigit():
					filtered_digits += [int(char)]
				else:
					matching_digits = [digit for digit in digits.keys() if line.startswith(digit, i)]
					if len(matching_digits) > 0:
						val = digits[matching_digits[0]]
						filtered_digits += [val]

			result += int('{}{}'.format(filtered_digits[0], filtered_digits[-1]))
		
		return result

solver = Solver(281, { 'test': 'input_test_p2.txt' })
solver.solve()