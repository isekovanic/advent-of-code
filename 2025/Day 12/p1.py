import sys

sys.path.append('../../')

from Core import SolverCore
from collections import defaultdict

# This was an interesting last problem, significantly more difficult that the last problems from
# previous years !
# The core idea of this solution is based on checking whether a given multiset of small 2D shapes
# can be placed on a MxN grid without overlaps, allowing rotations and reflections (as the problem
# states). Since I'm still sticking to Python for AoC, I could abuse the hell out of every dirty bit
# manipulation trick I could think of in order to make computation time reasonable. Even still, this
# solution runs for ~3 minutes or so (on my input at least), but finishes after a while. I'm fairly
# certain that there are either more ways to prune or better solutions out there that don't keep 2500
# bits long bitmasks, but I decided to stop here as it was good enough for me.
# The core idea revolves around keeping one huge bitmask that represents the board (with its currently
# occupied fields).
#
# Bit i corresponds to board cell i (i = y * M + x):
# - 1 means the cell is already "decided" (either covered by a placed shape OR explicitly declared empty)
# - 0 means the cell is still free/undecided
#
# Then, we precompute every possible placement of every possible shape (original, rotated and mirrored) and
# keep it as a separate bitmask, signifying which board cells that shape would occupy. While this already
# sounds horrendous, Python seems to be quite adept at handling such extremely large numbers and then overlap
# tests with the current board shape becomes trivial and very fast, through (m & occupied) == 0. Placing a
# piece of the board is also trivial and fast, through occupied |= m.
#
# Along the way, various other heuristics were used (which are explained in the code itself) that sped things
# up a little bit. One of the things that helped the most here is the MRV heuristic used, by picking the
# "hardest to place" shapes first at all times. My logic at the time was that there's more room for them,
# but I quickly gave up on this idea. And yet, it helps significantly and by a large factor. While I don't
# have an empiric proof of why that is, I'll treat it more as an educated guess or intuitive type of decision.
# One thing this does for sure is cutting branches out that would anyway fail very quickly (as handling the
# shapes will less options first does not do a ton of branching out and computations, just to reach a dead end
# towards the end of the recursion itself. This is basically the only justification I relied on.
#
# After all of the precomputations are done and everything is in order, the DFS itself that handles the backtracking
# is very easy. We essentially try out as many possibilities as we can, while pruning everywhere we can as well.

# Utils

# Convert an ASCII shape into a list of (x, y) coordinates, for easier
# consumption later.
def parse_shape(lines):
    pts = []
    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            if ch == "#":
                pts.append((x, y))
    return pts


# Shift a shape so that its top-left corner is at (0,0), then sort the
# points in order to make them hashable.
def normalize(pts):
    minx = min(x for x, _ in pts)
    miny = min(y for _, y in pts)
    return tuple(sorted((x - minx, y - miny) for x, y in pts))


# Rotate a shape 90 degrees counter-clockwise around (0,0).
def rot90(pts):
    return [(y, -x) for x, y in pts]


# Reflect a shape across the Y axis.
def flip_y(pts):
    return [(-x, y) for x, y in pts]

# Generate all unique orientations of a shape, including rotations and reflections.
def all_variants(pts):
    seen = set()
    cur = pts
    for _ in range(4):
        seen.add(normalize(cur))
        seen.add(normalize(flip_y(cur)))
        cur = rot90(cur)
    return [list(v) for v in seen]


# Compute the bounding box size of a normalized shape.
def bbox(pts):
    maxx = max(x for x, _ in pts)
    maxy = max(y for _, y in pts)
    return maxx + 1, maxy + 1


# Iterate over the indices of bits that are set to 1 in an integer.
def iter_set_bits(x):
    while x:
        b = x & -x
        yield (b.bit_length() - 1)
        x ^= b


# For every shape, for every rotation and reflection of that shape and
# for every position where it fits on the board, compute a bitmask that
# represents exactly which board cells it would occupy. Then store each
# such bitmask under every board cell that it touches, so that later we
# can quickly find all placements that cover a specific cell.
def build_index(w, h, shapes_ascii):
    base_pts = [parse_shape(s) for s in shapes_ascii]
    areas = [len(p) for p in base_pts]

    placements_by_type_cell = [defaultdict(list) for _ in shapes_ascii]

    for t, pts in enumerate(base_pts):
        for v in all_variants(pts):
            v_norm = normalize(v)
            bw, bh = bbox(v_norm)
            for oy in range(h - bh + 1):
                for ox in range(w - bw + 1):
                    m = 0
                    cells = []
                    for x, y in v_norm:
                        idx = (oy + y) * w + (ox + x)
                        m |= (1 << idx)
                        cells.append(idx)
                    for c in cells:
                        placements_by_type_cell[t][c].append(m)

    return areas, placements_by_type_cell

