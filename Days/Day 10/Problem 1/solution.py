import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

horizontal_compatible = {
	'left': ['-', 'L', 'F'],
	'right': ['-', 'J', '7']
}
vertical_compatible = {
	'up': ['|', '7', 'F'],
	'down': ['|', 'L', 'j']
}

directions = {
	'-': [(0, -1, horizontal_compatible['left']), (0, 1, horizontal_compatible['right'])],
	'|': [(-1, 0, vertical_compatible['up']), (1, 0, vertical_compatible['down'])],
	'L': [(-1, 0, vertical_compatible['up']), (0, 1, horizontal_compatible['right'])],
	'J': [(-1, 0, vertical_compatible['up']), (0, -1, horizontal_compatible['left'])],
	'7': [(1, 0, vertical_compatible['down']), (0, -1, horizontal_compatible['left'])],
	'F': [(1, 0, vertical_compatible['down']), (0, 1, horizontal_compatible['right'])]
}

class Graph:
	def __init__(self, pipes):
		self.edges = {}
		self.pipes = pipes

		for i in range(len(self.pipes)):
			for j in range(len(self.pipes[i])):
				if self.pipes[i][j] == 'S':
					self.start_node = (i, j)
				self.add_edge((i, j))

	def is_valid_node(self, node):
		x, y = node
		return 0 <= x < len(self.pipes) and 0 <= y < len(self.pipes[0])

	def get_neighbours(self, node):
		x, y = node
		val = self.pipes[x][y]
		neighbour_directions = directions[val] if val in directions else []
		neighbours = []

		for dx, dy, compatibility in neighbour_directions:
			potential_neighbour = (x + dx, y + dy)

			if not self.is_valid_node(potential_neighbour):
				continue
			new_val = self.pipes[potential_neighbour[0]][potential_neighbour[1]]

			if new_val in compatibility or new_val == 'S':
				neighbours += [potential_neighbour]
		
		return neighbours

	def modify_edges(self, f, t):
		if f in self.edges:
			self.edges[f] += [t] if t not in self.edges[f] else []
		else:
			self.edges[f] = [t]

	def add_edge(self, node):
		x, y = node
		for neighbour in self.get_neighbours(node):
			self.modify_edges(node, neighbour)
			self.modify_edges(neighbour, node)

	def find_largest_cycle(self):
		visited = set([])
		cycle = []

		stack = [(self.start_node, [self.start_node])]

		# dfs, but looking for only 1 cycle

		while stack:
			current_node, path = stack.pop()

			if current_node == self.start_node and len(path) > 3:
				cycle = path[path.index(self.start_node):]
				break
			if current_node not in visited:
				visited.add(current_node)
				for neighbour in self.edges[current_node]:
					stack += [(neighbour, path + [neighbour])]

		return cycle

class Solver(SolverCore):
	def _solve(self, problem_input):
		pipes = [list(row.strip()) for row in problem_input]

		graph = Graph(pipes)

		return len(graph.find_largest_cycle()) // 2

solver = Solver()
solver.solve()