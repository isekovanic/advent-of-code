import sys

sys.path.append('../../')

from Core import SolverCore

memo = {}

class Solver(SolverCore):
	def find_all_arrangements(self, record, configuration):
		if record == '':
			return len(configuration) == 0
		if len(configuration) == 0:
			return '#' not in record

		result = 0
		move_dot = 0
		move_hashtag = 0
		key = (record, str(configuration))

		if key in memo:
			return memo[key]

		# move ahead, do not create any blocks
		move_dot = self.find_all_arrangements(record[1:], configuration)

		# is the start of a faulty gear block, it cannot be an end because that would
		# have been caught before by the memo
		# try to move ahead for the entire block if possible, but do not spill into the next block
		if configuration[0] < len(record) and '.' not in record[:configuration[0]] and record[configuration[0]] != '#':
			move_hashtag = self.find_all_arrangements(record[configuration[0] + 1:], configuration[1:])

		results = {
			'.': move_dot,
			'#': move_hashtag,
			'?': move_dot + move_hashtag
		}

		memo[key] = results[record[0]]

		return memo[key]


	def _solve(self, problem_input):
		result = 0

		for line in problem_input:
			record, configuration = line.split()
			configuration = [int(x) for x in configuration.split(',')]

			result += self.find_all_arrangements(record + '.', configuration)
		
		return result

solver = Solver(21)
solver.solve()