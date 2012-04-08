__author__ = 'dmitrijdackov'

#!/usr/bin/python
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

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space
grid = [[0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

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
    [ 0, -1], # go left
    [ 1,  0], # go down
    [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D():
    # value [orientation][row][col]
    value = [[[999 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[999 for col in range(len(grid[0]))] for row in range(len(grid))]]
    policy = [[[2 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[2 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[2 for col in range(len(grid[0]))] for row in range(len(grid))],
        [[2 for col in range(len(grid[0]))] for row in range(len(grid))]]
    x = goal[0]
    y = goal[1]

    # There are four goal possibilities for four orientations
    open_list = [[0, 0, x, y], [0, 1, x, y], [0, 2, x, y], [0, 3, x, y]]

    value[0][x][y] = 0
    value[1][x][y] = 0
    value[2][x][y] = 0
    value[3][x][y] = 0

    while len(open_list):
        #print open_list
        # pick a state that needs to be processed
        item = open_list.pop(0)
        g = item[0]
        o = item[1]
        x = item[2]
        y = item[3]
        for j in range(len(action)):
            # reverse the action to get the state you may
            # have come from to get to this state
            x2 = x - forward[o][0]
            y2 = y - forward[o][1]
            o2 = (o - action[j] + len(forward)) % len(forward)
            g2 = g + cost[j]
            if (x2 in range(len(grid)) and y2 in range(len(grid[0]))
                and grid[x2][y2] == 0):
                if g2 < value[o2][x2][y2]:
                    # if the from state would have a lower cost
                    # to come through the current state,
                    # then update it to point this way
                    value[o2][x2][y2] = g2
                    policy[o2][x2][y2] = j
                    open_list.append([g2, o2, x2, y2])
        #for i in range(len(policy)):
    #    for j in range(len(policy[0])):
    #        mystring = '['
    #        for k in range(len(policy[0][0])):
    #            mystring += '(' + str(value[i][j][k]) + ','
    #            mystring += str(policy[i][j][k]) + ') '
    #        mystring += ']'
    #        print mystring
    #    print '-------------'

    policy2D = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    x = init[0]
    y = init[1]
    o = init[2]
    while not (x == goal[0] and y == goal[1]):
        a = policy[o][x][y]
        policy2D[x][y] = action_name[a]
        o = (o + action[a] + len(forward)) % len(forward)
        x = x + forward[o][0]
        y = y + forward[o][1]
    policy2D[x][y] = '*'
    return policy2D # Make sure your function returns the expected grid.

res = optimum_policy2D()
for i in range(len(res)):
    print(res[i])

#Here's my take on the policy discovery.
# I start from the goal and run the actions backwards.
# For each of the possible previous states, I update the policy if the previous
# state would do better (lower cost) to go through the current state.
# I then add the discovered previous states to a 'open'
# list which I'll use in the next iteration.
# The iteration ends when there's nothing left in the 'open' list.
# That is, for all states I could have come from to get to the goal,
# I've looked for the previous states.
# I think it's more efficient because it doesn't iterate through the table
# every time but only visits each cell a maximum of four times
# (and less for cells next to walls). What do you think?

def optimum_policy2D2():
    value = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]
    policy =[[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
        [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]
    policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    value[1][goal[0]][goal[1]]=0

    #start at goal-state
    x=goal[0]
    y=goal[1]
    d=1 #facing left
    v=0
    active_list=[[v,x,y,d]]

    #pick element from active_list with lowest v and expand it
    while active_list:  #while not empty list
        active_list.sort()
        active_list.reverse()
        [v,x,y,d]=active_list.pop()

        #for each action (L, #, R)
        for i in range(len(action)):
            x2=x-forward[d][0]
            y2=y-forward[d][1]
            d2=(d-action[i])%4
            v2=v+cost[i]
            if x2>=0 and x2<len(grid) and y2>=0 and y2<len(grid[0]):
                if grid[x2][y2]==0 and value[d2][x2][y2]>v2:
                    value[d2][x2][y2]=v2
                    policy[d2][x2][y2]=i
                    active_list.append([v2,x2,y2,d2])

    #collapse policy to 2D case
    x=init[0]
    y=init[1]
    d=init[2]

    while x!=goal[0] or y!=goal[1]:
        policy2D[x][y]=action_name[policy[d][x][y]]
        d=(d+action[policy[d][x][y]])%4
        x=x+forward[d][0]
        y=y+forward[d][1]
    policy2D[x][y]='*'

    return policy2D # Make sure your function returns the expected grid.

print ()

res = optimum_policy2D2()
for i in range(len(res)):
    print(res[i])
