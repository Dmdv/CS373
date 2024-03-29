__author__ = 'Dyachkov'

# ----------
# User Instructions:
#
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

#These dimensions are for the 4 possible orientations that robot can be [up, down, left, right],
# these are not state variables

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

grid1 = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

goal1 = [1, 5] # final position
init1 = [1, 0, 3] # first 2 elements are coordinates, third is direction
cost1 = [0.1, 1, 1] # the cost field has 3 values: right turn, no turn, left turn


# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
#
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------

# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
        [0, -1], # go left
        [1,  0], # go down
        [0,  1]] # do right

forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D():

    #for orientation in range(4):
    #    for i in range(len(action)): # iteration by action
    #        o2 = (orientation + action[i]) % 4
    #        x2 = forward[o2][0]
    #        y2 = forward[o2][1]
    #        #print (forward_name[o2], forward[o2], action_name[i])

    global o2
    value = [[[999 for col in row ] for row in grid] for f in forward]
    policy = [[[' ' for col in row ] for row in grid] for f in forward]
    policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    change = True
    while change:
        change = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for orientation in range(4):
                    if goal[0] == x and goal[1] == y:
                        if value[orientation][x][y] > 0:
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = '*'
                            change = True

                    elif not grid[x][y]:

                        # calculate 3 ways to propagate value
                        for i in range(len(action)): # iteration by action
                            # to keep orientation within 3.
                            # left + up = right
                            o2 = (orientation + action[i]) % 4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]

                            #print ("o2 = ", o2, "x2 = ", x2, "y2 = ", y2)

                            if len(grid) > x2 >= 0 <= y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 = value[o2][x2][y2] + cost[i]
                                if v2 < value[orientation][x][y]:
                                    change = True
                                    value[orientation][x][y] = v2
                                    policy[orientation][x][y] = action_name[i]
    x = init[0]
    y = init[1]
    orientation = init[2]
    policy2D[x][y] = policy[orientation][x][y]
    while policy[orientation][x][y] != '*':
        if policy[orientation][x][y] == '#':
            o2 = orientation
        elif policy[orientation][x][y] == 'R':
            o2 = (orientation - 1) % 4
        elif policy[orientation][x][y] == 'L':
            o2 = (orientation + 1) % 4
        x = x + forward[o2][0]
        y = y + forward[o2][1]
        orientation = o2
        policy2D[x][y] = policy[orientation][x][y]

    return policy2D # Make sure your function returns the expected grid.

for row in optimum_policy2D():
    print(row)

# You can move through the list of forward actions.
# If your direction is forward[i], forward[i-1]
# is the direction of a left turn and forward[i+1]
# is the direction of the right turn. Of course you should make this cyclic using % len(forward).