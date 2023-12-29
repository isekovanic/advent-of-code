import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def count_differences(self, p1, p2):
		differences = 0
		for s1, s2 in zip(p1, p2):
			differences += sum(1 for a, b in zip(s1, s2) if a != b)

		return differences

	def check(self, pattern):
		size = len(pattern)
		largest_reflection = (-1, 0) # index, size
		for i in range(size):
			f = []
			s = []
			if i <= size - i:
				f = pattern[:i]
				s = pattern[i:i + len(f)]
			else:
				s = pattern[i:]
				f = pattern[i - len(s):i]

			differences = self.count_differences(f, s[::-1])

			if differences == 1 and largest_reflection[1] <= len(f) and len(f) > 0:
				largest_reflection = (i, len(f))

		return largest_reflection

	def _solve(self, problem_input):
		result = 0

		for block in problem_input:
			pattern = [x for x in block.split('\n')]

			horizontal = self.check(pattern)
			vertical = self.check(list(map(list, zip(*pattern))))

			if horizontal[1] > vertical[1]:
				result += 100 * horizontal[0]
			else:
				result += vertical[0]

		return result

	def read_input(self, file):
		read_input = open(file, 'r')
		input_list = []

		for line in read_input.read().split('\n\n'):
			input_list += [line]

		return input_list

solver = Solver()
solver.solve()