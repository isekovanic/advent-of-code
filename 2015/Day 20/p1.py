import sys
from math import sqrt

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def find_divisors(self, number):
        divisors = []
        for i in range(1, int(sqrt(number)) + 1):
            if number % i == 0:
                divisors += [i, number // i]
        
        return divisors
    def _solve(self, problem_input):
        limit = int(problem_input[0])
        house = 2
        
        while True:
            if (sum(self.find_divisors(house))) * 10 >= limit:
                break
            house += 1

        return house


solver = Solver(8)
solver.solve()