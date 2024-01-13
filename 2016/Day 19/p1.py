import sys

sys.path.append('../../')

from Core import SolverCore

class Node:
    def __init__(self, idx):
        self.index = idx
        self.next = None
        self.prev = None

class Solver(SolverCore):
    def _solve(self, problem_input):
        elves = int(problem_input[0].strip())
        
        start = Node(1)
        current = start
        
        for i in range(1, elves):
            next_node = Node(i + 1)
            current.next = next_node
            next_node.prev = current
            
            current = next_node
        
        current.next = start
        start.prev = current
        
        current = start
        
        while current.next != current.prev:
            next_node = current.next
            current.next = next_node.next
            next_node.next.prev = current
            
            current = current.next

        return current.index


solver = Solver(3)
solver.solve()