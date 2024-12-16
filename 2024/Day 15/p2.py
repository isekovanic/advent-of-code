import sys

sys.path.append('../../')

from Core import SolverCore

# Not going to go into too many details as the code here is an absolute mess and I'm not
# proud of it, but hey - it works.
# Some points to note:
# - Whenever we move the enlarged boxes horizontally, we put all of the ones we want to move
#   in a stack which we ONLY flush if the boxes can move (i.e if we encounter a '.' character
#   after we've exhausted all boxes in the row); otherwise we don't do anything since we cannot
#   move.
# - Whenever we move vertically, we first run a BFS in the cardinal direction in which we're headed
#   (and it has to be BFS because the order matters of the boxes) and append each box in the exact
#   order that we visit it to a separate stack. The result should be a sorted stack which we then
#   flush ONLY if running the BFS did not encounter any walls that would prevent us from moving the
#   entire block. That way, we can ensure that nothing is overwritten whenever moving stuff from the
#   back. We make sure not to visit a box segment twice while running the BFS since it's pointless.

move_map = {
    '>': (0, 1),
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0),
}

class Solver(SolverCore):
    def _solve(self, problem_input):
        grid_input = [list(x) for x in problem_input[0]]
        moves = ''.join(problem_input[1])
        
        dimx, dimy = len(grid_input), len(grid_input[0])
        grid = {}
        
        current = (0, 0)
        for i in range(dimx):
            for j in range(dimy):
                point = (i, j * 2)
                next_point = (i, j * 2 + 1)
                if grid_input[i][j] == '@':
                    current = point
                    grid[point], grid[next_point] = '@', '.'
                if grid_input[i][j] == '#':
                    grid[point], grid[next_point] = '#', '#'
                if grid_input[i][j] == 'O':
                    grid[point], grid[next_point] = '[', ']'
                if grid_input[i][j] == '.':
                    grid[point], grid[next_point] = '.', '.'

        for move in moves:
            cx, cy = current
            dx, dy = move_map[move]
            
            new_point = (cx + dx, cy + dy)
            
            if grid[new_point] == '#':
                continue
            
            if grid[new_point] == '.':
                grid[new_point] = '@'
                grid[current] = '.'
                current = new_point
            
            if grid[new_point] in '[]':
                if move in '<>':
                    stack = []
                    new_box_point = new_point
                    while grid[new_box_point] in '[]':
                        nx, ny = new_box_point
                        stack.append((nx, ny))
                        new_box_point = (nx + dx, ny + dy)
                        
                    if grid[new_box_point] == '.':
                        while stack:
                            cb_x, cb_y = stack.pop()
                            grid[(cb_x + dx, cb_y + dy)] = grid[(cb_x, cb_y)]
                        
                        grid[current] = '.'
                        grid[new_point] = '@'
                        current = new_point
                else:
                    new_box_point = new_point
                    nx, ny = new_box_point
                    queue = [new_box_point]
                    if grid[new_box_point] == '[':
                        queue.append((nx, ny + 1))
                    else:
                        queue.append((nx, ny - 1))
                    
                    drain_stack = []
                    
                    can_move = True
                    visited = set([])
                    while queue:
                        nx, ny = queue.pop(0)
                        
                        if (nx, ny) in visited:
                            continue
                        
                        visited.add((nx, ny))
                        # only append to the stack if we actually visit a node
                        drain_stack.append((nx, ny))
                        
                        nx += dx
                        ny += dy
                        
                        if grid[(nx, ny)] == '[':
                            queue += [(nx, ny), (nx, ny + 1)]
                        elif grid[(nx, ny)] == ']':
                            queue += [(nx, ny), (nx, ny - 1)]
                        elif grid[(nx, ny)] == '#':
                            can_move = False
                            break
                    
                    if can_move:
                        while drain_stack:
                            nx, ny = drain_stack.pop()
                            
                            grid[(nx + dx, ny + dy)] = grid[(nx, ny)]
                            grid[(nx, ny)] = '.'
                    
                        grid[current] = '.'
                        grid[new_point] = '@'
                        current = new_point

        result = 0
        for point, val in grid.items():
            if val == '[':
                x, y = point
                result += 100 * x + y

        return result
    
    def read_input(self, file):
        read_input = open(file, 'r')
        return [group.split('\n') for group in read_input.read().split('\n\n')]


solver = Solver(9021)
solver.solve()

'''
####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
'''