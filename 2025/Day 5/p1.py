import sys
import math

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        unprocessed_ranges, string_ids = problem_input
        
        ids = [int(x) for x in string_ids]
        ranges = set([])
        
        for u_range in sorted(unprocessed_ranges):
            start, end = [int(x) for x in u_range.split('-')]
            
            new_range = (start, end)
            
            for existing_range in ranges:
                start_i, end_i = existing_range
                
                if start_i <= start <= end_i or start_i <= end <= end_i:
                    ranges.remove(existing_range)
                    
                    new_range = (min(start, start_i), max(end, end_i))
                    
                    break
                    
            ranges.add(new_range)
        
        result = 0
        
        for id in ids:
            for range in ranges:
                s, e = range
                
                if s <= id <= e:
                    result += 1

        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        
        return [block.split('\n') for block in read_input.read().split('\n\n')]


solver = Solver(3)
solver.solve()