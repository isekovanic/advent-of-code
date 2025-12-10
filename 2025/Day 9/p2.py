import sys

sys.path.append('../../')

from Core import SolverCore

# This one took me a very, very long time to solve. The crux of the problem becomes
# finding the largest axis-aligned rectangle that fits entirely inside a simple orthogonal
# polygon described by its integer vertex coordinates.
#
# Approach:
# - Parse the polygon vertices from input and close the polygon
# - Precompute vertical and horizontal edges to quickly test whether a candidate
#   rectangle's edge is crossed by any polygon edge
# - For remaining candidates, reject any whose interior is intersected by a
#   polygon edge, and finally confirm validity by checking that a representative
#   interior point lies inside the polygon using an even-odd ray casting test
#
# Essentially, if the polygon's edge crosses our rectangle we can be sure that it does not
# fit inside of the polygon. However, not crossing it does not mean that it fits entirely.
# For example, we can have a candidate be a rectangle of width 1, lying on the outskirts of
# the polygon (not intersecting and even though it CAN fit, it is not inside). Hence why we
# need to also check some point for validity (any point belonging to the rectangle will do).
# We do this by implementing rudimentary orthogonal ray-casting, so that we're sure that it
# is indeed inside. If at least one point is inside and there are no intersections with the
# polygon's edges, we can safely assume that the rectangle indeed fits and is present inside
# and so we can count it towards the maximum result calculation.
class Solver(SolverCore):
    # Checks if the rectangle edges intersect with any of the polygon's edges.
    # We will ignore edge cases where the rectangle lies exactly on a polygon edge.
    def intersects_edges(self, p1, p2, v_edges, h_edges):
        x1, y1 = p1
        x2, y2 = p2
        
        x_min, x_max, y_min, y_max = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        
        # vertical segments
        for ex, ey0, ey1 in v_edges:
            if x_min < ex < x_max and max(ey0, y_min) < min(ey1, y_max):
                return True
    
        # horizontal segments
        for ey, ex0, ex1 in h_edges:
            if y_min < ey < y_max and max(ex0, x_min) < min(ex1, x_max):
                return True
    
        return False
    
    # Even-odd ray casting algorithm.
    # Will return True if (px, py) lies strictly inside the polygon.
    def is_in_polygon(self, polygon, point):
        px, py = point
        intersections = 0
        n = len(polygon)
    
        for i in range(n - 1):
            x1, y1 = polygon[i]
            x2, y2 = polygon[i + 1]
    
            y1f, y2f = float(y1), float(y2)
            x1f, x2f = float(x1), float(x2)
    
            # Does the horizontal ray at y = py intersect edge (x1, y1) - (x2, y2) ?
            if (y1f > py) != (y2f > py):
                x_at_py = (x2f - x1f) * (py - y1f) / (y2f - y1f) + x1f
                if px < x_at_py:
                    intersections += 1
    
        return intersections % 2 == 1
    def _solve(self, problem_input):
        points = [tuple([int(x) for x in line.strip().split(',')]) for line in problem_input]
        
        # Ensure the polygon is closed
        polygon = points[:]
        polygon.append(polygon[0])
        
        # Pre-split edges for intersection checks
        vertical_edges, horizontal_edges = [], []
    
        for (x1, y1), (x2, y2) in zip(polygon, polygon[1:]):
            if x1 == x2:
                y0, y1 = sorted((y1, y2))
                vertical_edges.append((x1, y0, y1))
            else:
                x0, x1 = sorted((x1, x2))
                horizontal_edges.append((y1, x0, x1))
    
        result = 0
    
        # Try all corner pairs as potential diagonal corners of a rectangle
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1 = points[i]
                p2 = points[j]
                
                x1, y1 = p1
                x2, y2 = p2
        
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        
                if area <= result:
                    continue
        
                if self.intersects_edges(p1, p2, vertical_edges, horizontal_edges):
                    continue
        
                # Check that a representative interior point lies inside the polygon
                if self.is_in_polygon(polygon, (min(x1, x2) + 0.1, min(y1, y2) + 0.1)):
                    result = area
                
        return result


solver = Solver(24)
solver.solve()