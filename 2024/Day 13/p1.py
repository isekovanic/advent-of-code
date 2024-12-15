import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        result = 0
        
        for game in problem_input:
            button_a, button_b, prize = [[int(x) for x in re.findall('-?[0-9]+', line.strip())] for line in game]
            
            a_x, a_y = button_a
            b_x, b_y = button_b
            dest_x, dest_y = prize
            
            tokens = sys.maxsize
            
            for i in range(101):
                left_x, left_y = dest_x - b_x * i, dest_y - b_y * i
                
                cnt_a_x, cnt_a_y = int(left_x / a_x), int(left_y / a_y)
                
                if left_x % a_x == left_y % a_y == 0 and cnt_a_x == cnt_a_y:
                    tokens = min(tokens, i + cnt_a_x * 3)
            
            if tokens < sys.maxsize:
                result += tokens

        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(480)
solver.solve()