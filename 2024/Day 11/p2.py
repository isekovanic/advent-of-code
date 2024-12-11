import sys

sys.path.append('../../')

from Core import SolverCore

MAX_BLINKS = 75
splits = {}
class Solver(SolverCore):
    def find_splits(self, stone, depth = 0):
        if depth == MAX_BLINKS:
            return 1
        
        hash = (stone, depth)
        
        if hash in splits:
            return splits[hash]
        
        stone_str = str(stone)
        stone_length = len(stone_str)
        
        if stone_length % 2 == 0:
            splits[hash] = self.find_splits(int(stone_str[:stone_length // 2]), depth + 1) + self.find_splits(int(stone_str[stone_length // 2:]), depth + 1)
        else:
            splits[hash] = self.find_splits(1, depth + 1) if stone == 0 else self.find_splits(stone * 2024, depth + 1)
        
        return splits[hash]
    def _solve(self, problem_input):
        stones = [int(x) for x in problem_input[0].strip().split(' ')]
        
        result = 0
        for stone in stones:
            result += self.find_splits(stone)
            
        return result


solver = Solver(65601038650482)
solver.solve()