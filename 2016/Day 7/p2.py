import sys
from string import ascii_lowercase

sys.path.append('../../')

from Core import SolverCore
class Solver(SolverCore):
    def _solve(self, problem_input):
        aba_strings = []
        
        for i in ascii_lowercase:
            for j in ascii_lowercase:
                if i != j:
                    aba_strings += ['{}{}{}'.format(str(i), str(j), str(i))]
                
        result = 0
        for line in problem_input:
            is_hypernet = False
            supernets_aba_strings = set([])
            hypernets_aba_strings = set([])
            for address in line.strip().replace(']', '[').split('['):
                for string in aba_strings:
                    if string in address:
                        if is_hypernet:
                            hypernets_aba_strings.add(string)
                        else:
                            supernets_aba_strings.add(string)
                is_hypernet = not is_hypernet
            
            if any('{}{}{}'.format(aba_string[1], aba_string[0], aba_string[1]) in hypernets_aba_strings for aba_string in supernets_aba_strings):
                result += 1
                
        return result


solver = Solver(3, { 'test': 'input_test_p2.txt' })
solver.solve()