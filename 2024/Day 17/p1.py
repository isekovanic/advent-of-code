import sys
import re

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def combo_operand_value(self, a, b, c, operand):
        if operand == 6:
            return c
        if operand == 5:
            return b
        if operand == 4:
            return a
        
        return operand
    def _solve(self, problem_input):
        registers, instructions = problem_input
        a, b, c = [int(x.split(':')[1].strip()) for x in registers]
        instructions = [int(x) for x in re.findall('[0-9]+', instructions[0].strip())]
        
        ptr = 0
        
        result = []
        
        while ptr < len(instructions) - 1:
            opcode, operand = instructions[ptr], instructions[ptr + 1]
            
            combo_operand_value = self.combo_operand_value(a, b, c, operand)
            
            match opcode:
                case 0:
                    a = a // (2 ** combo_operand_value)
                case 1:
                    b ^= operand
                case 2:
                    b = combo_operand_value % 8
                case 3:
                    ptr = operand - 2 if a != 0 else ptr
                case 4:
                    b ^= c
                case 5:
                    result.append(str(combo_operand_value % 8))
                case 6:
                    b = a // (2 ** combo_operand_value)
                case 7:
                    c = a // (2 ** combo_operand_value)
            
            ptr += 2
            
        return ','.join(result)
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver('4,6,3,5,6,3,5,2,1,0', { 'test': 'input_test_p1.txt' })
solver.solve()