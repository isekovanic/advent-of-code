import sys

sys.path.append('../../')

from Core import SolverCore

reader_values = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

greater_checks = ['cats', 'trees']
fewer_checks = ['pomeranians', 'goldfish']
class Solver(SolverCore):
    def check_value(self, key, value):
        reader_val = reader_values[key]
        if key in greater_checks:
            return reader_val < value
        if key in fewer_checks:
            return reader_val > value
        
        return reader_val == value
    def _solve(self, problem_input):
        for idx, line in enumerate(problem_input):
            sue_values = {}
            memory_values = line.strip().split(', ')
            memory_values[0] = ': '.join(memory_values[0].split(': ')[1:])
            for memory_value in memory_values:
                key, value = memory_value.split(': ')
                sue_values[key] = int(value)
            
            if all(self.check_value(k, v) for k, v in sue_values.items()):
                return idx + 1
        
        # should not happen
        return -1


solver = Solver(4)
solver.solve()