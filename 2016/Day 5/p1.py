import sys
from hashlib import md5

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        password = problem_input[0].strip()
        i = 1
        iterations = 0
        result = ''
        while iterations < 8:
            md5_hash = md5('{}{}'.format(password, str(i)).encode()).hexdigest()
            if md5_hash[:5] == '00000':
                result += md5_hash[5]
                iterations += 1
            i += 1
        
        return result


solver = Solver('18f47a30')
solver.solve()