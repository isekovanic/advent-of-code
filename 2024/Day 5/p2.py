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
            
            # For this, we assume that there is always one solution per update, given the rules. If that's
            # not the case, there is no way of consistently solving this. Running on this assumption however
            # allows us to us an insertion sort - like - algorithm to sort the update.
            if not correct:
                # start out empty
                sorted_update = []
                
                for page in update:
                    # if no conflicting pages are found, insert at the end as it doesn't matter
                    insertion_index = len(sorted_update)
                    # go over the already sorted pages
                    for i in range(len(sorted_update)):
                        current_page = sorted_update[i]
                        if page in relations and current_page in relations[page]:
                            # find the first page that exists in the rules of our current page and mark it for
                            # insertion - the others don't really matter as if this one is respected, they would
                            # be too since the list is already sorted
                            insertion_index = i
                            break
                    
                    sorted_update.insert(insertion_index, page)
                
                result += int(sorted_update[len(sorted_update) // 2])

        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(123)
solver.solve()