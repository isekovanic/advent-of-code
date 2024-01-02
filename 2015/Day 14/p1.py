import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        reindeer_speeds = []
        
        for line in problem_input:
            _, metadata = line.strip().split(' can fly ')
            speed_meta, rest = metadata.split(' seconds, but then must rest for ')
            rest = int(rest.split(' ')[0])
            speed, time = [int(x) for x in speed_meta.split(' km/s for ')]
            
            reindeer_speeds += [(speed, time, rest)]
        
        result = 0
        race_time = 2503
        
        for speed, time, rest in reindeer_speeds:
            cycle = time + rest
            cycle_travel_length = speed * time
            
            cycles = race_time // cycle
            time_left = race_time - cycles * cycle
            
            result = max(result, cycles * cycle_travel_length + min(time_left, time) * speed)
        
        return result


solver = Solver(2660)
solver.solve()