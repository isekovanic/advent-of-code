import sys
import re
import string

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict
from fractions import Fraction
from math import inf

# I absolutely loved this problem, even thought it took me a couple of hours to figure out.
# Before we begin, it is imperative that we make a couple of observations:
# - We can safely scrape the solution from the first part, as it can no longer be utilized
# - The problem asks us to compute the arbitrary amount of taps on any button so that the sum
#   of increments it leads to equals the input array
#
# For illustrative purposes, let us take the very first test case as an example:
#
# (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
#
# Since there are 6 buttons in total, let us denote the number of taps on each button as
# a, b, c, d, e and f respectively. Then, we may represent the test case in a different form:
#
# a * x3 + b * x1 + b * x3 + c * x2 + d * x2 + d * x3 + e * x0 + e * x2 + f * x0 + f * x1 = 3 * x0 + 5 * x1 + 4 * x2 + 7 * x3 = 3 * x0 + 5 * x1 + 4 * x2
# <=>
# x0 * (e + f) + x1 * (b + f) + x2 * (c + d + e) + x3 * (a + b + d) = 3 * x0 + 5 * x1 + 4 * x2 + 7 * x3 = 3 * x0 + 5 * x1 + 4 * x2 + 7 * x3 = 3 * x0 + 5 * x1 + 4 * x2
#
# which in turn produces the following system of equations for us:
#
# e + f = 3
# b + f = 5
# c + d + e = 4
# a + b + d = 7
#
# However, things aren't as simple as solving this system, as we have 4 equalities and 6 variables.
# This means we'll need to get a bit creative.
#
# Firstly, let us reduce the system as much as we can, getting us:
#
# e = 3 - f
# b = 5 - f
# c = 1 + f - d
# a = 2 + f - d
# d = d
# f = f
#
# Since we know that the presses always have to be integers and cannot be negative (duh), we can further
# apply some more constraints to this:
#
# e = 3 - f >= 0 and b = 5 - f >= 0, meaning f <= 3
# c = 1 + f - d >= 0 and a = 2 + f - d >= 0, meaning d <= f + 1
#
# This makes the search domain for these two free variables much more lenient.
# Now, what we're actually trying to minimize is a + b + c + d + e + f, or in other words, minimize:
#
# 11 + f - d
#
# For this, we want to have f be as small as possible and d be as large as possible. Given the extra
# constraints from above, we can easily figure out that for any f in [0, 3], the sum is:
#
# 11 + f - (f + 1) <=> 11 - 1 = 10
#
# and so the solution here is 10.
# Now we need to do the same thing, however in a generic manner.
class Solver(SolverCore):
    # Solve a system of linear equations of the form:
    #
    # sum(vars_in_eq) = rhs
    #
    # under the constraints that:
    #   - all variables are integers,
    #   - all variables are >= 0,
    #   - and we want to minimize the sum of all variables.
    #
    # The coefficients of the variables are implicitly 1 in each equation.
    # For example, an input like:
    #
    # [(['a', 'd', 'f'], 10), (['d', 'f'], 6)]
    #
    # represents the system:
    #
    # a + d + f = 10
    # d + f     = 6
    #
    # Returns the minimal possible value of the total sum of all variables, or
    # None if no such solution exists.
    #
    # Notes
    # -----
    # Algorithm overview:
    #
    # 1. Collect all distinct variable names across all equations and assign
    #    each an index. Build a matrix A and vector b such that A * x = b
    #    represents the system, where each row of A has 1s for variables
    #    present in that equation and 0s otherwise.
    #
    # 2. Run Gaussian elimination to reduce A to reduced row-echelon form
    #    (RREF). From this, identify:
    #    - pivot columns: variables that are determined by the equations
    #    - free columns: variables that can be chosen freely
    #
    # 3. Compute a simple upper bound U[j] for each variable x_j:
    #    - if x_j appears in an equation with RHS = r,
    #      then x_j <= r (since all variables are non-negative).
    #    - U[j] is taken as the minimum RHS over all equations containing x_j.
    #
    # 4. Define an inner helper `build_solution(free_values)` which:
    #    - takes a mapping from free variable indices to concrete integer values,
    #    - reconstructs all pivot variables using the RREF rows,
    #    - rejects any candidate where:
    #        * a pivot becomes non-integer
    #        * any variable is < 0 or > its upper bound U[j]
    #        * or any original equation sum != RHS
    #
    # If valid, it returns the full assignment vector x; otherwise None.
    #
    # 5. If there are no free variables, the system has at most one solution.
    #    We attempt to build that solution once and return its total sum
    #    (or None if it fails).
    #
    # 6. If there are free variables, but not more than `max_free`, we
    #    perform a DFS over the free variables only.
    #    Each free variable is brute-forced in the range [0, U[idx]].
    #    For each complete assignment to free variables, we:
    #    - call `build_solution`
    #    - if valid, compute sum(x)
    #    - track the minimal sum found
    #
    # 7. If no valid assignment is found, return None.
    #    Otherwise, return the minimal total sum.
    #
    # This approach leverages linear algebra (RREF) to collapse the problem
    # to a small number of free variables and then performs an exhaustive
    # but bounded search over just those degrees of freedom, enforcing the
    # integer and non-negativity constraints at reconstruction time.
    def solve_system(self, equations, max_free=4):
        # 1) Collect variable names and build A, b
        var_names = sorted({name for vars_in_eq, _ in equations for name in vars_in_eq})
        n = len(var_names)
        if n == 0:
            return {}, 0
    
        name_to_idx = {v: i for i, v in enumerate(var_names)}
        m = len(equations)
    
        A = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        b = [Fraction(0) for _ in range(m)]
    
        for i, (vars_in_eq, rhs) in enumerate(equations):
            for nm in vars_in_eq:
                A[i][name_to_idx[nm]] = Fraction(1)
            b[i] = Fraction(rhs)
    
        # 2) RREF to express pivot vars in terms of free vars
        row = 0
        pivot_cols = [-1] * m
    
        for col in range(n):
            # find pivot row
            pivot = None
            for r in range(row, m):
                if A[r][col] != 0:
                    pivot = r
                    break
            if pivot is None:
                continue
    
            # swap pivot into current row
            A[row], A[pivot] = A[pivot], A[row]
            b[row], b[pivot] = b[pivot], b[row]
    
            # normalize pivot row
            fac = A[row][col]
            A[row] = [v / fac for v in A[row]]
            b[row] /= fac
    
            # eliminate this column in all other rows
            for r in range(m):
                if r != row and A[r][col] != 0:
                    fac2 = A[r][col]
                    A[r] = [A[r][c] - fac2 * A[row][c] for c in range(n)]
                    b[r] -= fac2 * b[row]
    
            pivot_cols[row] = col
            row += 1
            if row == m:
                break
    
        pivots = [c for c in pivot_cols if c != -1]
        free_cols = [j for j in range(n) if j not in pivots]
        pivot_row_by_col = {c: r for r, c in enumerate(pivots)}
        k = len(free_cols)
    
        # 3) Upper bounds: if var appears in sum(...) = rhs, then var <= min(rhs)
        U = [0] * n
        for j, v in enumerate(var_names):
            rhs_vals = [rhs for vars_in_eq, rhs in equations if v in vars_in_eq]
            U[j] = min(rhs_vals) if rhs_vals else 0
    
        # Precompute indices for each equation (for fast checking)
        eq_var_indices = []
        rhs_list = []
        for vars_in_eq, rhs in equations:
            idxs = [name_to_idx[nm] for nm in vars_in_eq]
            eq_var_indices.append(idxs)
            rhs_list.append(rhs)
    
        best = None
        best_sum = inf
    
        # Given a dict { free_col_index: value }, build the full solution x.
        # Returns list of ints or None if:
        # - some pivot becomes non-integer
        # - some var < 0 or > U
        # - or equations not satisfied
        def build_solution(free_values):
            x = [0] * n
    
            # set free vars
            for idx in free_cols:
                x[idx] = free_values.get(idx, 0)
    
            # compute pivot vars from RREF
            for c in reversed(pivots):
                r = pivot_row_by_col[c]
                s = b[r]
                rowA = A[r]
                for j in range(n):
                    if j == c:
                        continue
                    coeff = rowA[j]
                    if coeff != 0:
                        s -= coeff * x[j]
    
                if s.denominator != 1:
                    return None  # pivot would be fractional ?
                v = int(s)
                if v < 0:
                    return None  # violates non-negativity
                x[c] = v
    
            # check bounds 0 <= x[j] <= U[j]
            for j in range(n):
                if x[j] < 0 or x[j] > U[j]:
                    return None
    
            # check all original equations exactly
            for idxs, rhs in zip(eq_var_indices, rhs_list):
                if sum(x[j] for j in idxs) != rhs:
                    return None
    
            return x
    
        # No free vars: unique solution (if any)
        if k == 0:
            sol = build_solution({})
            if sol is None:
                return None
            return sum(sol)
    
        # More free vars than we want to brute-force
        if k > max_free:
            raise ValueError(f"Too many free variables ({k}) - this solution sucks for those :(")
    
        # 4) Brute force only the free variables
        free_idx_list = list(free_cols)
    
        def dfs(pos, free_values):
            nonlocal best, best_sum
    
            if pos == k:
                sol = build_solution(free_values)
                if sol is None:
                    return
                ssum = sum(sol)
                if ssum < best_sum:
                    best_sum = ssum
                    best = sol
                return
    
            idx = free_idx_list[pos]
            # free var domain is [0, U[idx]]
            for val in range(0, U[idx] + 1):
                free_values[idx] = val
                dfs(pos + 1, free_values)
            free_values.pop(idx, None)
    
        dfs(0, {})
    
        if best is None:
            return None
    
        return best_sum
    
    def solve_machine(self, configuration, buttons):
        system = self.collect_system(configuration, buttons)
        
        return self.solve_system(system)
        
    def collect_system(self, configuration, buttons):
        left_hands = defaultdict(list)
        
        for idx, button in enumerate(buttons):
            variable = string.ascii_lowercase[idx]
            for eq in button:
                left_hands[eq].append(variable)
                
        equations = []
        
        for idx, right_hand in enumerate(configuration):
            equations.append((left_hands[idx], right_hand))
            
        return equations
        

    def _solve(self, problem_input):
        result = 0
        
        for line in problem_input:
            _, *buttons, conf = line.split(' ')
            buttons = [[int(x) for x in re.findall('[0-9]+', button)] for button in buttons]
            
            configuration = [int(x) for x in re.findall('[0-9]+', conf)]
            
            result += self.solve_machine(configuration, buttons)

        return result


solver = Solver(33)
solver.solve()
