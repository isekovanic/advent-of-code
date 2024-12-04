import sys

sys.path.append('../../')

from Core import SolverCore

# What's regex ? :^)
class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        enabled = True
        
        for cmds in problem_input:
            for i in range(len(cmds)):
                
                if cmds[i:].startswith('don\'t()'):
                    enabled = False
                
                if cmds[i:].startswith('do()'):
                    enabled = True
                
                if not enabled:
                    continue
                
                window = i + 4
                if cmds[i:window] != 'mul(':
                    continue
                
                next_mul = cmds[window:].find('mul')
                next_close = cmds[window:].find(')')
                
 
                if next_close >= next_mul and (next_mul != -1 or next_close == -1):
                    continue
                
                potential_operation = cmds[window:next_close + window]
                
                split = potential_operation.split(',')
                
                if len(split) != 2:
                    continue
                
                f, s = potential_operation.split(',')
                
                if f.isnumeric() and s.isnumeric() and len(f) < 4 and len(s) < 4:
                    result += int(f) * int(s)
                    
        return result


solver = Solver(48, { 'test': 'input_test_p2.txt' })
solver.solve()