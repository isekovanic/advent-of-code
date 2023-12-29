import sys

sys.path.append('../../../')

from Core import SolverCore

# Disclaimer: I have yet to find a way to generalize this day's Problem 2 without legitimately spending
# a couple of days crafting a solution. Some points worth mentioning:
# - If we have more than 1 input towards "rx", we can repeat the procedure for all of them separately and 
#	then proceed to find the LCM between each one of them. Considering that the point at which these would
#	produce a "high" pulse is also cyclic (since all of its requirements also are, easy to deduce), this would
#	give us the correct answer. We can also do this recursively as deep as we need, albeit it would be quite a
#	bit slower.
# - What would we do if we notice that there are way too many conjunction modules and the repetition cycle
#	starts deeper than anticipated (which is at depth 2 for the current solution) ? In this case, we can precompute
# 	exactly where the cycles start. If we think about it, everything here should be cyclic so in the worst case
#	we might need to go as far back as the "broadcaster" module and start there. A cycle has to start at some
#	point due to the nature of the problem so that way we can know how far we should peek.
# - It is not implied that only conjunction modules will ever output to "rx". If this is not the case, then we 
#	have to take the separate cycles of those modules into account as well (these might be a little tricky, considering
#	their cycles might not be as clear to catch, although they should be relatively small).
# - For what it's worth, from all of the possible inputs I've seen so far it is definitely the case that "rx" always
#	has a single input which is a conjuction module and that module only has inputs that are always conjunction modules too.
#	If this weren't the case, a simple brute force could also quite easily work due to how easily the other modules switch
#	between states.

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
	def gcd(self, x, y):
		if y == 0:
			return x
		return self.gcd(y , int(x % y))

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

		# assumption 1) - only one module feeds into rx and it's a conjuction one

		rx_in = None
		for start, destinations in cables.items():
			if 'rx' in destinations:
				rx_in = start

		# assumption 2) - the modules that feed into rx_in are always conjuction modules as well and we will
		#				  denote them as rx_in_inputs from now on
		#
		# Based on assumptions 1) and 2), for rx to receive a "low" pulse we need all of the modules
		# in rx_in_inputs to be "high". Hence, we make:
		# assumption 3) - each module in rx_in_inputs fires a "high" pulse in a reasonable amount of time and 
		# 				  on a given interval (idependent of the rest)
		# To confirm this, we can easily check it by uncommenting the code under figure "util 1)" and see what
		# the value of the state for rx_in is at every iteration. We can also see that the value stays persistent
		# during each iteration for every state, meaning we can divide the intervals by iterations and do not have
		# to do it by state changes (actions within each iteration). To confirm that each cycle is the same length,
		# we can do a sampling test through uncommenting the code under figure "util 2)". Albeit this is not a proof
		# that it works, it's good enough so that we can make some educated guesses.

		iterations = 0
		intervals = {key: [] for key in modules[rx_in].state.keys()}
		min_seen_iterations = 2

		while True:
			iterations += 1
			# the queue state will be of type (origin, destination, pulse)
			queue = []

			# initialize
			for destination in cables['broadcaster']:
				queue += [('', destination, 0)]

			while queue:
				for key, entry in modules[rx_in].state.items():
					if entry == 1:
						intervals[key] += [iterations] if iterations not in intervals[key] else []
				# ==========
				# util 1)
				# Uncomment the code below to confirm the repetition of all values in rx_in_inputs
				# ==========
				# if 1 in modules[rx_in].state.values():
				# 	print(modules[rx_in].state, iterations)
				# ==========
				origin, current_module, pulse = queue.pop(0)

				modules[current_module].update_state(pulse, origin)
				new_pulse = modules[current_module].send_pulse(pulse)

				for destination in cables[current_module]:
					if new_pulse != None and destination in modules: 
						queue += [(current_module, destination, new_pulse)]

			# ==========
			# util 2)
			# Uncomment the line below to confirm (not heuristically, but by getting a lot more samples) that all of
			# the intervals happen on the same cycle. The number can be increased if you need more samples.
			# ==========
			# min_seen_iterations = 100
			# ==========

			if all(len(value) > min_seen_iterations for key, value in intervals.items()):
				break

		valid_intervals = [] # the names of the items do not matter, so keeping them in a list
		for key, value in intervals.items():
			# this is mostly here because of util 2) - it is obviously redundant for the final solution
			if len(set([s - f for f, s in zip(value, value[1:])])) == 1:
				valid_intervals += [value[1] - value[0]]
			else:
				raise Exception('The interval is not cyclic ! The assumptions are incorrect.')

		result = valid_intervals[0]
		for cycle in valid_intervals:
			result = result * cycle / self.gcd(result, cycle)

		return int(result)

solver = Solver()
solver.solve()