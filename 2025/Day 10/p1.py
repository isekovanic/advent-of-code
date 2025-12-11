import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def solve_machine(self, configuration, buttons):
        button_masks = []
        
        for button in buttons:
            button_mask = 0
            
            for idx in button:
                button_mask |= 1 << idx
            
            button_masks.append(button_mask)
        
        # (bitmask, moves)
        queue = [(0, 0)]
        visited = set([])
        
        while len(queue):
            current_configuration, moves = queue.pop(0)
            
            if current_configuration in visited:
                continue
            
            if current_configuration == configuration:
                return moves
            
            visited.add(current_configuration)
            
            for button_mask in button_masks:
                queue.append((current_configuration ^ button_mask, moves + 1))
            
        # no solution, should not happen
        assert False

    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            conf, *buttons, _ = line.split(' ')
            buttons = [[int(x) for x in re.findall('[0-9]+', button)] for button in buttons]
            
            configuration = int(conf[1:-1][::-1].replace('#', '1').replace('.', '0'), 2)
            
            result += self.solve_machine(configuration, buttons)

        return result


solver = Solver(7)
solver.solve()