import sys

sys.path.append('../../')

from Core import SolverCore

# Just a very brief note regarding the solution:
# - Looking at the outputs, we can quickly figure out that the register values repeat after a while
#   so we simply need to find the outputs up until the repetition and check if they're an alternating
#   sequence. We also have to make sure it actually begins with a 0 as prompted.
# - The reason why I'm not bothering to check when I should invoke the already visited registers
#   is because all of the test cases I could find (including my original one) only ever had one out command.
#   I am highly doubtful that Eric was able to craft a test case which has 2 out commands and is
#   a valid one.
# - If we did want to generalize it in such a way though, we should first test the current set of
#   registers to find the last out command that can be reached (we can't just use the last one in
#   general as that one might be unreachable). Afterwards, we apply the visited logic there since
#   this is what we'll refer to as a cycle.
class Solver(SolverCore):
    def is_alternating_and_binary(self, sequence):
        if sequence[0] == 1:
            return False
        for f, s in zip(sequence, sequence[1:]):
            if f + s != 1:
                return False
        return True
    def _solve(self, problem_input):
        instructions = [x.strip().split(' ') for x in problem_input]
        
        a_counter = 0
        while True:
            registers = { 'a': a_counter, 'b': 0, 'c': 0, 'd': 0 }
            seen_registers = set([])
            outputs = []
            
            idx = 0
            while idx < len(instructions):
                segments = instructions[idx]
                if len(segments) == 3:
                    instruction, val1, val2 = segments
                    
                    comparator = int(val1) if val1.replace('-', '').isnumeric() else registers[val1]
                    
                    if instruction == 'jnz':
                        if comparator != 0:
                            idx += int(val2) if val2.replace('-', '').isnumeric() else registers[val2]
                            continue
                    else:
                        if val2 in registers:
                            registers[val2] = comparator
                else:
                    instruction, register = segments
                    
                    if instruction == 'inc':
                        registers[register] += 1
                    elif instruction == 'tgl':
                        command_index = idx + registers[register]
                        if command_index < len(instructions):
                            command = instructions[command_index]
                            
                            if len(command) == 3:
                                command[0] = 'cpy' if command[0] == 'jnz' else 'jnz'
                            else:
                                command[0] = 'dec' if command[0] == 'inc' else 'inc'
                    elif instruction == 'out':
                        key = tuple(registers.items())
                        if key in seen_registers:
                            break
                        seen_registers.add(key)
                        
                        if register in registers:
                            outputs.append(registers[register])
                        else:
                            outputs.append(int(register))
                        
                    else:
                        registers[register] -= 1
                idx += 1
            
            if self.is_alternating_and_binary(outputs):
                break
            
            a_counter += 1
            
        return a_counter


solver = Solver(198)
solver.solve()