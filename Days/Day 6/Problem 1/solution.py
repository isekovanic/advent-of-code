import sys

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		race_times = [int(x) for x in problem_input[0].split(':')[1].split()]
		race_records = [int(x) for x in problem_input[1].split(':')[1].split()]

		result = 1

		for time, record in zip(race_times, race_records):
			possible_wins = 0
			for ms in range(time + 1):
				possible_wins += (time - ms) * ms > record

			result *= possible_wins

		return result

solver = Solver()
solver.solve()