import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# We keep the data as a range instead of counting how many elements it has (since we are likely
# going to have many space segments anyway). Starting from the right hand side, we try to fit
# each data segment into an empty space exactly ONCE (as the problem states). If it doesn't fit,
# we don't move it.
# If we move a segment, we do 2 things:
# - We release its memory, meaning its following space segment increases by its length
# - We modify the segment's range within the map to the new range
# This allows us to get a new map containing ranges of segments that we can iterate over in the end
# and use the triangular formula trick from part 1 to calculate the final result.
class Solver(SolverCore):
    def sum_range(self, f, t):
        return t * (t + 1) // 2 - f * (f - 1) // 2
    def _solve(self, problem_input):
        disk_map = problem_input[0].strip()
        id_count = {}
        space_count = defaultdict(tuple)
        total_size = 0
        
        for i in range(len(disk_map)):
            idx = i // 2
            size = int(disk_map[i])
            new_total_size = total_size + size
            if i % 2 == 0:
                id_count[idx] = (total_size, new_total_size)
            else:
                space_count[idx] = (total_size, new_total_size)
                
            total_size = new_total_size
            
        max_id = len(id_count)
        result = 0
        
        for i in range(max_id - 1, 0, -1):
            df, dt = id_count[i]
            for j in range(i):
                sf, st = space_count[j]
                
                if sf >= st:
                    continue
                
                if st - sf >= dt - df:
                    to = sf + dt - df
                    id_count[i] = (sf, to)
                    space_count[j] = (to, st)
                    
                    break
        
        for i in range(max_id):
            f, t = id_count[i]
            result += i * self.sum_range(f, t - 1)

        return result


solver = Solver(2858)
solver.solve()