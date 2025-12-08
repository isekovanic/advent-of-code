import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        *value_inputs, operation_inputs = problem_input
        
        values = []
        
        for line in value_inputs:
            new_values = re.findall('[0-9]+', line)
            
            values.append(new_values)
        
        operations = re.findall('[+*]', operation_inputs)
        
        return sum([eval(operation.join(list(vals))) for vals, operation in zip(list(zip(*values)), operations)])


solver = Solver(4277556)
solver.solve()