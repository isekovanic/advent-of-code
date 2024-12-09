import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# Felt like I over-engineered this one, but it runs quite fast. Could have probably
# done it similar to part 2, however I felt it'd be more complicated that way considering
# we'd have to split ranges and that's never fun.
# For each data segment, we calculate its value by calculating the sum of the range multiplied
# by its ID. We can calculate the sum as the subtraction of triangular number formulae for each
# segment.
# For each space segment, we fill it with as many of the larger IDs as we can, starting from the
# right. Each time we do a full fill, we use the same trick as for data segments to calculate the
# result quickly. If a data segment doesn't entirely fit to fill it, we fill as much as we can and
# do the same calculation. Since we use up all of the numbers, we get rid of the spaces associated
# with the current right hand ID we're looking at.
class Solver(SolverCore):
    def sum_range(self, f, t):
        return t * (t + 1) // 2 - f * (f - 1) // 2
    def _solve(self, problem_input):
        disk_map = problem_input[0].strip()
        id_count = {}
        space_count = defaultdict(int)

        for i in range(len(disk_map)):
            idx = i // 2
            if i % 2 == 0:
                id_count[idx] = int(disk_map[i])
            else:
                space_count[idx] = int(disk_map[i])

        max_id = len(id_count)
        last_good = max_id - 1
        result = 0
        index = 0

        for i in range(max_id):
            data = id_count[i]
            spaces = space_count[i]

            if data == 0 and spaces == 0:
                continue

            new_data_index = index + data - 1
            result += i * self.sum_range(index, new_data_index)

            index += data

            while spaces > id_count[last_good] and last_good > i:
                new_data_count = id_count[last_good]
                result += last_good * self.sum_range(index, index + new_data_count - 1)
                index += new_data_count
                id_count[last_good] = 0
                space_count[last_good] = 0
                last_good -= 1
                spaces -= new_data_count

            if last_good <= i:
                continue
            result += last_good * self.sum_range(index, index + spaces - 1)
            index += spaces
            id_count[last_good] -= spaces
            space_count[i] = 0

        return result


solver = Solver(1928)
solver.solve()