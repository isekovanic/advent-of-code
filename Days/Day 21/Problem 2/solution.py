import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

max_steps = 26501365

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

# Detective day once again. Let's make the following observations:
# - The distance to each border of the grid itself is the same for all directions. This is kind
#	of crucial for the solution since otherwise we would need to keep track how many steps it
#	takes for each pair of sides to another (they would not be conjunctive) and we would definitely
#	not be able to figure out how to calculate each inwards grid. Or at the very list I can't think
#	of a generalized way to do it.
# - The grid is always MxM; while this is not a crucial observation, it does help a bit when calculating
#	the movement. If it weren't the case, we would need to calculate the number of steps going up/down and the
#	number of steps going right/left and adjust accordingly (the final steps would be different depending on
#	the edge we're currently viewing). Since I noticed this I decided to stick to it, but it is easily fixable.
# - The test input is modified to account for these assumptions, as is the case with the main input.

class Solver(SolverCore):
	def is_valid(self, point, grid):
		m, n = len(grid), len(grid[0])
		x, y = point

		return 0 <= x < m and 0 <= y < n and grid[x][y] != '#'

	def bfs(self, start, steps, grid):
		queue = [(start, steps)]
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


	def _solve(self, problem_input):

		grid = [list(x.strip()) for x in problem_input]
		start = ()

		# Even though we calculate S here it is always going to be in the middle
		# this was the case for all cases I've seen so far.

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 'S':
					start = (i, j)

		result = 0
		
		# Let us first notice that given enough steps, the grid is filled the same, regardless where
		# it starts from. What does matter, however is whether the number of steps is even or odd. This
		# can be very easily deduced considering the solution for Problem 1, where we say that we cannot
		# end on a specific point unless the number of steps when we first reached it is even. This holds
		# true for basically all of the grids that we step through, except for the ones on the edges. So,
		# if we can easily calculate how many grids are completely filled we can find exactly how many points
		# are reachable on each one, regardless of where the entry point is. Without loss of generality, we
		# can assume that there is a fixed step parity for entering a grid at any time. 

		odd_variant = self.bfs(start, max_steps, grid)
		even_variant = self.bfs(start, max_steps + 1, grid) # since max_steps is constant, we can do this

		multiplications = (max_steps - len(grid) // 2) // len(grid) - 1 # since it's always going to spill over, halving it is fine

		odd_filled_grids = 0
		even_filled_grids = 0

		# We calculate each square of grids around the currently acquired ones. Since the starting grid
		# is odd, each even "layer" belongs to the even filled grids whereas each odd ones belongs to the
		# odd ones.

		multiplier = 1
		for i in range(multiplications):
			multiplier += 2
			delta = multiplier * 4 - 4

			if i % 2:
				odd_filled_grids += delta
			else:
				even_filled_grids += delta

		# Since due to the nature of the problem the visited points spread spherically, half of them
		# will never be filled due to how Manhattan Distance works.

		odd_filled_grids //= 2
		even_filled_grids //= 2

		# The initial grid is odd and was not counted.

		odd_filled_grids += 1

		result += odd_filled_grids * odd_variant + even_filled_grids * even_variant

		# At this moment, we have successfully calculated all of the points that do not belong to
		# grids on the edge of the infinite one. Now, we need to calculate the points belonging
		# in grids on the very border. Since S is at the very middle, we can use this to calculate 
		# exactly how much spills over into these border grids.
		#
		# First, let us calculate the very furthest points we can reach.

		furthest_length = len(grid) // 2 + multiplications * len(grid)
		point_depth = max_steps - furthest_length - 1

		# Now, we can calculate the edge grids in each direction since we know how many points
		# we have when entering them (and as we already mentioned WLoG it does not matter exactly which
		# point we start from, so we can assume the middle one). We can simply run the bfs for each one
		# of these separately, since the configuration of rocks is different considering we do not
		# have an unlimited number of steps now (not enough to fill the entire grid).

		s_x, s_y = start

		result += self.bfs((len(grid) - 1, s_y), point_depth, grid) # north
		result += self.bfs((0, s_y), point_depth, grid) # south
		result += self.bfs((s_x, 0), point_depth, grid) # east
		result += self.bfs((s_x, len(grid[0]) - 1), point_depth, grid) # west

		# Finally, all that's left now is the most difficult part - calculating the borders connecting
		# the edges. Let us first notice that the edges consist of 2 spilling over grids, one is connected
		# diagonally to an edge (the ones we just calculated) and a part of one that is adjacent to either
		# an edge and the grid diagonal to it, or 2 grids diagonal to a single edge and diagonal to each other.
		# Due to the nature of how the points spread as mentioned before, we can easily deduce that all of these
		# spill-over segments from both of these grids are equal for a certain border. So, if we calculate the
		# number of points in one of them, we can just multiply by the length of the edge and we're done.

		# Since we know that we'll always have this combination that is adjacent to an edge of the large grid,
		# we can go about calculating those ones since they're the easiest. Since we agreed that WLoG we may
		# reach each edge through its center point of the side entrance, the fastest way to reach both of
		# these segments would be in reference to it. Since we don't particularly care about the entry point,
		# we just need the number of steps left for each of these.

		# we only need to travel half the length, so we lose that from our points
		steps_adjacent = point_depth - len(grid) // 2 - 1
		# for the diagonal ones, we need to go back by the length of the grid (traversal here would happen earlier)
		# and move towards the segment
		steps_diagonal = point_depth + len(grid) - len(grid) // 2 - 1

		# North-East

		ne_entry = (len(grid) - 1, 0)

		ne_adjacent = self.bfs(ne_entry, steps_adjacent, grid)
		ne_diagonal = self.bfs(ne_entry, steps_diagonal, grid)

		# there is an extra diagonal one in here, so we subtract it (and will do this for all sides)

		result += (multiplications + 1) * (ne_adjacent + ne_diagonal) - ne_diagonal

		# North-West

		nw_entry = (len(grid) - 1, len(grid) - 1)

		nw_adjacent = self.bfs(nw_entry, steps_adjacent, grid)
		nw_diagonal = self.bfs(nw_entry, steps_diagonal, grid)

		result += (multiplications + 1) * (nw_adjacent + nw_diagonal) - nw_diagonal

		# South-East

		se_entry = (0, 0)

		se_adjacent = self.bfs(se_entry, steps_adjacent, grid)
		se_diagonal = self.bfs(se_entry, steps_diagonal, grid)

		result += (multiplications + 1) * (se_adjacent + se_diagonal) - se_diagonal

		# South-West

		sw_entry = (0, len(grid) - 1)

		sw_adjacent = self.bfs(sw_entry, steps_adjacent, grid)
		sw_diagonal = self.bfs(sw_entry, steps_diagonal, grid)

		result += (multiplications + 1) * (sw_adjacent + sw_diagonal) - sw_diagonal

		return result

solver = Solver()
solver.solve()