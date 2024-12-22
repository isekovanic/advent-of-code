import sys

sys.path.append('../../')

from Core import SolverCore

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
        
        result = 0
        for seed in secret_seeds:
            secret = seed
            for _ in range(2000):
                secret = self.get_secret_number(secret)
            result += secret

        return result


solver = Solver(37327623, { 'test': 'input_test_p1.txt' })
solver.solve()