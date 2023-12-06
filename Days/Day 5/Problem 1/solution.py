import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		_, seeds = [x.split() for x in problem_input[0].split(': ')]
		seeds = [int(x) for x in seeds]
		mappings = {}

		start_seeds = seeds[:]
		start = ''
		end = ''

		for line in list(filter(lambda x: x != '\n', problem_input[2:])):
			if line[0].isdigit():
				destination, source, length = [int(x) for x in line.split()]

				for seed in seeds:
					if source <= seed <= source + length - 1:
						mappings[start][seed] = destination + seed - source
			else: 
				if start != end != '':
					seeds = [mappings[start][x] for x in seeds]
				start, end = line[:-6].split('-to-')

				mappings[start] = {
					'destination': end,
				}

				for seed in seeds:
					mappings[start][seed] = seed

		result = sys.maxsize
		for seed in start_seeds:
			key = 'seed'
			while True:
				seed = mappings[key][seed]
				key = mappings[key]['destination']

				if key == 'location':
					break

			result = min(result, seed)

		return result

solver = Solver()
solver.solve()