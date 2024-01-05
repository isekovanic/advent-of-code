import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        compressed_string = problem_input[0].strip()
        result = ''
        
        i = 0
        while i < len(compressed_string):
            if compressed_string[i] == '(':
                instruction_end = i + compressed_string[i:].index(')')
                instruction = compressed_string[i + 1:instruction_end]
                cont, times = [int(x) for x in instruction.split('x')]
                to_repeat = compressed_string[instruction_end + 1:instruction_end + cont + 1]
                result += times * to_repeat
                i = instruction_end + cont + 1
            else:
                result += compressed_string[i]
                i += 1
                
        return len(result)


solver = Solver(18, { 'test': 'input_test_p1.txt' })
solver.solve()