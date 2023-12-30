import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		space = [[1 if y == '#' else 0 for y in x] for x in problem_input]

		rows_to_expand = []
		cols_to_expand = []

		for i in range(len(space)):
			if sum(space[i]) == 0:
				rows_to_expand += [i]

		x_posed_space = list(map(list, zip(*space)))

		for i in range(len(x_posed_space)):
			if sum(x_posed_space[i]) == 0:
				cols_to_expand += [i]

		galaxy_coords = []
		for i in range(len(space)):
			for j in range(len(space[i])):
				if space[i][j]:
					galaxy_coords += [(i, j)]

		result = 0

		for i in range(len(galaxy_coords)):
			for j in range(i + 1, len(galaxy_coords)):
				x1, y1 = galaxy_coords[i]
				x2, y2 = galaxy_coords[j]
				extra_rows = 0
				extra_cols = 0
				for r in rows_to_expand:
					extra_rows += min(x1, x2) < r < max(x1, x2)
				for c in cols_to_expand:
					extra_cols += min(y1, y2) < c < max(y1, y2)

				result += abs(y2 - y1) + abs(x2 - x1) + extra_cols + extra_rows

		return result

solver = Solver(374)
solver.solve()