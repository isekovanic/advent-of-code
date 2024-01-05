import sys
from string import ascii_lowercase

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        for line in problem_input:
            encrypted_string, checksum = line.strip().split('[')
            segments = encrypted_string.split('-')
            sector = int(segments.pop())
            decrypted = []
            
            for segment in segments:
                new_seg = ''
                for char in segment:
                    idx = (ascii_lowercase.index(char) + sector) % 26
                    new_seg += ascii_lowercase[idx]
                decrypted += [new_seg]
                
            # print(' '.join(decrypted), sector)
            
            if ' '.join(decrypted) == 'northpole object storage':
                return sector
            
        print('It is possible that my Northpole Object Storage name is different than yours.')
        print('Please have a look at the full output and search for something containing "northpole" or similar.')
        print('You can see the full output by uncommenting the commented out print() statement in the solution in the solution.')
        
        return -1


solver = Solver(1514)
solver.solve()