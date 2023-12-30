import sys

sys.path.append('../../../')

from Core import SolverCore

button_presses = 1000

class Module:
	def __init__(self, mod_type):
		self.type = mod_type
		if self.type == '%':
			self.state = 0
		else:
			self.state = {}

	def update_state(self, pulse, origin):
		if self.type == '%':
			if pulse == 0:
				self.state += 1
				self.state %= 2
		else:
			if origin in self.state:
				self.state[origin] = pulse

	def send_pulse(self, pulse):
		if self.type == '%':
			return None if pulse == 1 else self.state
		else:
			if all(x == 1 for x in self.state.values()):
				return 0
			return 1

class Solver(SolverCore):
	def _solve(self, problem_input):

		cables = {}
		modules = {}

		for line in problem_input:
			start, end = line.split(' -> ')
			if '%' in start or '&' in start:
				modules[start[1:]] = Module(start[0])
			start = start.replace('%', '').replace('&', '')

			end = end.strip().split(', ')
			cables[start] = end

		for start, destinations in cables.items():
			for destination in destinations:
				if destination in modules and modules[destination].type == '&':
					modules[destination].state[start] = 0

		low = 0
		high = 0

		for _ in range(button_presses):
			# the queue state will be of type (origin, destination, pulse)
			queue = []

			low += 1 # the low pulse sent to the broadcaster

			# initialize
			for destination in cables['broadcaster']:
				queue += [('', destination, 0)]
				low += 1

			while queue:
				origin, current_module, pulse = queue.pop(0)

				modules[current_module].update_state(pulse, origin)
				new_pulse = modules[current_module].send_pulse(pulse)

				for destination in cables[current_module]:
					low += new_pulse == 0
					high += new_pulse == 1
					if new_pulse != None and destination in modules:
						queue += [(current_module, destination, new_pulse)]
		
		return low * high

solver = Solver(32000000, { 'test': 'input_test_p1.txt' })
solver.solve()