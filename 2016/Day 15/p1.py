import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        disks = []
        for line in problem_input:
            numbers = [int(x) for x in re.findall('[0-9]+', line)]
            _, positions, _, pos = numbers
            disks.append((positions, pos))
        
        t = 0
        while not all((t + pos + idx + 1) % positions == 0 for idx, (positions, pos) in enumerate(disks)):
            t += 1

        return t


solver = Solver(5)
solver.solve()