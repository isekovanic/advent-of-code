import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def find_winners(self, reindeer_speeds, race_time):
        distances = {}
        for reindeer, (speed, time, rest) in reindeer_speeds.items():
            cycle = time + rest
            cycle_travel_length = speed * time
            
            cycles = race_time // cycle
            time_left = race_time - cycles * cycle
            
            distances[reindeer] = cycles * cycle_travel_length + min(time_left, time) * speed
        
        winners = []
        for reindeer, distance in distances.items():
            if len(winners) == 0:
                winners += [reindeer]
            else:
                if distances[winners[0]] < distances[reindeer]:
                    winners = [reindeer]
                elif distances[winners[0]] == distances[reindeer]:
                    winners += [reindeer]
        
        return winners
    def _solve(self, problem_input):
        reindeer_speeds = {}
        
        for line in problem_input:
            reindeer, metadata = line.strip().split(' can fly ')
            speed_meta, rest = metadata.split(' seconds, but then must rest for ')
            rest = int(rest.split(' ')[0])
            speed, time = [int(x) for x in speed_meta.split(' km/s for ')]
            
            reindeer_speeds[reindeer] = (speed, time, rest)
        
        points = {reindeer: 0 for reindeer in reindeer_speeds.keys()}
        race_time = 2503
        
        for i in range(1, race_time + 1):
            winners = self.find_winners(reindeer_speeds, i)
            
            for winner in winners:
                points[winner] += 1
        
        return max(points.values())


solver = Solver(1564)
solver.solve()