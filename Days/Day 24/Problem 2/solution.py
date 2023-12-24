import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

# In this solution we are going to:
# - Skip most of the logic we had in Problem 1 and instead focus on several observations
# - We do not have to (nor can we, as far as I know) explicitly find a solution for each line that intersects
#	all of the other lines; but instead, we can do this axis by axis. This is because the axes do not need
#	to work together, but rather each axis coordinate needs to satisfy specific conditions
# - The X axis position of any rock at any given moment in time is x + vx * t, where t is the moment in time. We essentially
#	want to make sure that rock_x + rock_vx * t = x + vx * t for every single hailstone. Of course, the t does not (nor
#	will it) be the same unless we destroy 2 hailstones in one of their intersection points, but it doesn't matter.
# - We can apply the above rule for all 3 coordinates separately and we "simply" need to find a solution which satisfies
#	all 3 equations for a fixed t, for every single hailstone
# - With the equations above, we would have 3 variables (rock_x, rock_vx and t) which makes things a bit more difficult - so let's simplify a bit;
#	we can rewrite the example equation above as t * (rock_vx - vx) = x - rock_x <=> t = (x - rock_x) / (rock_vx - vx).
# - This equation is going to be valid for every single axis, so we'd have something like the following:
#	t = (x - rock_x) / (rock_vx - vx) = (y - rock_y) / (rock_vy - vy) = (z - rock_z) / (rock_vz - vz)
# - This, in turn, allows us to get rid of t and only solve for each pair of equalities as mentioned above. We would still
#	have a ton of equations, but one less variable this way so it makes the solution much easier (although still hard).
# - Let us take one pair of equations and examine it, for example: (x - rock_x) / (rock_vx - vx) = (y - rock_y) / (rock_vy - vy).
#	Trying to put all variables on one side, we would get something like: (x - rock_x) * (rock_vy - vy) = (y - rock_y) * (rock_vx - vx) <=>
#	<=> x * rock_vy - x * vy - rock_x * rock_vy + rock_x * vy = y * rock_vx - y * vx - rock_y * rock_vx + rock_y * vx <=>
#	<=> x * rock_vy - rock_x * rock_vy + rock_x * vy - y * rock_vx + rock_y * rock_vx - rock_y * vx = x * vy - y * vx. Now
#	at this point, let's notice something - we have an equation that is not linear. This happens because of the fact that
#	we have components of it that consist of 2 multiplied variables, meaning crafting a solution is going to be difficult.
#	Here's the catch though, both of these components have no constant before them (or we can say they're multiplied by a
#	constant that equals 1). This means, that if we generate 2 of these equations by subtracting one from the other we would
#	get a linear equation with 4 variables. Here is roughly what that would look like:
#	x1 * rock_vy - rock_x * rock_vy + rock_x * vy1 - y1 * rock_vx + rock_y * rock_vx - rock_y * vx1 
#	- x2 * rock_vy + rock_x * rock_vy - rock_x * vy2 + y2 * rock_vx - rock_y * rock_vx + rock_y * vx2 
#	= x1 * vy1 - y1 * vx1 - x2 * vy2 + y2 * vx2 <=> 
#	<=> (x1 - x2) * rock_vy + rock_x * (vy1 - vy2) - (y1 - y2) * rock_vx - rock_y * (vx1 - vx2) = x1 * vy1 - y1 * vx1 - x2 * vy2 + y2 * vx2
# - Since we have a ton of these equations (and the example test case also subtly hints at this since it has 5 points), it
#	turns out we can craft 4 different of these equations very easily (by doing for example hailstone 1 with hailstone 2, then hailstone 1 with
#	hailstone 3 etc.), giving us a system of 4 linear equations with 4 variables. This is something that we can solve and we
#	can do it for every axis (the example only explains the solution for the x-axis). In the end, we should have a solution 
#	satisfying all of the rules (we should only really need 4 hailstones to do this). The solution below should have a 
#	sufficient number of comments to guide you through the process. 
# - Ironically, as difficult as it was to figure this out the solution works super fast (unlike Day 23 :'( )

