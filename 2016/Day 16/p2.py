import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def calculate_checksum(self, state_string):
        checksum = ''
        for i in range(0, len(state_string), 2):
            p1, p2 = state_string[i:i + 2]
            
            if p1 == p2:
                checksum += '1'
            else:
                checksum += '0'
        return checksum
        
    def _solve(self, problem_input):
        state_string = problem_input[0].strip()
        
        wanted_length = 35651584
        
        while len(state_string) < wanted_length:
            complement = ''
            for char in state_string[::-1]:
                if char == '1':
                    complement += '0'
                else:
                    complement += '1'
            state_string = '{}{}{}'.format(state_string, '0', complement)
        
        state_string = state_string[:wanted_length]
        
        checksum = self.calculate_checksum(state_string)
        
        while len(checksum) % 2 == 0:
            checksum = self.calculate_checksum(checksum)
    
        return checksum


solver = Solver('10111110011110111')
solver.solve()