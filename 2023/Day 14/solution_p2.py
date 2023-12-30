import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def move(self, grid):
		size = len(grid)
		# x-pose
		grid = list(map(list, zip(*grid)))
		result = 0
		for k, row in enumerate(grid):
			new_row = []
			block_loc = 0
			rocks = 0

			for i, item in enumerate(row):
				if item == '#':
					new_row += ['O'] * rocks + ['.'] * (i - block_loc - rocks) + ['#']

					block_loc = i + 1
					rocks = 0
				elif item == 'O':
					rocks += 1
			new_row += ['O'] * rocks + ['.'] * (i - block_loc + 1 - rocks)
			grid[k] = new_row

		# finish clockwise rotation, to account for the anti-clockwise side being always up
		return [row[::-1] for row in grid]

	def cycle(self, grid):
		for _ in range(4):
			grid = self.move(grid)

		return grid


	def _solve(self, problem_input):

		grid = [list(x.strip()) for x in problem_input]

		idx = 1
		visited = { str(grid): 0 }

		# working under the assumption that these cycles are bound to repeat

		while True:
			grid = self.cycle(grid)
			if str(grid) in visited.keys():
				break

			visited[str(grid)] = idx
			idx += 1

		cycle_start = visited[str(grid)]
		cycle_length = idx - cycle_start

		cycles = 1000000000

		last_grid_idx = (cycles - cycle_start) % cycle_length + cycle_start
		last_grid = None

		for key, val in visited.items():
			if val == last_grid_idx:
				last_grid = key
				break

		size = len(grid)

		return sum([row.count('O') * (size - i) for i, row in enumerate(eval(last_grid))])

solver = Solver(64)
solver.solve()