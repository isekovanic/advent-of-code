import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def calculate_weight(self, size, min_col, rocks):
		t_size = size - min_col
		r_size = t_size - rocks
		# size + size - 1 + size - 2 + size - 3 = 3 * size - (3 * 4) // 2
		return t_size * (t_size + 1) // 2 - r_size * (r_size + 1) // 2

	def _solve(self, problem_input):

		size = len(problem_input)

		grid = list(map(list, zip(*[list(x.strip()) for x in problem_input])))

		result = 0
		for row in grid:
			min_col = 0
			rocks = 0

			for i, item in enumerate(row):
				if item == '#':
					result += self.calculate_weight(size, min_col, rocks)

					min_col = i + 1
					rocks = 0 
				elif item == 'O':
					rocks += 1
			result += self.calculate_weight(size, min_col, rocks)

		return result

solver = Solver()
solver.solve()