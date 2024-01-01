import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def calculate_sum(self, json):
        result = 0
        values = json.values() if type(json) is dict else json
        for value in values:
            value_type = type(value)
            if value_type is int:
                result += value
            if value_type is dict or value_type is list:
                result += self.calculate_sum(value)
        
        return result
    def _solve(self, problem_input):
        json_string = problem_input[0].strip()
                
        return self.calculate_sum(eval(json_string))


solver = Solver(3, { 'test': 'input_test_p1.txt' })
solver.solve()