class Solver(SolverCore):
	# Return the minor of the matrix after removing the specified row and column.
	def minor(self, matrix, row, col):
		return [[matrix[i][j] for j in range(len(matrix[i])) if j != col] for i in range(len(matrix)) if i != row]

	# Calculate the determinant of a matrix using Laplace expansion.
	def determinant(self, matrix):
		size = len(matrix)

		# Base case: 2x2 matrix
		if size == 2:
			return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

		det = 0
		for col in range(size):
			sign = (-1) ** col
			det += sign * matrix[0][col] * self.determinant(self.minor(matrix, 0, col))

		return det

	# Solve the system of equations represented through coefficients A and constants B using Cramer's method.
	def cramer_method(self, A, B):
		n = len(A)
		det_A = self.determinant(A)

		if det_A == 0:
			raise ValueError('No solutions found. Something\'s probably wrong with the system of equations.')

		X = []
		for i in range(n):
			Ai = [row[:] for row in A]
			for j in range(n):
				Ai[j][i] = B[j]

			det_Ai = self.determinant(Ai)
			X.append(det_Ai / det_A)

		return X

	def form_equation(self, h1, h2):
		x1, y1, vx1, vy1 = h1
		x2, y2, vx2, vy2 = h2

		coefficients = [x1 - x2, vy1 - vy2, y2 - y1, vx2 - vx1]
		constant = x1 * vy1 - y1 * vx1 - x2 * vy2 + y2 * vx2

		return (coefficients, constant)

	def _solve(self, problem_input):

		hailstones = []

		for hailstone in problem_input:
			[x, y, z], [vx, vy, vz] = [[int(p) for p in x.split(',')] for x in hailstone.strip().split('@')]

			hailstones += [((x, y, z), (vx, vy, vz))]

		xy_equations = []
		xy_constants = []

		yz_equations = []
		yz_constants = []

		xz_equations = []
		xz_constants = []

		# Don't need more than 4 to solve the system, so keeping only the first 4.
		for h1, h2 in zip(hailstones[:5], hailstones[1:5]):
			(x1, y1, z1), (vx1, vy1, vz1) = h1
			(x2, y2, z2), (vx2, vy2, vz2) = h2

			xy_eq, xy_const = self.form_equation((x1, y1, vx1, vy1), (x2, y2, vx2, vy2))
			yz_eq, yz_const = self.form_equation((y1, z1, vy1, vz1), (y2, z2, vy2, vz2))
			xz_eq, xz_const = self.form_equation((x1, z1, vx1, vz1), (x2, z2, vx2, vz2))

			xy_equations += [xy_eq]
			yz_equations += [yz_eq]
			xz_equations += [xz_eq]

			xy_constants += [xy_const]
			yz_constants += [yz_const]
			xz_constants += [xz_const]

		xy_vy, xy_x, xy_vx, xy_y = self.cramer_method(xy_equations, xy_constants)
		yz_vz, yz_y, yz_vy, yz_z = self.cramer_method(yz_equations, yz_constants)
		xz_vz, xz_x, xz_vx, xz_z = self.cramer_method(xz_equations, xz_constants)

		# This part's pure paranoia that the solution is not correct in some cases. Left 
		# these here in case there is indeed some combination of the points for which this 
		# does not work well.

		x = 0
		if xy_x == xz_x:
			x = xy_x
		else:
			raise ValueError('The values for the solution for x do not match.')

		y = 0
		if xy_y == yz_y:
			y = xy_y
		else:
			raise ValueError('The values for the solution for y do not match.')

		z = 0
		if xz_z == yz_z:
			z = xz_z
		else:
			raise ValueError('The values for the solution for z do not match.')

		# casting just to get rid of the decimal representation, this will always be an integer
		return int(x + y + z)

solver = Solver()
solver.solve()