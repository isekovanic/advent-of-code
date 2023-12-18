import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def calculate_hash(self, entry):
		current_result = 0
		for char in entry:
			current_result += ord(char)
			current_result *= 17
			current_result %= 256

		return current_result

	def _solve(self, problem_input):
		lenses = [[] for _ in range(256)]
		for entry in problem_input[0].strip().split(','):
			if '=' in entry:
				parts = entry.split('=')
				label = parts[0]
				focal_length = int(parts[1])

				box_idx = self.calculate_hash(label)
				replaced = False
				for i, item in enumerate(lenses[box_idx]):
					if item[0] == label:
						lenses[box_idx][i] = (label, focal_length)
						replaced = True
						break

				if not replaced:
					lenses[box_idx] += [(label, focal_length)]
			else:
				label, _ = entry.split('-')
				box_idx = self.calculate_hash(label)

				lenses[box_idx] = list(filter(lambda x: x[0] != label, lenses[box_idx]))

		result = 0
		for i, box in enumerate(lenses):
			for j, lens in enumerate(box):
				_, focal_length = lens
				result += (i + 1) * (j + 1) * int(focal_length)

		
		return result

solver = Solver()
solver.solve()