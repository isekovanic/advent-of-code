import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        password = list('abcdefgh')
        
        for line in problem_input:
            instruction = line.strip().split(' ')
            if 'swap' in instruction:
                _, op, v1, _, _, v2 = instruction
                
                if op == 'position':
                    v1, v2 = int(v1), int(v2)
                    f, s = password[v2], password[v1]
                    password[v1] = f
                    password[v2] = s
                else:
                    for idx, char in enumerate(password):
                        if char == v1:
                            password[idx] = v2
                        elif char == v2:
                            password[idx] = v1
            elif 'rotate' in instruction:
                direction = 'right'
                steps = 0
                if 'step' in line:
                    _, direction, s, _ = instruction
                    steps = int(s)
                else:
                    letter = instruction[-1]
                    
                    letter_idx = password.index(letter)
                    steps = letter_idx + 1 + (letter_idx > 3)
                
                steps %= len(password)
                
                if direction == 'left':
                    password = password[steps:] + password[:steps]
                else:
                    password = password[-steps:] + password[:-steps]
            elif 'reverse' in instruction:
                _, _, s, _, e = instruction
                s, e = int(s), int(e)
                
                password = password[:s] + password[s:e + 1][::-1] + password[e + 1:]
            else:
                _, _, s, _, _, e = instruction
                
                s, e = int(s), int(e)
                
                v = password.pop(s)
                password.insert(e, v)
                
        return ''.join(password)


solver = Solver('fbdecgha')
solver.solve()