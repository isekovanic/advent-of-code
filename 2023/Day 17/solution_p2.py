import sys
import heapq

sys.path.append('../../')

from Core import SolverCore

# Directions:
# 0 - standing still
# 1 - down
# 2 - up
# 3 - right
# 4 - left

directions = {
	0: (0, 0),
	1: (1, 0),
	2: (-1, 0),
	3: (0, 1),
	4: (0, -1),
}

class Solver(SolverCore):
	def is_valid(self, pos, grid):
		x, y = pos

		return 0 <= x < len(grid) and 0 <= y < len(grid[0])

	def get_neighbours(self, node, direction, consecutive_nodes, grid):
		# Can't think of a better way to handle the first node being skipped weight wise,
		# there's probably something not as silly as this and the check below but I found it
		# easiest to implement "standing still". Needless to say, this is mostly redundant as
		# we always skip it bar the first time, but oh well.
		dx = [0, 1, -1, 0, 0]
		dy = [0, 0, 0, 1, -1]

		neighbours = []
		
		x, y = node

		for new_dir, (d_i, d_j) in enumerate(zip(dx, dy)):
			# enforce at least 4 consecutive nodes
			if consecutive_nodes < 4 and new_dir != direction and direction != 0:
				continue

			# ensure no more than 10 consecutive nodes appear in the path
			if new_dir == direction and consecutive_nodes == 10 or directions[direction] == (-d_i, -d_j) or new_dir == 0: # stop going in this direction
				continue

			new_node = (x + d_i, y + d_j)
			if self.is_valid(new_node, grid):
				neighbours += [(new_node, new_dir)]

		return neighbours

	def dijkstra(self, grid, start, end):
		# We represent the state as: (distance_so_far, node, direction, consecutive_nodes)
		priority_queue = [(0, start, 0, 0)]
		# Since the states are unique we can apply a handling of state visits, since the first time we
		# see a state it is always going to be the most optimal due to the nature of Dijkstra's algorithm.
		# Note: This is not so typical of Dijkstra.
		visited = set([])

		while priority_queue:
			current_distance, current_node, direction, consecutive_nodes = heapq.heappop(priority_queue)

			if current_node == end:
				return current_distance

			key = (current_node, direction, consecutive_nodes)
			if key in visited:
				continue

			visited.add(key)

			for neighbour in self.get_neighbours(current_node, direction, consecutive_nodes, grid):
				n_node, n_direction = neighbour
				x, y = n_node
				weight = grid[x][y]
				distance = current_distance + weight

				heapq.heappush(priority_queue, (distance, n_node, n_direction, (consecutive_nodes + 1) if n_direction == direction else 1))

		# will never happen, since a path exists between every 2 nodes in the grid
		return -1

	def _solve(self, problem_input):

		grid = [[int(x) for x in row.strip()] for row in problem_input]

		start = (0, 0)
		end = (len(grid) - 1, len(grid[0]) - 1)

		return self.dijkstra(grid, start, end)

solver = Solver(94)
solver.solve()