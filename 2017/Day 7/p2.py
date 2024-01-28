import sys

sys.path.append('../../')

from Core import SolverCore

# My solution is once again a generic one, handling a lot of cases that simply do not appear throughout any
# of the other test cases I've seen. A couple of notes:
# - There is potential ambiguity in the nature of the problem, given the current problem description. Namely,
#   if we encounter a node which has only 2 children, each one of them has a different value (hinting at
#   the subtree being unbalanced) but yet the subtrees with the children as nodes are completely balanced, it
#   would be impossible to tell which node is the wrong one (it can be either because it depends on the direct
#   children themselves). Eric Wastl confirmed that this will never be the case, though.
# - A tree can be completely balanced and yet have a subtree that is not balanced (and contains the bad node).
#   Hence, to determine the value of the bad node we have to figure out whether the weight of a subtree does not
#   match its siblings or whether it as well as all of its children are potentially unbalanced. In other words,
#   in a general case it is not enough to simply assume the current node is bad if all of its children hold the
#   same weight, but rather we need to check for balance too because we might be wrong. I'm pointing this out
#   since I've seen a lot of solutions that don't take this into account at all.
# - A single child is an edge case that we also have to handle. For these cases as well as for the case of having
#   2 children we determine if the bad node is in a subtree solely through finding which tree is unbalanced.
class Tower:
    def __init__(self, memory):
        self.parent = None
        self.children = []
        self.memory = memory
        self.tree_memory = None
    
    def calculate_tree_memory(self):
        if self.tree_memory is not None:
            return
        tree_memory = self.memory
        for child in self.children:
            child.calculate_tree_memory()
            tree_memory += child.tree_memory
        
        self.tree_memory = tree_memory
        
class Solver(SolverCore):
    def is_balanced(self, tower, towers):
        children = tower.children
        return len(set([child.tree_memory for child in children])) == 1 and all(self.is_balanced(child, towers) for child in children) or len(children) == 0
    def find_unbalanced_memory(self, root, towers):
        root_children = root.children
        children_weights = [child.tree_memory for child in root_children]
        for child, weight in zip(root_children, children_weights):
            if children_weights.count(weight) == 1 and len(root_children) > 2 or not self.is_balanced(child, towers):
                return self.find_unbalanced_memory(child, towers)
        
        return root.memory
    def _solve(self, problem_input):
        towers = {}
        inheritance = {}
        
        for line in problem_input:
            children = []
            if '->' in line:
                line, children = line.strip().split(' -> ')
                children = children.split(', ')
            
            t_name, mem = line.strip().split(' ')
            mem = int(mem[1:-1])
            towers[t_name] = Tower(mem)
            if len(children):
                inheritance[t_name] = children
        
        for k, v in inheritance.items():
            for child in v:
                towers[k].children.append(towers[child])
                towers[child].parent = towers[k]
        
        root = None
        for tower in towers.values():
            if tower.parent is None:
                root = tower
                break
        
        for tower in towers.values():
            tower.calculate_tree_memory()
            
        unbalanced_memory = self.find_unbalanced_memory(root, towers)
        root_children_memories = [child.tree_memory for child in root.children]
        correct = 0
        wrong = 0
        
        # if someone has a clever way of doing this please let me know, I felt like a neanderthal writing this
        for memory in root_children_memories:
            if root_children_memories.count(memory) == 1:
                wrong = memory
            else:
                correct = memory
    
        return unbalanced_memory + correct - wrong


solver = Solver(60)
solver.solve()