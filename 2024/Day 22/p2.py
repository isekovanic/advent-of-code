import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# We optimize the search for sequences by calculating each sequence as it appears
# in real time, and then just adding to it the first time it appears in each initial
# secret. At the end we get the value for each secret's subsequence and we just return
# the maximum one of these since we don't care about which sequence was actually used.
class Solver(SolverCore):
    
    execute_step = lambda self, x, y: (x ^ y) % 16777216
    def get_secret_number(self, seed):
        secret = seed
        
        # step 1
        step_1 = secret * 64
        secret = self.execute_step(secret, step_1)
        
        # step 2
        step_2 = secret // 32
        secret = self.execute_step(secret, step_2)
        
        # step 3
        step_3 = secret * 2048
        return self.execute_step(secret, step_3)
        
    def _solve(self, problem_input):
        secret_seeds = [int(x) for x in problem_input]
        sequence_map = defaultdict(lambda: 0)
        
        for seed in secret_seeds:
            secret = seed
            sequence = []
            visited = set([])
            last = secret % 10
            for _ in range(2000):
                secret = self.get_secret_number(secret)
                price = secret % 10
                
                sequence.append(price - last)
                sequence = sequence[-4:]
                
                seq_key = tuple(sequence)
                if seq_key not in visited and len(seq_key) == 4:
                    sequence_map[seq_key] += price
                    visited.add(seq_key)
                
                last = price
        
        return max(sequence_map.values())


solver = Solver(23, { 'test': 'input_test_p2.txt' })
solver.solve()