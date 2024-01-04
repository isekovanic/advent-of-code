import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):
		replacements, molecule = problem_input
		atom_map = {}
		for replacement in replacements.split('\n'):
			start, end = replacement.split(' => ')
			if start not in atom_map:
				atom_map[start] = []
			atom_map[start] += [end]
		
		result = set([])
		
		for key, values in atom_map.items():
			segments = molecule.split(key)
			for value in values:
				for i in range(len(segments) - 1):
					result.add('{}{}{}'.format(key.join(segments[:i + 1]), value, key.join(segments[i + 1:])))
		
		return len(result)
	def read_input(self, file):
		read_input = open(file, 'r')
		return read_input.read().split('\n\n')

solver = Solver(7, { 'test': 'input_test_p1.txt' })
solver.solve()