import sys
from hashlib import md5

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        password = problem_input[0].strip()
        i = 1
        iterations = 0
        result = ['' for _ in range(8)]
        while iterations < 8:
            md5_hash = md5('{}{}'.format(password, str(i)).encode()).hexdigest()
            if md5_hash[:5] == '00000':
                position = md5_hash[5]
                char = md5_hash[6]
                if position.isnumeric() and '0' <= position < '8' and result[int(position)] == '':
                    print(i)
                    result[int(position)] = char
                    iterations += 1
                
            i += 1
        
        return ''.join(result)


solver = Solver('05ace8e3')
solver.solve()