class Solver(SolverCore):
    
    # Solve for one grid, given the ASCII shapes
    def solve_pack(self, w, h, shapes_ascii, counts):
        areas, placements_by_type_cell = build_index(w, h, shapes_ascii)
    
        board_area = w * h
        need = sum(c * a for c, a in zip(counts, areas))
        
        # exit early if there is no way the solution will fit, this helps
        # for a ridiculously surprising number of cases for the main input
        if need > board_area:
            return False
    
        empties_allowed = board_area - need
    
        # I found that larger first significantly speeds things up (by about a
        # minute for my input). I'm sure there's a fancy explanation why, but I
        # can't seem to figure it out and found it through experimentation.
        type_order = sorted(range(len(counts)), key=lambda t: -areas[t])
    
        remaining = counts[:]
        dead_ends = set()
    
        # Choose the next board cell to branch on using a minimum remaining values heuristic.
        # What this basically means is that we prefer a free cell that currently has the fewest
        # valid placements that could cover it. This tends to force decisions early and reduces
        # the search branching factor, for lack of a more sophisticated algorithm.
        def choose_mrv_cell(occupied):
            full = (1 << board_area) - 1
            # swap out all 0s for 1s (and vice versa) and bind it to only the board region
            free = (~occupied) & full
    
            best_cell = None
            best_opts = None
            best_len = 10**9
    
            scanned = 0
            # Iterate over some currently free (undecided) board cells. For each candidate cell,
            # count how many valid placements could cover it and pick the cell with the fewest
            # options to branch on to next.
            for cell in iter_set_bits(free):
                # calculate the candidate placements for a cell
                opts = []
                for t in type_order:
                    if remaining[t] == 0:
                        continue
                    for m in placements_by_type_cell[t].get(cell, ()):
                        if (m & occupied) == 0:
                            opts.append((t, m))
                            
                L = len(opts)
                if L < best_len:
                    best_len = L
                    best_cell = cell
                    best_opts = opts
                    if best_len <= 1:
                        break
                scanned += 1
                # do not try deeper than this, it's just another experimental heuristic I added
                # to bypass going too deep while keeping pruning sane
                if scanned >= 80:
                    break
    
            return best_cell, best_opts
    
        def dfs(occupied, empties_used):
            key = (occupied, tuple(remaining), empties_used)
            if key in dead_ends:
                return False
    
            # capacity pruning
            free_cells = board_area - occupied.bit_count()
            if sum(remaining[t] * areas[t] for t in range(len(remaining))) > free_cells:
                dead_ends.add(key)
                return False
    
            # empty budget pruning
            if empties_used > empties_allowed:
                dead_ends.add(key)
                return False
    
            # done placing all pieces
            if all(r == 0 for r in remaining):
                return True
    
            cell, opts = choose_mrv_cell(occupied)
            if cell is None:
                dead_ends.add(key)
                return False
    
            bit = 1 << cell
    
            # if nothing can cover this cell, skipping is forced
            if not opts:
                if empties_used < empties_allowed and dfs(occupied | bit, empties_used + 1):
                    return True
                dead_ends.add(key)
                return False
    
            # try placements
            for t, m in opts:
                remaining[t] -= 1
                if dfs(occupied | m, empties_used):
                    return True
                remaining[t] += 1
    
            if empties_used < empties_allowed and dfs(occupied | bit, empties_used + 1):
                return True
    
            dead_ends.add(key)
            return False
    
        return dfs(0, 0)
    
    def _solve(self, problem_input):
        *blocks, grids = problem_input
        
        for block in blocks:
            block.pop(0)
            
        result = 0
        
        for idx, grid in enumerate(grids):
            dims, counts = grid.split(': ')
            w, h = [int(x) for x in dims.split('x')]
            counts = [int(x) for x in counts.split(' ')]
            
            result += self.solve_pack(w, h, blocks, counts)
            
        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        
        return [block.split('\n') for block in read_input.read().split('\n\n')]

solver = Solver(2)
solver.solve()