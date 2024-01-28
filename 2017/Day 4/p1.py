import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            passphrases = line.strip().split(' ')
            seen = set([])
            ok = True
            for passphrase in passphrases:
                if passphrase in seen:
                    ok = False
                    break
                seen.add(passphrase)
            if ok:
                result += 1

        return result


solver = Solver(2, { 'test': 'input_test_p1.txt' })
solver.solve()