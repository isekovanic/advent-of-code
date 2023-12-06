import sys
from math import ceil, sqrt

sys.path.append('../../../Core')

from SolverCore import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):
		time = int(''.join(problem_input[0].split(':')[1].split()))
		record = int(''.join(problem_input[1].split(':')[1].split()))

		# -ms^2 + time * ms - record = 0 

		ms = [ceil((time - sqrt(time ** 2 - 4 * record)) / 2), ceil((time + sqrt(time ** 2 - 4 * record)) / 2)]

		return ms[1] - ms[0]

solver = Solver()
solver.solve()