import sys
from hashlib import md5

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        secret_key = problem_input[0].strip()
        
        i = 1
        
        while True:
            to_hash = '{}{}'.format(secret_key, str(i))
            if md5(to_hash.encode('utf-8')).hexdigest()[:5] == '00000':
                break
            
            i += 1

        return i


solver = Solver(1048970)
solver.solve()