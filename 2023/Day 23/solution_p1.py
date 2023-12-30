import sys

sys.path.append('../../../')

from Core import SolverCore

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

class Solver(SolverCore):
	def is_valid(self, point, grid):
		x, y = point

		return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

	def _solve(self, problem_input):

		grid = [list(x.strip()) for x in problem_input]

		start = ()
		visited = set([])

		for i in range(len(grid[0])):
			if grid[0][i] == '.':
				start = (0, i)
				break

		# the state is (current_node, path_length)
		stack = [(start, set([]))]
		result = 0

		while stack:
			current_node, path = stack.pop()

			if current_node[0] == len(grid) - 1:
				result = max(result, len(path))
				continue

			x, y = current_node
			val = grid[x][y]

			potential_neighbours = []

			if val == '.':
				for d_x, d_y in zip(dx, dy):
					neighbour = (x + d_x, y + d_y)

					if self.is_valid(neighbour, grid):
						potential_neighbours += [neighbour]
			else:
				if val == '>':
					potential_neighbours += [(x, y + 1)]
				elif val == '<':
					potential_neighbours += [(x, y - 1)]
				elif val == 'v':
					potential_neighbours += [(x + 1, y)]
				else:
					potential_neighbours += [(x - 1, y)]

			for p_n in potential_neighbours:
				if p_n not in path:
					new_path = path.copy()
					new_path.add(current_node)
					stack += [(p_n, new_path)]
		
		return result

solver = Solver(94)
solver.solve()