import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        for line in problem_input:
            encrypted_string, checksum = line.strip().split('[')
            checksum = checksum[:-1]
            segments = encrypted_string.split('-')
            sector = segments.pop()
            occurences = {}
            
            for char in ''.join(segments):
                if char not in occurences:
                    occurences[char] = 0
                occurences[char] += 1
                
            wanted_checksum = ''.join([entry[0] for entry in sorted(occurences.items(), key = lambda x: (-x[1], x[0]))[:5]])
            
            if wanted_checksum == checksum:
                result += int(sector)
            
        return result


solver = Solver(1514)
solver.solve()