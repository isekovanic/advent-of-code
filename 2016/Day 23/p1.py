import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        registers = { 'a': 7, 'b': 0, 'c': 0, 'd': 0 }
        instructions = [x.strip().split(' ') for x in problem_input]
        
        idx = 0
        while idx < len(instructions):
            segments = instructions[idx]
            if len(segments) == 3:
                instruction, val1, val2 = segments
                
                comparator = int(val1) if val1.replace('-', '').isnumeric() else registers[val1]
                
                if instruction == 'jnz':
                    if comparator != 0:
                        idx += int(val2) if val2.replace('-', '').isnumeric() else registers[val2]
                        continue
                else:
                    if val2 in registers:
                        registers[val2] = comparator
            else:
                instruction, register = segments
                
                if instruction == 'inc':
                    registers[register] += 1
                elif instruction == 'tgl':
                    command_index = idx + registers[register]
                    if command_index < len(instructions):
                        command = instructions[command_index]
                        
                        if len(command) == 3:
                            command[0] = 'cpy' if command[0] == 'jnz' else 'jnz'
                        else:
                            command[0] = 'dec' if command[0] == 'inc' else 'inc'
                else:
                    registers[register] -= 1
            idx += 1
            
        return registers['a']


solver = Solver(3)
solver.solve()