import sys
from functools import reduce

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        lenghts = [ord(x) for x in problem_input[0].strip().replace(' ', '')] + [17, 31, 73, 47, 23]
        
        seq = [i for i in range(256)]
        skip = 0
        pos = 0
        
        for _ in range(64):
            for length in lenghts:
                for i in range(length // 2 + length % 2):
                    f, t = (pos + i) % len(seq), (pos + length - i - 1) % len(seq)
                    seq[f], seq[t] = seq[t], seq[f]
                pos = (pos + length + skip) % len(seq)
                skip += 1
        
        dense_hash = [reduce(lambda x, y: x ^ y, seq[i:i + 16]) for i in range(0, 256, 16)]
        
        result = ''
        for item in dense_hash:
            hex_number = hex(item)[2:]
            if len(hex_number) == 1:
                hex_number = '0' + hex_number
            
            result += hex_number

        return result


solver = Solver('4a19451b02fb05416d73aea0ec8c00c0')
solver.solve()