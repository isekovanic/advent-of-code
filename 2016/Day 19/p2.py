import sys

sys.path.append('../../')

from Core import SolverCore

# Brute forcing this is sort of too slow due to the nature of the problem. We essentially need
# a data structure that would allow us to:
# - Easily bypass already removed nodes
# - Easily handle the circularity
# For that reason, we go with a custom implemented linked list. Additionally, since we cannot
# easily look ahead in the linked list without struggling with complexity we also keep an up-to-date
# lookup table for each node in the list so that we can access them quickly. Every time we do a single
# iteration (we reach an elf for whom if we want to continue we have to wrap around the beginning of the
# elf list again) we update this lookup table from scratch and update the indices of the elves inside of it.
# We need to do this because it's way too much of a hassle (or at least I couldn't think of a clever way to)
# keep a record of all of the removed elves to include in the calculations. For a single cycle though, since
# we always look forward to remove elves we can very safely assume that removing elves will only make a difference
# for elves in the future before they loop back. Furthermore, since the cut-off for where the target elf is
# was chosen to be the middle, we can easily prove that only half of the elves will ever be affected, meaning
# that we will never have a realistic scenario where our current elf surpasses the index of the first removed
# elf. With that in mind, if we just reset the lookup table with new indices every time a cycle is complete
# we can get an answer very efficiently despite the large number of elves.
class Node:
    def __init__(self, idx):
        self.index = idx
        self.name = idx + 1
        self.next = None
        self.prev = None
    
    def __repr__(self):
        return '{} -> {} -> {}'.format( self.prev.name, self.name, self.next.name)

class Solver(SolverCore):
    def _solve(self, problem_input):
        elves = int(problem_input[0].strip())
        
        start = Node(0)
        current = start
        node_lookup = { 0: current }
        
        for i in range(1, elves):
            next_node = Node(i)
            current.next = next_node
            next_node.prev = current
            
            current = next_node
            node_lookup[current.index] = current
        
        current.next = start
        start.prev = current
        
        current = start
        removed = 0
        
        while current.prev != current.next:
            steps_to_next = (elves - removed) // 2
            lookup = current.index + steps_to_next + removed
            
            if lookup > elves - 1:
                iterator = current
                iter_start = iterator.name
                iterator.index = 0
                node_lookup = { 0: iterator }
                iterator = iterator.next
                idx = 1
                
                while iterator.name != iter_start:
                    node_lookup[idx] = iterator
                    iterator.index = idx
                    iterator = iterator.next
                    idx += 1
                
                elves -= removed
                removed = 0
                
                continue
            
            to_remove = node_lookup[lookup]
            
            to_remove.prev.next = to_remove.next
            to_remove.next.prev = to_remove.prev
            removed += 1
            
            current = current.next

        return current.name


solver = Solver(2)
solver.solve()