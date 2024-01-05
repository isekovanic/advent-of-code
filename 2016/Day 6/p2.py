import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
    def _solve(self, problem_input):
        repetitions = {i: {} for i in range(len(problem_input[0].strip()))}
        for line in problem_input:
            for i in range(len(line.strip())):
                char = line[i]
                if char not in repetitions[i]:
                    repetitions[i][char] = 0
                repetitions[i][char] += 1
        
        result = ''
        for i in range(len(repetitions.keys())):
            result += sorted(repetitions[i].items(), key = lambda x: x[1])[0][0]
            
        return result


solver = Solver('advent')
solver.solve()