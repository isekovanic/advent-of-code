import sys
from copy import deepcopy

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        registers = { 'a': 12, 'b': 0, 'c': 0, 'd': 0 }
        instructions = [x.strip().split(' ') for x in problem_input]
        
        jnz_map = {}
        
        idx = 0
        while idx < len(instructions):
            segments = instructions[idx]
            if len(segments) == 3:
                instruction, val1, val2 = segments
                
                comparator = int(val1) if val1.replace('-', '').isnumeric() else registers[val1]
                
                if instruction == 'jnz':
                    # Since most of the operations are extremely common repetitions of inc/dec ones,
                    # we can remember the registry state each time we reach a jnz instruction since these
                    # are the ones responsible for the repetitions. The next time we reach it, we calculate
                    # how long it would take for the comparator value to reach 0 and we translate all of the
                    # operations on all other registries. We do this for every single jnz and so we're mostly
                    # done in a few milliseconds.
                    if val1 in registers:
                        key = (idx, tuple(segments))
                        if key in jnz_map:
                            prev_registers = jnz_map[key]
                            register_deltas = {}
                            
                            for k in registers.keys():
                                register_deltas[k] = registers[k] - prev_registers[k]
                            
                            # decreasing this means we'll eventually skip it
                            if register_deltas[val1] < 0 and registers[val1] % abs(register_deltas[val1]) == 0:
                                reps = registers[val1] // abs(register_deltas[val1])
                                
                                for k in registers.keys():
                                    registers[k] += register_deltas[k] * reps
                            del jnz_map[key]
                        else:
                            jnz_map[key] = deepcopy(registers)
                        comparator = registers[val1]
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