import sys
import re

sys.path.append('../../')

from Core import SolverCore

# This was by far my favourite problem so far. Hopefully we get more like this one
# instead of soul crushing grids :^)
# Don't let the couple of lines fool you, the problem is actually substantially difficult.
# Some key observations we have to make in order to be able to solve it.
# If we start printing out the results for each A starting from 0, we'll quickly notice
# that:
# - The results start filling up from the left, towards the right
# - The digits within the results are repeating for each output, the left one being the
#     control one (meaning: we can eventually get to the wanted answer)
# - Each next digit changes after its predecessor has changed exactly 8 times
# This basically means that for every digit to appear, exactly 8 ** digit_index within the
# result. Afterwards, that same digit changes after exactly that many A increments as well
# (because its predecessor needs to be incremented 8 times for this to happen).
# Now, finding a digit in itself is not enough, since we need to increment as many times as
# the index of the digit starting from the previous result, since we're going from the right.
# For example, it could very well be that even though we've found the digit 0 at the last
# position, in order to find the digit before it we'd need to move more than 8 steps (virtually
# increasing the 0 we just found to whatever comes next).
# Instead, we check this the other way around - we calculate the steps needed for the digit to
# appear and then we cross-check all potential solution digits which are all mod 8 values. This
# way, if we end up going towards a stale branch we can easily backtrack and go a different path.
# The recursive solution simply returns the first time it encounters the correct output, which is
# the least amount of steps needed indeed.
class Solver(SolverCore):
    def combo_operand_value(self, a, b, c, operand):
        if operand == 6:
            return c
        if operand == 5:
            return b
        if operand == 4:
            return a
        
        return operand
    
    def find_outputs(self, a, b, c, instructions):
        ptr = 0
        result = ''
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
                    result += str(combo_operand_value % 8)
                case 6:
                    b = a // (2 ** combo_operand_value)
                case 7:
                    c = a // (2 ** combo_operand_value)
            
            ptr += 2
        
        return result
        
    def _solve(self, problem_input):
        registers, instructions = problem_input
        _, b, c = [int(x.split(':')[1].strip()) for x in registers]
        instructions = [int(x) for x in re.findall('[0-9]+', instructions[0].strip())]
        wanted_result = ''.join([str(x) for x in instructions])[::-1]
        
        def dfs(result, d):
            if d == len(wanted_result):
                return result
            for i in range(8):
                result_candidate = result * 8 + i
                output = self.find_outputs(result_candidate, b, c, instructions)
                if output[0] == wanted_result[d]:
                    subtree_result = dfs(result_candidate, d + 1)
                    if subtree_result > -1:
                        return subtree_result
            # no result for the current subtree
            return -1
        
        return dfs(0, 0)
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(117440, { 'test': 'input_test_p2.txt' })
solver.solve()