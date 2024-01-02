import sys
from functools import reduce

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def find_combinations(self, target_sum, nb_combinations, current_combination = []):
        if target_sum == 0 and len(current_combination) == nb_combinations:
            return [current_combination]
        
        if len(current_combination) == nb_combinations - 1:
            return [current_combination + [target_sum]]
    
        combinations = []
        for i in range(target_sum + 1):
            updated_combination = current_combination + [i]
            updated_sum = target_sum - i
            combinations += self.find_combinations(updated_sum, nb_combinations, updated_combination)
    
        return combinations
    def _solve(self, problem_input):
        ingredients = []
        
        for line in problem_input:
            ingredient, properties = line.strip().split(': ')
            properties = [int(prop.split(' ')[1]) for prop in properties.split(', ')]
            
            ingredients += [tuple(properties)]
        
        ingredient_sum = 100
        ingredient_combinations = self.find_combinations(ingredient_sum, len(ingredients))
        
        result = 0
        
        for combination in ingredient_combinations:
            current_sum = [0 for _ in range(len(ingredients[0]))]
            
            for idx, ingredient in enumerate(ingredients):
                for prop_idx, prop in enumerate(ingredient):
                    current_sum[prop_idx] += prop * combination[idx]
            
            calories = current_sum.pop()
            
            if any([x < 0 for x in current_sum]) or calories != 500:
                continue
            
            result = max(result, reduce(lambda x, y: x * y, current_sum, 1))
            
        return result


solver = Solver(57600000)
solver.solve()