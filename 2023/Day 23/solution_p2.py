import sys

sys.path.append('../../')

from Core import SolverCore

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

# Observations:
# - There isn't an instance where the paths that are NOT branching off in different directions
#	are not surrounded by '#' characters. This means that the width of the path we're travelling through
#	is always going to be 1.
# - Instead of traversing the grid point by point like we did in Problem 1, we can very easily condense this
#	into another graph. Each intersection (where the path branches off into multiple directions) can be considered
#	nodes, as the longest path between each intersection is the only path available.
# - We can then run a slightly modified version of the solution for Problem 1 to get the final solution. Please
#	keep in mind that this is still extremely slow (ran for about 3 minutes for me) and is likely due to the
#	way I wrote the DFS handling every single path. Finding the longest path is an NP-hard problem and we will
#	always have to do this, but I'm sure something can be optimized further by looking at the rankings of other
#	people.

class Solver(SolverCore):
	def is_valid(self, point, grid):
		x, y = point

		return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

	def get_neighbours(self, point, grid):
		potential_neighbours = []
		x, y = point

		for d_x, d_y in zip(dx, dy):
			neighbour = (x + d_x, y + d_y)

			if self.is_valid(neighbour, grid):
				potential_neighbours += [neighbour]

		return potential_neighbours


	# We will use bfs to generalize the grid, reducing it to a weighted, undirected graph.
	# From that point on, it would be much more efficient to run the solution to Problem 1 and
	# get a solution in a reasonable amount of time.

	def bfs(self, grid, start, intersections):
		graph = {}

		queue = [(start, 0)]
		visited = set([])

		while queue:
			current_node, path_length = queue.pop(0)

			# A set is not particularly needed for this. We only really need to know if
			# current_node is not the same as the previous node we visited, since if there
			# is a cycle a new intersection would have been reached anyway so the entire loop
			# would stop.
			
			if current_node in visited:
				continue

			visited.add(current_node)

			if current_node in intersections and current_node != start:
				# Found intersection, so reset the length and add the relevant nodes into
				# the graph.

				if start not in graph:
					graph[start] = set([])

				if current_node not in graph:
					graph[current_node] = set([])

				graph[start].add((current_node, path_length))
				graph[current_node].add((start, path_length))

				continue

			for p_n in self.get_neighbours(current_node, grid):
				if p_n not in visited:
					queue += [(p_n, path_length + 1)]

		return graph

	def dfs(self, graph, start, end):
		stack = [(start, [])]
		result = 0

		while stack:
			current_node, path = stack.pop()

			if current_node == end:
				path_length = sum(entry[1] for entry in path)
				result = max(result, path_length)
				continue

			for neighbour in graph[current_node]:
				if neighbour[0] not in [node[0] for node in path]:
					new_path = path[::]
					new_path += [neighbour]
					stack += [(neighbour[0], new_path)]

		return result

	def _solve(self, problem_input):

		grid = [list(x.strip()) for x in problem_input]

		start = ()
		end = ()

		for i in range(len(grid[0])):
			if grid[0][i] == '.':
				start = (0, i)
				
			if grid[-1][i] == '.':
				end = (len(grid) - 1, i)

		intersections = []

		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if grid[i][j] != '#' and len(self.get_neighbours((i, j), grid)) > 2:
					intersections += [(i, j)]

		intersections += [start, end]

		graph = {}
		
		for intersection in intersections:
			# We run BFS for each intersection because:
			# - It's super fast and not relevant to the final time
			# - It's a bit more intuitive to find the paths to each neighbouring node this way,
			#	and much easier to debug
			# - I had some bug while trying to do it in 1 cycle and could not bother finding
			#	and fixing it. :^)
			sub_graph = self.bfs(grid, intersection, intersections)
			for k, v in sub_graph.items():
				if k not in graph:
					graph[k] = v
				else:
					graph[k] = graph[k].union(v)
		
		# This is really slow. Consider finding a better solution for it.

		result = self.dfs(graph, start, end)

		return result

solver = Solver(154)
solver.solve()