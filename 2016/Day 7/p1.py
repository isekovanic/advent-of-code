import sys
from string import ascii_lowercase

sys.path.append('../../')

from Core import SolverCore
class Solver(SolverCore):
    def _solve(self, problem_input):
        abba_strings = []
        
        for i in ascii_lowercase:
            for j in ascii_lowercase:
                if i != j:
                    abba_strings += ['{}{}{}{}'.format(str(i), str(j), str(j), str(i))]
                
        result = 0
        for line in problem_input:
            is_hypernet = False
            hypernets_good = True
            addresses_good = False
            for address in line.strip().replace(']', '[').split('['):
                if any(string in address for string in abba_strings):
                    if is_hypernet:
                        hypernets_good = False
                    else:
                        addresses_good = True
                is_hypernet = not is_hypernet
            
            if hypernets_good and addresses_good:
                result += 1
                
                

        return result


solver = Solver(2, { 'test': 'input_test_p1.txt' })
solver.solve()