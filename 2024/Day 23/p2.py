import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# The expansion of part 1 is a textbook Bron-Kerbosch problem ! It's been ages
# since I've been able to use this one. It's the de-facto go-to algorithm when
# it comes to finding the largest clique in a graph whenever we have a really
# sparse one. Considering that there are more than 250000 potential edges out
# of which only 3000 and something are used in the inputs, the algorithm is
# performant and produces an answer really quickly.
class Solver(SolverCore):
    def bron_kerbosch(self, R, P, X, graph):
        if not P and not X:
            yield R
        while P:
            v = P.pop()
            new_R = R | {v}
            yield from self.bron_kerbosch(new_R, P & graph[v], X & graph[v], graph)
            X.add(v)
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
            
        P = set(edges.keys())
        R = set([])
        X = set([])
        max_clique = set([])
    
        for clique in self.bron_kerbosch(R, P, X, edges):
            if len(clique) > len(max_clique):
                max_clique = clique
        
        return ','.join(sorted(list(max_clique)))


solver = Solver('co,de,ka,ta')
solver.solve()