import sys

sys.path.append('../../')

from Core import SolverCore

# Directions:
# 1 - up
# 2 - right
# 3 - down
# 4 - left

directions_map = {
	1: (-1, 0),
	2: (0, 1),
	3: (1, 0),
	4: (0, -1)
}

class Solver(SolverCore):
	def is_valid(self, pos, grid):
		x, y = pos

		return 0 <= x < len(grid) and 0 <= y < len(grid[0])

	def spawn_beams(self, beam, mirror):
		x, y, direction = beam

		if mirror == '-':
			if direction == 1 or direction == 3:
				return [(x, y + 1, 2), (x, y - 1, 4)]
			return [(x, y + (1 if direction == 2 else -1), direction)]

		if mirror == '|':
			if direction == 2 or direction == 4:
				return [(x - 1, y, 1), (x + 1, y, 3)]
			return [(x + (1 if direction == 3 else -1), y, direction)]

		if mirror == '/':
			if direction == 1:
				return [(x, y + 1, 2)]
			if direction == 2:
				return [(x - 1, y, 1)]
			if direction == 3:
				return [(x, y - 1, 4)]
			return [(x + 1, y, 3)]

		if mirror == '\\':
			if direction == 1:
				return [(x, y - 1, 4)]
			if direction == 2:
				return [(x + 1, y, 3)]
			if direction == 3:
				return [(x, y + 1, 2)]
			return [(x - 1, y, 1)]

		# not a mirror, has gone out of bounds so breaking the cycle
		return []

	def _solve(self, problem_input):

		grid = [list(x.strip()) for x in problem_input]

		# containing (x, y, z) where:
		# x - starting x position
		# y - starting y position
		# z - direction
		beam_queue = [(0, 0, 2)]
		energized = set([])
		visited = set([])

		while len(beam_queue):
			beam = beam_queue.pop(0)
			x, y, direction = beam
			if (x, y, direction) in visited:
				continue

			while self.is_valid((x, y), grid) and grid[x][y] == '.':
				energized.add((x, y))
				visited.add((x, y, direction))
				dx, dy = directions_map[direction]
				x += dx
				y += dy

			if self.is_valid((x, y), grid):
				beam_queue += self.spawn_beams((x, y, direction), grid[x][y])
				energized.add((x, y))
				visited.add((x, y, direction))
		
		return len(energized)

solver = Solver(46)
solver.solve()