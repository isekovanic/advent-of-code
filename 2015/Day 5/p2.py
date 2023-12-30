import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def is_nice(self, line):
        pair_check = any([line[i + 2:].count(line[i:i + 2]) > 0 for i in range(len(line) - 1)])
        repetition_check = any([line[i:i + 3] == line[i:i + 3][::-1] for i in range(len(line) - 2)])
            
        return pair_check and repetition_check
    
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            result += self.is_nice(line.strip())
    
        return result


solver = Solver(2, { 'test': 'input_test_p2.txt' })
solver.solve()