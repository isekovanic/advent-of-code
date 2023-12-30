import sys

sys.path.append('../../')

from Core import SolverCore

directions = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}
class Solver(SolverCore):
    def visit_houses(self, start, moves):
        start = (0, 0)
        visited = set([start])
        
        for char in moves:
            x, y = directions[char]
            
            s_x, s_y = start
            start = (s_x + x, s_y + y)
            visited.add(start)
        
        return visited
    def _solve(self, problem_input):
        moves = problem_input[0].strip()
        
        santa_moves = []
        robot_moves = []
        
        for i, move in enumerate(moves):
            if i % 2 == 0:
                santa_moves += [move]
            else:
                robot_moves += [move]
            
        santa_visited = self.visit_houses((0, 0), santa_moves)
        robot_visited = self.visit_houses((0, 0), robot_moves)
        
        return len(santa_visited.union(robot_visited))


solver = Solver(11)
solver.solve()