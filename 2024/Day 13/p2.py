import sys
import re

sys.path.append('../../')

from Core import SolverCore

# Since the final numbers for X and Y are way too large and we don't have an upper limit on the
# number of times we can press each button, this is impossible to bruteforce.
# Instead, let us take note of the fact that in order to solve this, let us first make the observation
# that the solution to the problem is actually the solution to the following system of equations:
#
# a_1 * A + a_2 * B = c_1
# b_1 * A + b_2 * B = c_2
#
# Where a_1 and a_2 are the X increments and b_1 and b_2 are the Y increments for each button respectively
# and c_1 and c_2 are the X and Y destinations, respectively. Finally, A and B are the presses of each button.
# The system can have 3 possible outcomes:
# 1. No solution (a1 / a2 != b1 / b2)
# 2. Infinitely many solutions (a1 / a2 == b1 / b2 and both a and b coefficients grow linearly the same as c1 / c2)
# 3. A single solution otherwise
# We're interested in situations 2 and 3 specifically, since situation 1 will always return 0 as the answer.
# In the event of situation 3, we simply return the solution to the system of equations if the system has an integer
# solution for both A and B (otherwise the single solution does not fit into our constraints).
# In the event of situation 2, we check if pressing button A gives us more yield than it costs (that happens if a1 / b1
# is higher than 3 since that's the cost of button A), in which case we press button A all the way through. Otherwise,
# we press button B all the way through.
# It is worth noting that you can easily check if situation 2 can ever occur, and for all of the test cases I've
# encountered that is not the case - but rather each system has a single integer solution and no solution otherwise. I
# added that part for completeness of the puzzle. Here's are a few examples where this would be relevant:
#
# - Press button A all the way:
#   Button A: X+5, Y+5
#   Button B: X+1, Y+1
#   Prize: X=30, Y=30
# - Press button B all the way:
#   Button A: X+1, Y+1
#   Button B: X+5, Y+5
#   Prize: X=30, Y=30
class Solver(SolverCore):
    def cramer_rule(self, a1, b1, c1, a2, b2, c2):
        # If the system is unsolvable, return -1 (parallel lines, inconsistent system)
        if a1 * b2 == a2 * b1 and b1 * c2 != b2 * c1:
            return 0
        
        # Check for infinite solutions (proportional equations)
        if a1 * b2 == a2 * b1 and b1 * c2 == b2 * c1 and a1 * c2 == a2 * c1:
            # we can justify always pressing button A
            if a1 / b1 > 3.0 and c1 % a1 == 0:
                return int(c1 // a1) * 3
            # otherwise, always press button B
            return int(c1 // b1) if c1 % b1 == 0 else 0
        
        # Otherwise, we can find the unique solution using Cramer's rule
        det = a1 * b2 - a2 * b1  # determinant of the coefficient matrix
        
        # Cramer's rule to solve for x and y (which are in our case A and B presses)
        det_x = c1 * b2 - c2 * b1
        det_y = a1 * c2 - a2 * c1
        
        x = det_x / det
        y = det_y / det
        
        # Check if the solutions are integers
        if x % 1 != 0 or y % 1 != 0:
            return 0
    
        return int(x * 3 + y)
    def _solve(self, problem_input):
        result = 0
        
        for game in problem_input:
            button_a, button_b, prize = [[int(x) for x in re.findall('-?[0-9]+', line.strip())] for line in game]
            
            a_x, a_y = button_a
            b_x, b_y = button_b
            dest_x, dest_y = prize
            
            dest_x += 10000000000000
            dest_y += 10000000000000
            
            result += self.cramer_rule(a_x, b_x, dest_x, a_y, b_y, dest_y)
            
        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(875318608908)
solver.solve()