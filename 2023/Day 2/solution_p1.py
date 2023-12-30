import sys

sys.path.append('../../')

from Core import SolverCore

# red, green, blue

max_cubes = [12, 13, 14]
cube_indices = ['red', 'green', 'blue']

class Solver(SolverCore):
	def check(self, cubes):
		for i in range(3):
			if max_cubes[i] < cubes[i]:
				return False
		return True

	def _solve(self, problem_input):

		result = 0

		for line in problem_input:
			game_id, games = line.split(':')
			game_id = int(game_id[5:])

			is_possible = True

			for game in games.split(';'):
				entries = game.split(',')

				curr_cubes = [0, 0, 0]

				for entry in entries:
					cnt, color = entry.split()

					curr_cubes[cube_indices.index(color)] += int(cnt)

					if not self.check(curr_cubes):
						is_possible = False

			if is_possible:
				result += game_id
		
		return result

solver = Solver(8)
solver.solve()