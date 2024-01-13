import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def can_be_merged(self, range1, range2):
        r1_s, r1_e = range1
        r2_s, r2_e = range2
        
        return r1_s <= r2_s <= r1_e or r2_s <= r1_s <= r2_e or r1_e + 1 == r2_s or r2_e + 1 == r1_s
    def merge_ranges(self, range1, range2):
        r1_s, r1_e = range1
        r2_s, r2_e = range2
        
        return min(r1_s, r2_s), max(r1_e, r2_e)
        
    def _solve(self, problem_input):
        ranges = []
        
        for line in problem_input:
            start, end = [int(x) for x in line.strip().split('-')]
            
            ranges.append((start, end))
        
        ranges.sort(key = lambda x: x[0])
        visited = set([])
        merged_ranges = []
        
        for main_range in ranges:
            if main_range in visited:
                continue
            merged_range = main_range
            visited.add(main_range)
            for merging_range in ranges:
                if merging_range not in visited and self.can_be_merged(merged_range, merging_range):
                    merged_range = self.merge_ranges(merged_range, merging_range)
                    visited.add(merging_range)
            
            merged_ranges.append(merged_range)
        
        merged_ranges.sort(key = lambda x: x[0])
        
        start, end = merged_ranges[0]
        
        return end + 1 if start == 0 else start - 1


solver = Solver(3)
solver.solve()