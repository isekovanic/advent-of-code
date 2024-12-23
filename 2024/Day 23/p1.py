import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict
from itertools import combinations

# This problem revolves around finding all cliques with size 3 in a graph that
# also contain a computer that begins with 't'. Since the clique size is very
# limited, we can easily brute-force the solution by keeping the graph as a
# dictionary of sets and quickly being able to confirm all combinations of
# neighbours of any node beginning with 't'.
class Solver(SolverCore):
    def _solve(self, problem_input):
        connections = [tuple(x.strip().split('-')) for x in problem_input]
        
        edges = defaultdict(set)
        potential_computers = set([])
        
        for connection in connections:
            f, t = connection
            if f[0] == 't':
                potential_computers.add(f)
            if t[0] == 't':
                potential_computers.add(t)
            
            edges[f].add(t)
            edges[t].add(f)
        
        result = 0
        cliques = set([])
        for computer in potential_computers:
            neighbours = edges[computer]
            for pair in combinations(neighbours, 2):
                f, s = pair
                key = tuple(sorted([computer, f, s]))
                if key in cliques:
                    continue
                cliques.add(key)
                result += s in edges[f]

        return result


solver = Solver(0)
solver.solve()