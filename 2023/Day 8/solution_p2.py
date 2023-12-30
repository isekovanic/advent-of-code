import sys

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def gcd(self, x , y):
	    if y == 0:
	        return x
	    return self.gcd(y , int(x % y))

	def _solve(self, problem_input):
		instructions = list(problem_input[0].strip())

		desert_map = {}

		for line in problem_input[2:]:
			f, t = line.strip().split(' = ')
			left, right = t.split(', ')

			desert_map[f] = (left[1:], right[:-1])

		current = []

		for node in desert_map.keys():
			if node[-1:] == 'A':
				current += [node]

		cycles = []

		for node in current:
			current_node = node
			original_instructions = instructions[:]
			cycle_start = 0
			steps = 0
			while True:
				instruction = original_instructions.pop(0)

				current_node = desert_map[current_node]['LR'.index(instruction)]

				steps += 1
				original_instructions += [instruction]

				if current_node[-1:] == 'Z':
					if cycle_start == 0:
						cycle_start = steps
					else:
						cycle = steps - cycle_start
						cycles += [(cycle, cycle_start - cycle)]
						break

		result = cycles[0][0]
		for cycle, offset in cycles:
			result = result * cycle / self.gcd(result, cycle)
		
		return int(result)

solver = Solver(6, { 'test': 'input_test_p2.txt' })
solver.solve()