import sys

sys.path.append('../../../')

from Core import SolverCore

# Brief explanation of the idea:
# We will try to form lines for every every hailstone's trajectory, resulting in a line equation.
# For every pair of lines, we will check if:
# - They intersect at all (otherwise they're parallel and will never intersect)
# - Their intersection point is within the boundaries

# Forms a line equation, given 2 points in a 2D plane

class Line:
	def __init__(self, p1, p2):
		x1, y1 = p1
		x2, y2 = p2

		vx = x2 - x1
		vy = y2 - y1

		# y = slope * x + y_intercept (line equation in the y-intercept form)
		# We will represent our lines in a standard form: a * x + b * y = c

		self.a = -(y2 - y1)
		self.b = (x2 - x1)

		# plug in the first point to find y_intercept (or c in our standard form)

		self.c = self.b * y1 + self.a * x1
		self.start_point = p1
		self.starting_velocity = (vx, vy)

	def is_intersection_valid(self, line, intersection):
		x, y = intersection

		if x < line.start_point[0] and line.starting_velocity[0] > 0:
			return False
		if x > line.start_point[0] and line.starting_velocity[0] < 0:
			return False
		if y < line.start_point[1] and line.starting_velocity[1] > 0:
			return False
		if y > line.start_point[1] and line.starting_velocity[1] < 0:
			return False
		return True

	def intersection_with(self, line):
		determinant = self.a * line.b - line.a * self.b

		if determinant == 0:
			# no point of intersections, the lines are parallel
			return None
		else:
			# an intersection exists, return its coordinates
			x = (line.b * self.c - self.b * line.c) / determinant
			y = (self.a * line.c - line.a * self.c) / determinant

			intersection = (x, y)

			if self.is_intersection_valid(self, intersection) and self.is_intersection_valid(line, intersection):
				return intersection

			return None

	def __repr__(self):
		return 'a={}, b={}, c={}'.format(self.a, self.b, self.c)

class Solver(SolverCore):
	def _solve(self, problem_input):

		lines = []

		# space = (7, 27) # test input
		space = (200000000000000, 400000000000000) # actual input

		for hailstone in problem_input:
			[x, y, z], [vx, vy, vz] = [[int(p) for p in x.split(',')] for x in hailstone.strip().split('@')]

			# form lines by calculating an extra point for each hailstone

			p1 = (x, y)
			p2 = (x + vx, y + vy)

			lines += [Line(p1, p2)]

		result = 0

		for i in range(len(lines)):
			for j in range(i + 1, len(lines)):
				intersection_point = lines[i].intersection_with(lines[j])

				if intersection_point != None and space[0] <= intersection_point[0] <= space[1] and space[0] <= intersection_point[1] <= space[1]:
					result += 1
		
		return result

solver = Solver(0)
solver.solve()