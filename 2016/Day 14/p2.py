import sys
from hashlib import md5

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def md5_hex(self, salt, id):
        to_encode = '{}{}'.format(salt, str(id))
        final_hash = md5(to_encode.encode()).hexdigest()
        
        for _ in range(2016):
            final_hash = md5(final_hash.encode()).hexdigest()

        return final_hash
    def _solve(self, problem_input):
        salt = problem_input[0].strip()

        idx = 0
        cnt = 0
        hexes = {}
 
        for i in range(idx, 1001):
            hexes[i] = self.md5_hex(salt, i)

        while cnt < 64:
            encoded = hexes[idx]
            hexes[idx + 1000] = self.md5_hex(salt, idx + 1000)

            rep = None
            for i, char in enumerate(encoded):
                if '{}{}{}'.format(char, char, char) == encoded[i:i + 3]:
                    rep = char
                    break

            if rep and any('{}{}{}{}{}'.format(rep, rep, rep, rep, rep) in hexes[i] for i in range(idx + 1, idx + 1001)):
                cnt += 1

            idx += 1

        return idx - 1


solver = Solver(22551)
solver.solve()