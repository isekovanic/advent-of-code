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
            for p in passphrases:
                passphrase = ''.join(sorted(p))
                if passphrase in seen:
                    ok = False
                    break
                seen.add(passphrase)
            if ok:
                result += 1

        return result


solver = Solver(3, { 'test': 'input_test_p2.txt' })
solver.solve()