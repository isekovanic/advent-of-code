import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        registers = { 'a': 0, 'b': 0, 'c': 1, 'd': 0 }
        instructions = [x.strip().split(' ') for x in problem_input]
        
        idx = 0
        while idx < len(instructions):
            segments = instructions[idx]
            if len(segments) == 3:
                instruction, val1, val2 = segments
                
                comparator = int(val1) if val1.isnumeric() else registers[val1]
                
                if instruction == 'jnz':
                    if comparator != 0:
                        idx += int(val2)
                        continue
                else:
                    registers[val2] = comparator
            else:
                instruction, register = segments
                
                if instruction == 'inc':
                    registers[register] += 1
                else:
                    registers[register] -= 1
            idx += 1
            
        return registers['a']


solver = Solver(42)
solver.solve()