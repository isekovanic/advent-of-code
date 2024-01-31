import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        lenghts = [int(x) for x in problem_input[0].strip().split(',')]
        
        seq = [i for i in range(256)]
        skip = 0
        pos = 0
        
        for length in lenghts:
            for i in range(length // 2 + length % 2):
                f, t = (pos + i) % len(seq), (pos + length - i - 1) % len(seq)
                seq[f], seq[t] = seq[t], seq[f]
            pos = (pos + length + skip) % len(seq)
            skip += 1

        return seq[0] * seq[1]


solver = Solver(2)
solver.solve()