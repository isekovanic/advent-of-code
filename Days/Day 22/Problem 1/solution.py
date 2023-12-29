import sys

sys.path.append('../../../')

from Core import SolverCore

class Cube:
	def __init__(self, name, ix, iy, iz):
		self.name = name # purely for debugging and cross-checking purposes, technically not needed

		self.ix = ix
		self.iy = iy
		self.iz = iz

		self.supported_by = []
		self.has_fallen = False

	def are_overlapping(self, r1, r2):
		start1, end1 = r1
		start2, end2 = r2

		return not (end1 < start2 or end2 < start1)

	def cubes_overlap(self, cube):
		if cube.iz[1] >= self.iz[0]:
			return False

		x_overlaps = self.are_overlapping(self.ix, cube.ix)
		y_overlaps = self.are_overlapping(self.iy, cube.iy)

		return x_overlaps and y_overlaps

	def fall(self, falling_cubes):
		cubes = list(filter(lambda x: x.has_fallen, falling_cubes))
		max_height = 0
		for cube in cubes:
			if cube != self and self.cubes_overlap(cube):
				max_height = max(max_height, cube.iz[1])

		for cube in cubes:
			if self.cubes_overlap(cube) and cube.iz[1] == max_height:
				self.supported_by += [cube]

		height = self.iz[1] - self.iz[0]

		self.iz = (max_height + 1, max_height + 1 + height)

		self.has_fallen = True

	def __repr__(self):
		return '{}, ix={}, iy={}, iz={}, supported_by={}'.format(self.name, self.ix, self.iy, self.iz, [c.name for c in self.supported_by])

class Solver(SolverCore):
	def _solve(self, problem_input):

		cubes = []

		for idx, line in enumerate(problem_input):
			[sx, sy, sz], [ex, ey, ez] = [[int(x) for x in coords.split(',')] for coords in line.split('~')]

			cubes += [Cube(idx, (sx, ex), (sy, ey), (sz, ez))]

		for cube in sorted(cubes, key=lambda x: x.iz[0]):
			cube.fall(cubes)

		cannot_disintegrate = set([])
		for cube in cubes:
			if len(cube.supported_by) == 1:
				cannot_disintegrate.add(cube.supported_by[0])
		
		return len(cubes) - len(cannot_disintegrate)

solver = Solver()
solver.solve()