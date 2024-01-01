import sys
from itertools import permutations

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        happiness_changes = {}
        
        for line in problem_input:
            start, _, sign, change, *rest, end = line.strip().split(' ')
            change = int(change)
            if sign == 'lose':
                change = -change
            end = end[:-1]
            if start not in happiness_changes:
                happiness_changes[start] = {}
            happiness_changes[start][end] = change
        
        people = happiness_changes.keys()
        
        people_permutations = permutations(people)
        result = 0
        
        for people_permutation in people_permutations:
            happiness = 0
            for idx, person in enumerate(people_permutation):
                prev_idx = (idx - 1) % len(people_permutation)
                next_idx = (idx + 1) % len(people_permutation)
                
                happiness += happiness_changes[person][people_permutation[prev_idx]] + happiness_changes[person][people_permutation[next_idx]]
            
            result = max(happiness, result)
            
        return result


solver = Solver(330)
solver.solve()