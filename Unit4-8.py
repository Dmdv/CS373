__author__ = 'dmitrijdackov'

# ----------
# User Instructions:
#
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    # or closed = [[0] * len(grid[0]) for i in grid]
    closed[init[0]][init[1]] = 1 # since I am expanding this cell, it should be checked as 1

    x = init[0]
    y = init[1]
    g = 0
    open = [[g, x, y]]
    found = False
    resign = False

    # If the open list is empty, it
    # means that you have not found the goal,
    # and have nowhere else to search, so return fail, else we
    # find the smallest value of open.

    while not found and not resign:
        if len(open) == 0:
            resign = True
            return "fail"
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
        if x == goal[0] and y == goal[1]:
            found = True
        else:
            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if x2 >=0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                    if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                        g2 = g + cost
                        open.append([g2, x2, y2])
                        print (open)
                        closed[x2][y2] = 1
    return next


print (search())