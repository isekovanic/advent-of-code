import sys

sys.path.append('../../')

from Core import SolverCore

operations = {
    'on': lambda x: x + 1,
    'off': lambda x: max(x - 1, 0),
    'toggle': lambda x: x + 2
}
class Solver(SolverCore):
    def find_operation(self, instruction):
        if instruction.startswith('turn on'):
            return 'on'
        if instruction.startswith('turn off'):
            return 'off'
        return 'toggle'
    def _solve(self, problem_input):
        grid = [[0 for _ in range(1000)] for _ in range(1000)]
        
        for instruction in problem_input:
            operation = self.find_operation(instruction)
            instruction = instruction.replace('turn on ', '').replace('turn off ', '').replace('toggle ', '')
            
            start, end = instruction.split(' through ')
            s_x, s_y = [int(x) for x in start.split(',')]
            e_x, e_y = [int(x) for x in end.split(',')]
            
            for i in range(s_x, e_x + 1):
                for j in range(s_y, e_y + 1):
                    grid[i][j] = operations[operation](grid[i][j])

        return sum([sum(row) for row in grid])


solver = Solver(1001996)
solver.solve()