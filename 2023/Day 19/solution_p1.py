import sys

sys.path.append('../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		workflows_input, parts_input = problem_input

		parts = [eval(part.replace('=', ':').replace('{', '{"').replace(':', '":').replace(',', ',"')) for part in parts_input]
		
		workflows = {}
		for workflow in workflows_input:
			name, value = workflow.split('{')
			workflows[name] = value[:-1].split(',')

		start_workflow = 'in'

		accepted = []

		for part in parts:
			current_workflow = start_workflow
			x, m, a, s = [part[k] for k in ('x', 'm', 'a', 's')]

			while current_workflow != 'A' and current_workflow != 'R':
				for rule in workflows[current_workflow]:
					rule_parts = rule.split(':')
					if len(rule_parts) == 1:
						rule_parts = ['True', rule_parts[0]]

					predicate, destination = rule_parts

					if eval(predicate):
						current_workflow = destination
						break

			if current_workflow == 'A':
				accepted += [(x, m, a, s)]
	
		result = 0

		for part in accepted:
			result += sum(part)
		
		return result

	def read_input(self, file):
		read_input = open(file, 'r')

		blocks = [block.split('\n') for block in read_input.read().split('\n\n')]

		return blocks

solver = Solver(19114)
solver.solve()