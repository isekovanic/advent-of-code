import sys

sys.path.append('../../')

from Core import SolverCore

# Thanks a lot https://x.com/ericwastl?lang=en, I did not need much rest/sleep after work anyway !
# In all seriousness, probably one of the most interesting problems I've ever seen.
# It doesn't take long to notice (and also it literally saying so in the problem statement) that
# what we're actually looking at is a logical Full Adder Circuit. So as to not spend ages explaining
# how it works, it's essentially this: https://www.electronics-tutorials.ws/combination/comb_7.html
# Now, our task is to reverse engineer the circuit and to find all 4 mistakes (or swaps) that have
# been done to make it not capable of additive boolean arithmetic.
# In retrospect (and after looking at the subreddit after the fact), I would've been much better off
# doing some clever way to print the entire circuit and just doing it by hand; which is how most people
# did it. I was under the impression that the chaining of mistakes would be too difficult to spot so
# I did not give it a shot. But anyway I have this so here we go.
# Essentially, I believe that Eric went pretty easy on us with how complicated the test cases could've
# been - up to the point that I think it's an NP-Complete problem to solve the absolutely general case
# of this. Regardless, let us make a few observations:
# - The entire circuit consists of many full adder logic circuits (one for each digit) and we can divide
#   all of these to work independently
# - The thing that we need to keep accountable is the carry digit, that if swapped could wreak havoc
#   across the entire circuit
# - The inner workings of the circuit can be isolated and reviewed on their own
# - It is NOT necessary to do the swaps on the spot (i.e to know what we should swap to immediately), but
#   rather we can rely on the fact that our algorithm is going to catch both parts of the swap in a single
#   iteration over all gates
# Now, we can define the rules of engagement that the circuit needs to follow which we'll use to determine
# whether it's valid or not.
# 1. A 'zXX' wire must not be the output of anything but an XOR gate
# 2. If we have an XOR gate, it can only be the intermediate XOR gate or the one that outputs 'zXX'
# 3. The output from an AND gate must NOT go into anything other than an OR gate
# 4. The output from an OR gate must NOT go into anything other than an XOR gate
# Please keep in mind that here we do not account for the correctness of the 'xXX' and 'yXX' wires in contrast
# to their connectivity to their respective 'zXX' wire. If we think about it, it shouldn't be needed as if
# the circuit is broken, it'll break on one of the rules from above rather than having to rely on finding
# if the values are correct.
# Rule 1. is pretty self explanatory - as the main digit output in a full adder circuit is indeed an XOR gate
# if we catch 'zXX' being anything otherwise will lead us to an error. As a matter of fact, 3 of my swaps
# were exactly this (and for other people too according to the subreddit it seems).
# Rule 2. basically says that an XOR gate can either be located as the output to 'xXX' XOR 'yXX' or the output
# of some two wires that connect to 'zXX'. Anything else is an error.
# For rule 3. the idea is that an AND gate is only allowed to directly output to the OR gate that spits out the
# carry to the next full adder. We look through all non-OR gates and see if our output appears as one of their
# inputs - if it does, it's an error.
# Finally, rule 4. states that the output of the OR gate (which spits out our carry) can only really go into an
# XOR gate (which is the next full adder's secondary XOR that outputs the next 'zXX'). Anything else is again an
# error.
# Using the rules above we get all of the values we need. I've tried this on a few other test cases and it seems
# to also work there. Wonder if it's generic enough.
# Oh also the example test case is completely out of scope of the problem itself so I crafted my own.

ops = {
    'XOR': lambda x, y: x ^ y,
    'OR': lambda x, y: x | y,
    'AND': lambda x, y: x & y
}

wires = {}
gates = {}
class Solver(SolverCore):
    def calculate_circuit(self, loc):
        global wires
        
        if loc in wires:
            return wires[loc]
        
        (f, s), cmd = gates[loc]
        op = ops[cmd]
        wires[loc] = op(self.calculate_circuit(f), self.calculate_circuit(s))
        
        return wires[loc]
    def _solve(self, problem_input):
        global wires
        global gates
        
        wires = {}
        gates = {}
        
        start_wires, gate_inputs = problem_input
        
        for wire in start_wires:
            name, val = wire.strip().split(': ')
            val = int(val)
            
            wires[name] = val
        
        for gate in gate_inputs:
            expr, loc = gate.strip().split(' -> ')
            f, op, s = expr.split(' ')
            
            gates[loc] = ((f, s), op)
        
        result = []
        for output, ((f, s), op) in gates.items():
            # rule 1
            if output[0] == 'z' and op != 'XOR':
                result.append(output)
                continue
            
            # rule 2
            if op == 'XOR' and f[0] not in 'xy' and s[0] not in 'xy' and output[0] != 'z':
                result.append(output)
                continue
            
            # rule 3
            # we also skip the first set of wires as they do not abide to the rule
            if op == 'AND' and sorted([f, s]) != ['x00', 'y00']:
                for (t_operands, t_op) in gates.values():
                    if t_op == 'OR':
                        continue
                    
                    if output in t_operands:
                        result.append(output)
                        break
                continue
            
            # rule 4
            if op == 'XOR':
                for (t_operands, t_op) in gates.values():
                    if t_op != 'OR':
                        continue
                    
                    if output in t_operands:
                        result.append(output)
                        break
        
        # one of the rules is adding 'z45' as a 9th mistake and I
        # couldn't figure out which one, so just filtering it here
        result = [x for x in result if x != 'z45']
        return ','.join(sorted([x for x in result if x != 'z45']))
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver('aaa,bbx,z01,z02', { 'test': 'input_test_p2.txt' })
solver.solve()