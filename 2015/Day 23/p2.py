import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        instructions = []
        
        for line in problem_input:
            segments = line.strip().replace(',', '').split()
            instruction, *rest = segments
            
            if instruction == 'jio' or instruction == 'jie':
                reference, jump = rest
                instructions += [(instruction, reference, int(jump))]
            elif instruction == 'jmp':
                jump = rest[0]
                instructions += [(instruction, int(jump))]
            else:
                reference = rest[0]
                instructions += [(instruction, reference)]
            
        registries = {
            'a': 1,
            'b': 0
        }
        
        idx = 0
        
        while 0 <= idx < len(instructions):
            instruction = instructions[idx]
            increment = 1
            if instruction[0] == 'jmp':
                increment = instruction[1]
            elif instruction[0] == 'jio':
                _, reference, jump = instruction
                if registries[reference] == 1:
                    increment = jump
            elif instruction[0] == 'jie':
                _, reference, jump = instruction
                if registries[reference] % 2 == 0:
                    increment = jump
            elif instruction[0] == 'inc':
                reference = instruction[1]
                registries[reference] += 1
            elif instruction[0] == 'tpl':
                reference = instruction[1]
                registries[reference] *= 3
            else:
                reference = instruction[1]
                registries[reference] /= 2
            idx += increment
            
        return registries['b']

solver = Solver(1)
solver.solve()