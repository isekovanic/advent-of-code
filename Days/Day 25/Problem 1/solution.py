import sys
from copy import deepcopy

sys.path.append('../../../Core')

from SolverCore import SolverCore

# This problem is a textbook minimum-cut one. A lot of resources exist about this online so not going
# to delve deep into the topic.

sys.setrecursionlimit(10000) # since the DFSs are written recursively, not going to redo them for sure

class Solver(SolverCore):
	def max_flow(self, graph, source, sink):
		# DFS that augments the paths for our max flow.
		def dfs(graph, visited, path):
			visited.add(path[-1])
			if path[-1] == sink:
				return path
			for neighbor in graph[path[-1]]:
				if neighbor not in visited:
					result = dfs(graph, visited, path + [neighbor])
					if result: # skip empty paths because they mess everything up later on
						return result
			return None

		max_flow = 0
		residual_graph = deepcopy(graph)

		while True:
			augmenting_path = dfs(residual_graph, set(), [source])
			if not augmenting_path:
				break

			min_capacity = float('inf')

			for u, v in zip(augmenting_path, augmenting_path[1:]):
				if v in residual_graph[u]:
					min_capacity = min(min_capacity, 1)  # unweighted, so capacity is either 1 or 0
					residual_graph[u].remove(v)
					residual_graph[v] += [u]

			max_flow += min_capacity
				    
		return (max_flow, residual_graph)

	def min_cut(self, residual_graph, source):
		visited = set([])
		# Just a normal DFS, to see which nodes are reachable in the residual graph
		def dfs(graph, node):
			visited.add(node)
			for neighbor in graph[node]:
				if neighbor not in visited:
					dfs(graph, neighbor)

		# Identify nodes reachable from the source in the original graph and store them in visited
		dfs(residual_graph, source)

		# Find the minimum cut nodes; they're the ones that exist in the graph but not in visited
		# (i.e were not reachable from the source).
		min_cut_nodes = {node for node in residual_graph.keys() if node not in visited}

		return min_cut_nodes

	def _solve(self, problem_input):

		graph = {}

		for line in problem_input:
			start, *ends = [x.strip() for x in line.strip().replace(':', '').split()]

			for end in ends:
				if start in graph:
					graph[start] += [end]
				else:
					graph[start] = [end]

				if end in graph:
					graph[end] += [start]
				else:
					graph[end] = [start]

		for i in graph.keys():
			for j in graph.keys():
				if i != j:
					flow, residual_graph = self.max_flow(graph, i, j)
					# Essentially waiting to find a start node that's in one of the components
					# and an end node that's in the other. According to the problem description,
					# there can only be one such minimum cut, so we take the length of the first
					# one we find and declare that to be one of our components. The length of the
					# other one is the found length subtracted from the number of nodes.
					if flow == 3:
						component_size = len(self.min_cut(residual_graph, i))
						return component_size * (len(graph) - component_size)

		# no such minimum cut found, should never happen		
		return -1

solver = Solver()
solver.solve()