import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        ranges = [tuple(token.split('-')) for token in problem_input[0].split(',')]
        result = 0
        
        for rng in ranges:
            start, end = [int(x) for x in rng]
            
            for i in range(start, end + 1):
                len_i = len(str(i))
                
                for rep in range(2, len_i + 1):
                    if len_i % rep == 0:
                        div = 10 ** (len_i // rep)
                        
                        vals = set([])
                        acc = i
                        
                        while acc:
                            vals.add(acc % div)
                            acc //= div
                        
                        if len(vals) == 1:
                            result += i
                            break
                        
        return result


solver = Solver(4174379265)
solver.solve()