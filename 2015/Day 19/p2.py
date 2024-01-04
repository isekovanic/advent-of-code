import sys
from random import shuffle

sys.path.append('../../')

from Core import SolverCore

# This one was particularly difficult for me. This quasy-solution is based on the following assumptions:
# - There is always a single path to getting from 'e' to our input. If this weren't the case, we could apply
#	the same solution but for every possible combination of replacements (instead of doing it for all 43 of them
#	we can reduce it down to like a 10 or something and then fill in the rest, as anyway not all mappings even appear
#	within the input string)
# - Suppose we have 2 mappings described as X -> AB and 3 mappings Y -> TR. We will notice that these 2 are either:
#	1. Completely disjunct (meaning we can replace them simulataneously without hurting the credibility of our string).
#	2. Enveloping each other (so we would have something like ATRB or similar in here), meaning we have to replace TR first and then AB.
#	3. They overlap with each other (for example, SiSi and SiCa do this since you can have a segment of the string SiSiCa and this is
#	   where it gets tricky).
# - This allows us to conclude that while it does not matter in which order we perform the replacement operations (or that
#	we do them as described in the problem description), it DOES matter which mapping is sorted out first; and then we can proceed
#	with doing the replacements in real time across the entire string.
# - Whenever a solution does not exist, it basically means we've reached a dead end and cannot do any more replacements and have to restart.
# With these assumptions in mind, we can construct quite a silly solution such as mine that basically runs the program for a random shuffle
# of the replacements until we find string 'e'. It turns out that this actually works quite fast and finds a solution incredibly quickly. One
# final optimization we do is the fact that we do the entire thing backwards, or rather than finding in how many steps 'e' can reach our input,
# we find the number of steps to reduce our input to 'e'. While I'm 100% sure we can find a rule by which we need to sort the input replacements
# (for example the one I mentioned above, whenever a mapping envelops another) I was not able to find anything significant or deterministic.

class Solver(SolverCore):
	def _solve(self, problem_input):
		replacements, molecule = problem_input
		atom_map = {}
		for replacement in replacements.split('\n'):
			start, end = replacement.split(' => ')
			atom_map[end] = start
		
		atom_map_items = list(atom_map.items())
		current_molecule = molecule
		result = 0
		
		while current_molecule != 'e':
			shuffle(atom_map_items)
			current_molecule = molecule
			result = 0
			prev_molecule = ''
			while prev_molecule != current_molecule:
				prev_molecule = current_molecule
				for key, value in atom_map_items:
					if key in current_molecule:
						cnt = current_molecule.count(key)
						current_molecule = current_molecule.replace(key, value)
						result += cnt

		return result
	def read_input(self, file):
		read_input = open(file, 'r')
		return read_input.read().split('\n\n')

solver = Solver(6, { 'test': 'input_test_p2.txt' })
solver.solve()