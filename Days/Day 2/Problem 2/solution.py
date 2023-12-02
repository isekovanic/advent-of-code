import sys
from functools import reduce

sys.path.append('../../../Core')

from SolverCore import SolverCore

cube_indices = ['red', 'green', 'blue']

class Solver(SolverCore):
	def _solve(self, problem_input):

		result = 0

		for line in problem_input:
			game_id, games = line.split(':')
			game_id = int(game_id[5:])

			min_cubes = [0, 0, 0]

			for game in games.split(';'):
				entries = game.split(',')

				for entry in entries:
					cnt, color = entry.split()

					cube_idx = cube_indices.index(color)
					min_cubes[cube_idx] = max(min_cubes[cube_idx], int(cnt))

			power = reduce(lambda x, y: x * y, min_cubes)

			result += power
		
		return result

solver = Solver()
solver.solve()