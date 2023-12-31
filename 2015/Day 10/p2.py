import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def generate_look_say_sequence(self, sequence):
        sequence += '$'
        cnt = 1
        current = sequence[0]
        result = ''
        
        for char in sequence[1:]:
            if char != current:
                result += '{}{}'.format(str(cnt), current)
                cnt = 0
                current = char
            cnt += 1
        
        return result
    def _solve(self, problem_input):
        sequence = problem_input[0].strip()
        
        for _ in range(50):
            sequence = self.generate_look_say_sequence(sequence)
            
        return len(sequence)


solver = Solver(3369156)
solver.solve()