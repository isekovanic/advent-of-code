import sys
from collections import defaultdict

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        registers = defaultdict(int)
        result = -1
        
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
            
            result = max(max(registers.values()), result)
        
        return result


solver = Solver(10)
solver.solve()