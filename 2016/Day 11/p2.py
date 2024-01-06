import sys
from itertools import combinations
from copy import deepcopy

sys.path.append('../../')

from Core import SolverCore

# Oh my god. This one destroyed me.
# As a very short summary:
# - We do a standard BFS, but we try to skip as many states as we can.
# - We do NOT go back to floors that are already cleared - this is counter productive.
# - We skip states we've already visited before.
# - It is not enough to check if the particular state has been visited, but rather we
#   need to check if a "similar" state has been seen before. What this means is that if
#   we've had the same configuration of microchip/generator pairs on various floors before,
#   we can skip this state entirely since we do not need to look at it (the first one found
#   will always be the most optimal one due to the nature of how BFS works). This means that
#   for each state we generate a particular key that is independent of the actual elements,
#   but rather depends on how they're configured on all of the floors.
class Solver(SolverCore):
    def is_valid_state(self, state):
        for item in state:
            element, item_type = item
            if item_type == 'microchip' and (element, 'generator') not in state and any(i[1] == 'generator' for i in state):
                return False
        return True
    
    # The key generation function. Each element is labelled with an ID, starting from the bottom floor.
    # Note that the type of the item we're currently viewing (either "generator" or "microchip") IS very
    # important, as having a promethium generator on the first floor and a promethium microchip on the
    # second is not the same as having a promethium microchip on the first floor and a promethium generator
    # on the second. However, having a promethium generator on the first floor and a promethium microchip on
    # the second IS the same as having a cobalt generator on the first floor and having a cobalt generator on
    # the second, in terms of caching at least. As it turns out, this shaves off a LOT of unnecessary states.
    def generate_key(self, state):
        name_map = {}
        id = 0
        key = ()
        
        for floor in state:
            key_floor = ()
            for item in floor:
                el, t = item
                if el not in name_map:
                    name_map[el] = id
                    id += 1
                t = 'G' if t == 'generator' else 'M'
                key_floor += ('{}{}'.format(str(name_map[el]), t),)
            key += (key_floor,)
        
        return key
        
    def _solve(self, problem_input):
        floors = [[] for _ in range(4)]
        
        for floor, line in enumerate(problem_input):
            _, items = line.strip().split('contains ')
            items = items.replace('and', ',and')
            for item in items.split(','):
                floors[floor].append(tuple(item.replace('a ', '').replace('-compatible', '').replace('.', '').replace('and', '').strip().split(' ')))
            
        
        floors = [tuple(sorted(filter(lambda x: x != ('nothing', 'relevant') and x != ('',), floor))) for floor in floors]
        floors[0] += (('elerium', 'microchip'), ('dilithium', 'microchip'), ('elerium', 'generator'), ('dilithium', 'generator'))
        
        queue = [(0, 0, floors)]
        visited = set([])
        
        while queue:
            steps, current_floor, state = queue.pop(0)
            floor_state = state[current_floor]
            
            if len(floor_state) == 0:
                # can't use the elevator
                continue
                
            if all(len(floor) == 0 for floor in state[:3]):
                # found the first winning state
                return steps
            
            key = (current_floor, self.generate_key(state))
            if key in visited:
                continue
            visited.add(key)
            
            next_states = tuple(combinations(floor_state, 1)) + tuple(combinations(floor_state, 2))
            
            for next_state in next_states:
                updated_floor_state = tuple(filter(lambda x: x not in next_state, floor_state))
                if self.is_valid_state(updated_floor_state) and self.is_valid_state(next_state):
                    for next_floor in [current_floor - 1, current_floor + 1]:
                        if next_floor < 0 or next_floor > 3:
                            continue
                        if next_floor < current_floor and all(len(floor) == 0 for floor in state[:current_floor]):
                            continue
                        next_floor_state = state[next_floor] + tuple(next_state)
                        if next_floor != current_floor and self.is_valid_state(next_floor_state):
                            next_queue_state = deepcopy(state)
                            next_queue_state[current_floor] = tuple(sorted(updated_floor_state))
                            next_queue_state[next_floor] = tuple(sorted(next_floor_state))
                            
                            queue.append((steps + 1, next_floor, next_queue_state))
        
        # impossible to move everything to floor 4
        return -1

solver = Solver(-1)
solver.solve()