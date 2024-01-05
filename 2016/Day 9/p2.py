import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def count_decompressed(self, compressed_string):
        i = 0
        result = 0
        while i < len(compressed_string):
            if compressed_string[i] == '(':
                instruction_end = i + compressed_string[i:].index(')')
                instruction = compressed_string[i + 1:instruction_end]
                cont, times = [int(x) for x in instruction.split('x')]
                to_repeat = compressed_string[instruction_end + 1:instruction_end + cont + 1]
                result += times * self.count_decompressed(to_repeat)
                i = instruction_end + cont + 1
            else:
                result += 1
                i += 1
        
        return result
    def _solve(self, problem_input):
        compressed_string = problem_input[0].strip()
                
        return self.count_decompressed(compressed_string)


solver = Solver(241920, { 'test': 'input_test_p2.txt' })
solver.solve()