import sys

sys.path.append('../../')

from Core import SolverCore
from itertools import permutations, product

# The solution from part 1 works very quickly, so for part 2 we can just increase the
# depth to which we want to count.

keypad = { '7': (0, 0), '8': (0, 1), '9': (0, 2),
           '4': (1, 0), '5': (1, 1), '6': (1, 2),
           '1': (2, 0), '2': (2, 1), '3': (2, 2),
           'X': (3, 0), '0': (3, 1), 'A': (3, 2) }

movepad = { 'X': (0, 0), '^': (0, 1), 'A': (0, 2),
            '<': (1, 0), 'v': (1, 1), '>': (1, 2), }

pad_cache = {}
count_cache = {}

dirs = {
    '>': (0, 1),
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0),
}
class Solver(SolverCore):
    def solve_for_pad(self, pad, commands):
        global pad_cache
        
        paths = []
        current_button = commands[0]
        pad_position = pad[current_button]
        wall = pad['X']
        
        for char in commands[1:]:
            char_position = pad[char]
            
            cx, cy = pad_position
            nx, ny = char_position
            
            dx, dy = cx - nx, cy - ny
            
            vertical_move = 'v' if dx < 0 else '^'
            horizontal_move = '>' if dy < 0 else '<'
            
            adx, ady = abs(dx), abs(dy)
            
            cache_key = (current_button, char)
            
            if cache_key not in pad_cache:
                potential_paths = [''.join(permutation) for permutation in permutations(horizontal_move * ady + vertical_move * adx)]
                valid_paths = set([])
                
                for potential_path in potential_paths:
                    tcx, tcy = cx, cy
                    is_valid = True
                    for cmd in potential_path:
                        tdx, tdy = dirs[cmd]
                        tcx, tcy = tcx + tdx, tcy + tdy
                        
                        if (tcx, tcy) == wall:
                            is_valid = False
                            break
                    
                    if is_valid:
                        valid_paths.add(potential_path + 'A')
                
                pad_cache[cache_key] = valid_paths
            
            paths.append(pad_cache[cache_key])
            
            pad_position = char_position
            current_button = char
        
        return [''.join(x) for x in product(*paths)]
    
    def count_paths(self, commands, depth):
        if depth == 25:
            return len(commands)
        
        cache_key = (commands, depth)
        if cache_key in count_cache:
            return count_cache[cache_key]
        
        count_cache[cache_key] = 0
        
        previous_char = 'A'
        
        for char in commands:
            paths = self.solve_for_pad(movepad, previous_char + char)
            previous_char = char
            count_cache[cache_key] += min([self.count_paths(path, depth + 1) for path in paths])
        
        return count_cache[cache_key]
    
    def _solve(self, problem_input):
        codes = [x.strip() for x in problem_input]
        
        result = 0
        for code in codes:
            paths = self.solve_for_pad(keypad, 'A' + code)
            result += min([self.count_paths(path, 0) for path in paths]) * int(code[:-1])
            
        return result


solver = Solver(154115708116294)
solver.solve()