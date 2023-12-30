import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):
		_, seed_ranges = [x.split() for x in problem_input[0].split(': ')]
		seed_ranges = [int(x) for x in seed_ranges]
		seeds = []
		for i in range(0, len(seed_ranges), 2):
			seeds += [(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1])]

		mappings = {}

		start = ''
		end = ''

		new_ranges = {}

		for line in list(filter(lambda x: x != '\n', problem_input[2:] + ['END'])):
			if line[0].isdigit():
				destination, source, length = [int(x) for x in line.split()]

				mappings[(source, source + length)] = destination - source
			else:
				new_seeds = []
				while len(seeds):
					seed_s, seed_e = seeds.pop()
					found_overlap = False
					for key, val in mappings.items():
						s, e = key
						# process all variants where the mapping and the seed range can overlap
						if seed_s < s < e < seed_e: # mapping is inside of seed range
							seeds += [(seed_s, s)]
							seeds += [(e, seed_e)]
							new_seeds += [(s + val, e + val)]
							found_overlap = True
						elif seed_s < s < seed_e <= e: # mapping is coming to the right of seed range
							seeds += [(seed_s, s)]
							new_seeds += [(s + val, seed_e + val)]
							found_overlap = True
						elif s <= seed_s < e < seed_e: # mapping is coming to the left of seed range
							seeds += [(e, seed_e)]
							new_seeds += [(seed_s + val, e + val)]
							found_overlap = True
						elif s <= seed_s <= seed_e <= e: # seed range is inside of mapping
							new_seeds += [(seed_s + val, seed_e + val)]
							found_overlap = True
						if found_overlap: # if an overlap is found, break and let the stack handle the rest
							break
					if (not found_overlap):
						new_seeds += [(seed_s, seed_e)]

				seeds = new_seeds
				mappings = {}

		return (sorted(seeds)[0][0])

solver = Solver(46)
solver.solve()