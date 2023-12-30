import sys
import math

sys.path.append('../../../')

from Core import SolverCore

class Solver(SolverCore):
	def _solve(self, problem_input):

		workflows_input, _ = problem_input
		
		workflows = {}
		for workflow in workflows_input:
			name, value = workflow.split('{')
			workflows[name] = value[:-1].split(',')

		start_workflow = 'in'
		start_ranges = {
			'x': (1, 4000),
			'm': (1, 4000),
			'a': (1, 4000),
			's': (1, 4000)
		}
		# each element in the format of (possible_ranges, workflow)
		queue = [(start_ranges, start_workflow)]
		accepted = []

		while queue:
			current_ranges, current_workflow = queue.pop(0)

			if current_workflow == 'A':
				accepted += [current_ranges]
				continue
			if current_workflow == 'R':
				continue

			for rule in workflows[current_workflow]:
				rule_parts = rule.split(':')
				# according to the problem statement, this always comes at the end
				if len(rule_parts) == 1:
					queue += [(current_ranges.copy(), rule_parts[0])]
				else:
					predicate, destination = rule_parts

					# by looking at the test cases, we assume that predicates will always be
					# strict inequalities
					if '<' in predicate:
						prop, value = predicate.split('<')
						value = int(value) - 1

						prop_range = current_ranges[prop]

						r_s, r_e = prop_range

						if value >= r_e:
							queue += [(current_ranges.copy(), destination)]
							break # break early, the entire range fits
						elif r_s <= value < r_e:
							new_ranges = current_ranges.copy()
							new_ranges[prop] = (r_s, value)
							queue += [(new_ranges.copy(), destination)]
							current_ranges[prop] = (value + 1, r_e)
					else:
						prop, value = predicate.split('>')
						value = int(value) + 1

						prop_range = current_ranges[prop]

						r_s, r_e = prop_range

						if value <= r_s:
							queue += [(current_ranges.copy(), destination)]
							break # break early, the entire range fits
						elif r_s < value <= r_e:
							new_ranges = current_ranges.copy()
							new_ranges[prop] = (value, r_e)
							queue += [(new_ranges.copy(), destination)]
							current_ranges[prop] = (r_s, value - 1)
		
		return sum([eval('*'.join([str(s - f + 1) for f, s in ranges.values()])) for ranges in accepted])

	def read_input(self, file):
		read_input = open(file, 'r')

		blocks = [block.split('\n') for block in read_input.read().split('\n\n')]

		return blocks

solver = Solver(167409079868000)
solver.solve()