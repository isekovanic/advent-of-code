import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
	def move(self, point, direction, length):
		x, y = point

		if direction == 'R':
			return (x, y + length)
		if direction == 'D':
			return (x + length, y)
		if direction == 'L':
			return (x, y - length)
		return (x - length, y)

	def shoelace_formula(self, points):
		area = 0
		perimeter = 0

		for p1, p2 in zip(points, points[1:] + [points[0]]):
			x1, y1 = p1
			x2, y2 = p2

			perimeter += abs(x1 - x2) + abs(y1 - y2)

			area += x1 * y2 - x2 * y1

		# Due to the way the trenches are structured, the standard shoelace formula is not
		# going to work. Since it works for catresian coordinates, only 1 half of the trenches
		# is going to be counted towards the final area (since the other half comes cyclically back),
		# but is considered a "line" in terms of the shoelace theorem). Hence, we add half of the perimeter
		# + 1 for the last operation, since the start node is not counter otherwise.
		return abs(area) / 2 + perimeter / 2 + 1

	def _solve(self, problem_input):

		current = (0, 0)
		vertices = [current]

		for instruction in problem_input:
			direction, length, _ = instruction.split()
			length = int(length)
			current = self.move(current, direction, length)

			vertices += [current]

		# technically not needed since we anyway always start at (0, 0),
		# but added here just for consistency in terms of the theorem.
		vertices.pop()
		
		return int(self.shoelace_formula(vertices))

solver = Solver(62)
solver.solve()