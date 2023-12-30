import sys

sys.path.append('../../')

from Core import SolverCore

vowels = ['a', 'e', 'i', 'o', 'u']
disallowed = ['ab', 'cd', 'pq', 'xy']


class Solver(SolverCore):
    def is_nice(self, line):
        char_set = set(list(line))
        
        vowel_check = sum([line.count(vowel) for vowel in vowels]) > 2
        repeating_check = any([char * 2 in line for char in char_set])
        disallowed_check = all([x not in line for x in disallowed])
        
        return vowel_check and repeating_check and disallowed_check
    
    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            result += self.is_nice(line.strip())
    
        return result


solver = Solver(2, { 'test': 'input_test_p1.txt' })
solver.solve()