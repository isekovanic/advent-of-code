import sys
from collections import defaultdict

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        registers = defaultdict(int)
        
        for line in problem_input:
            op, cond = line.strip().split(' if ')
            cond_name = cond.split(' ')[0]
            cond = cond.replace(cond_name, 'registers["{}"]'.format(cond_name))
            
            if eval(cond):
                dest, operation, value = op.split(' ')
                value = int(value)
                
                if operation == 'inc':
                    registers[dest] += value
                else:
                    registers[dest] -= value
        
        return max(registers.values())


solver = Solver(1)
solver.solve()