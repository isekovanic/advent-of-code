import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

class Solver(SolverCore):
    def _solve(self, problem_input):
        rules, updates = problem_input
        
        updates = [update.split(',') for update in updates]
        relation_list = [rule.split('|') for rule in rules]
        relations = defaultdict(list)
        for rel in relation_list:
            before, after = rel
            relations[before].append(after)
        
        result = 0
        
        for update in updates:
            visited = set([])
            
            correct = True
            for page in update:
                if page in relations and any(relation in visited for relation in relations[page]):
                    correct = False
                    break
                visited.add(page)
            
            if correct:
                result += int(update[len(update) // 2])

        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(143)
solver.solve()