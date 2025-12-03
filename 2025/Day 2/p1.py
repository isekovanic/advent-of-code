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
                if len(str(i)) % 2 == 0:
                    div = 10 ** (len(str(i)) / 2)
                    
                    if i // div == i % div:
                        result += i
                        
        return result


solver = Solver(1227775554)
solver.solve()