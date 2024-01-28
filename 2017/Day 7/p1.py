import sys

sys.path.append('../../')

from Core import SolverCore

class Tower:
    def __init__(self, memory):
        self.parent = None
        self.children = []
        self.memory = memory

class Solver(SolverCore):
    def _solve(self, problem_input):
        towers = {}
        inheritance = {}
        
        for line in problem_input:
            children = []
            if '->' in line:
                line, children = line.strip().split(' -> ')
                children = children.split(', ')
            
            t_name, mem = line.strip().split(' ')
            mem = int(mem[1:-1])
            towers[t_name] = Tower(mem)
            if len(children):
                inheritance[t_name] = children
        
        for k, v in inheritance.items():
            towers[k].children = v
            for child in v:
                towers[child].parent = k
        
        for name, tower in towers.items():
            if tower.parent is None:
                return name

        return None


solver = Solver('tknk')
solver.solve()