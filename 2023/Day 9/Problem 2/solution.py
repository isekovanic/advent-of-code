import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def calc_next_element(self, sequence):
		difference_sequences = []

		current = sequence

		while True:
			differences = [y - x for x, y in zip(current, current[1:])]
			difference_sequences += [differences]

			if all([x == 0 for x in differences]):
				break
			current = differences

		difference_sequences[-1] += [0]
		for i in range(len(difference_sequences) - 2, -1, -1):
			difference_sequences[i] += [difference_sequences[i][-1] + difference_sequences[i + 1][-1]]

		return difference_sequences[0][-1] + sequence[-1]


	def _solve(self, problem_input):
		result = 0

		for line in problem_input:
			sequence = [int(x) for x in line.split()][::-1]

			result += self.calc_next_element(sequence)

		return result

solver = Solver()
solver.solve()