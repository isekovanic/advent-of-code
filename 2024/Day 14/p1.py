import sys
import re
import math

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        robots = [[int(x) for x in re.findall('-?[0-9]+', line.strip())] for line in problem_input]
        # uncomment for example case in the problem description
        # dimx, dimy = 11, 7
        dimx, dimy = 101, 103
        
        quadrants = [0, 0, 0, 0]
        
        for robot in robots:
            sx, sy, vx, vy = robot
            
            ex, ey = (sx + vx * 100) % dimx, (sy + vy * 100) % dimy
            
            if 0 <= ex < dimx // 2 and 0 <= ey < dimy // 2:
                quadrants[0] += 1
            elif 0 <= ex < dimx // 2 and dimy // 2 < ey < dimy:
                quadrants[1] += 1
            elif dimx // 2 < ex < dimx and 0 <= ey < dimy // 2:
                quadrants[2] += 1
            elif dimx // 2 < ex < dimx and dimy // 2 < ey < dimy:
                quadrants[3] += 1

        return math.prod(quadrants)


solver = Solver(12)
solver.solve()