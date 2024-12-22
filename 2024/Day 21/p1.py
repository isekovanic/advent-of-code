import sys

sys.path.append('../../')

from Core import SolverCore
from itertools import permutations, product

# Really loved this problem, despite it taking me quite a while to solve. Let's go
# through the thought process chronologically.
# My first idea revolved around always being able to heuristically find the best
# solution in any possible scenario. In essence, we can make the observation that
# the best possible path (or one of them at least) always has as many consecutive moves
# in a single direction as possible. This essentially means that if we want to get from
# A to 7 for example, it's always better down the line to go ^^^<< instead of ^<^<^ for
# example. This is due to the fact that the latter would produce more moves for the pads
# controlling the main one, thus resulting in more moves altogether. Staying on a single
# move pretty much means we can hit A multiple times (3 and 2 in the above example) and
# not have to move at all. However, this scenario is not 100% correct every time - considering
# that sometimes you may end up taking an intentionally "bad" path if it'll let you move
# better in the future. So this wasn't the way to go.
# Afterwards, I tried implementing a heuristic brute-force to try to find all of the paths
# manually and count the ones that we need (the lowest length ones). This however was too slow
# with my implementation (although to be fair, I looked at some other solutions after the fact
# and many of them actually implement a brute-force for part 1 going through all possible paths;
# I just think mine was not optimised enough or went over too many duplicate paths). Even if I got
# this to work there's no chance it'd ever solve part 2.
# So, we need something better. At this point, let's make another observation. Apart from the
# initial transformation of the main keypad to the movement pad strokes, there is something peculiar
# going on with every move that we want to translate to our own moves. We always begin at A and also
# have to go back to A every time. This is because of the fact that if we want to display 029A for
# example, we need to do <A^A^^>AvvvA (or any other variations of it) - meaning we would end up with
# something like this for each part of the code: <A ^A ^^>A vvvA. Taking the first segment as an
# example, it basically means that we need to go do < and then back to A in the shortest way
# possible. This property of the commands translates recursively too. As a side-effect of it, it
# also means that we can consider the final list of commands in segments - and each segment is left
# to be optimised by itself and has no influence on the other segments. This is pretty important
# with what we're about to do.
# First, we calculate the original code translation into keystrokes. Our solver takes a pad and
# a list of commands we want to do. We can easily calculate all of the optimal paths, provided we
# keep the list of commands relatively small. We first look for all of the paths that have the
# length of the Euclidean distance between the two buttons we want to inspect, so for example
# going from A to 7 would give us a distance of 5 and this will always be the optimal length.
# Since we need to go up 3 times and left 2, we want to have all possible permutations of the
# following list ['^', '^', '^', '<', '<'], removing the ones that go over the X part of the
# pad. For good measure, we also cache these paths as we can easily reuse them if we encounter
# the same move (and we for sure will, considering how large the answers are).
# Then, we write a DP-like approach which uses the observation we made. Let us denote a minimization
# function called f(). If we have a string of commands 'XYZ', thanks to the disjunct property of
# the keystrokes we can say without any loss of generality that f('XYZ') = min(f('AX'), f('XY'), f('YZ')).
# In other words, it means that we can calculate each segment separately and just find the minimum one.
# Of course, we also have to take into account that if there are multiple ways to get 'AX' we have to count
# each one of those; so first we solve the pad problem for 'AX' and only then do we find the minimum. We stop
# counting once we reach the desired depth of robot keypads, which in this case is 2.
# Since we're now doing this recursively, we can very easily cache already seen states and so this
# finally gives us a solution that runs blazingly quickly and only really counts sizes.

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
                
                # remove paths that are invalid
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
        if depth == 2:
            return len(commands)
        
        cache_key = (commands, depth)
        if cache_key in count_cache:
            return count_cache[cache_key]
        
        count_cache[cache_key] = 0
        
        previous_char = 'A'
        
        for char in commands:
            # find all variants of moving between the nodes
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


solver = Solver(126384)
solver.solve()