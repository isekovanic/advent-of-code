import sys

sys.path.append('../../')

from Core import SolverCore

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
        
        
        outputs = []
        for gate in gates.keys():
            if gate[0] == 'z':
                outputs.append(gate)
            self.calculate_circuit(gate)

        return int(''.join([str(wires[output]) for output in sorted(outputs)])[::-1], 2)
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(2024, { 'test': 'input_test_p1.txt' })
solver.solve()