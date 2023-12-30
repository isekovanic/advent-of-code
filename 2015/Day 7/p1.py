import sys

sys.path.append('../../')

from Core import SolverCore

two_arg_ops = {
    'LSHIFT': lambda x, y: x << y,
    'RSHIFT': lambda x, y: x >> y,
    'AND': lambda x, y: x & y,
    'OR': lambda x, y: x | y
}
class Solver(SolverCore):
    def _solve(self, problem_input):
        memo = {}
        
        for line in problem_input:
            operation, destination = line.strip().split(' -> ')
            memo[destination] = operation
        
        def calculate_circuit_value(destination):
            value = memo[destination]
            
            if type(value) is int:
                return value
            
            if value.isnumeric():
                memo[destination] = int(value)
                return int(value)
            
            if 'NOT' in value:
                value = value[4:]
                if value.isnumeric():
                    memo[destination] = ~int(value)
                return ~calculate_circuit_value(value)
            
            if any([op in value for op in two_arg_ops.keys()]):
                f, operation, s = value.split(' ')
                
                if f.isnumeric():
                    f = int(f)
                else:
                    f = calculate_circuit_value(f)
                
                if s.isnumeric():
                    s = int(s)
                else:
                    s = calculate_circuit_value(s)
                
                memo[destination] = two_arg_ops[operation](f, s)
                
                return memo[destination]
            
            memo[destination] = calculate_circuit_value(value)
            return memo[destination]
        
        # in case of overflow above the designated range
        return calculate_circuit_value('a') % 65536


solver = Solver(507)
solver.solve()