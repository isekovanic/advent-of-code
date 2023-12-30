import sys

sys.path.append('../../')

from Core import SolverCore

max_steps = 64

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

class Solver(SolverCore):
	def is_valid(self, point, grid):
		m, n = len(grid), len(grid[0])
		x, y = point

		return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'

	def _solve(self, problem_input):

		grid = [list(x.strip()) for x in problem_input]
		start = ()

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 'S':
					start = (i, j)

		queue = [(start, max_steps)]
		visited = set([])
		result = 0

		while queue:
			(x, y), steps = queue.pop(0)

			if (x, y) in visited:
				continue

			visited.add((x, y))

			if steps % 2 == 0:
				result += 1

			if steps == 0:
				continue

			for d_x, d_y in zip(dx, dy):
				neighbour = (x + d_x, y + d_y)
				if self.is_valid(neighbour, grid):
					queue += [(neighbour, steps - 1)]

		return result

solver = Solver(42, { 'test': 'input_test_p1.txt' })
solver.solve()