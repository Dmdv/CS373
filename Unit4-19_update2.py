__author__ = 'Dyachkov'

grid = [[1, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1]]

goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

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
import bisect

# list of (cost,action) tuples sorted by cost
acost = sorted([(cost[i], i) for i, _ in enumerate(action)])

# Minimum cost cache, indexed by a cell coordinate tuple
costCache = {}

# Calculate a new state given old state and action, None if new state isn't on the map or is a wall
def new_state(state, act):
    newDir = (state[2] + act) % len(forward)
    fw = forward[newDir]
    ns = (state[0] + fw[0], state[1] + fw[1], newDir)
    if 0 <= ns[0] < len(grid) and 0 <= ns[1] < len(grid[0]) and grid[ns[0]][ns[1]] != 1:
        return ns
    return None

# Generator function enumerating through next states for a given state
# in order of ascending cost
def state_gen(state, base_cost):
    # produces next states of any one state
    for cost, act_idx in acost:
        newState = new_state(state, action[act_idx])
        if newState:
            newCost = cost + base_cost
            yield (newCost, newState, (state, act_idx))

# Given a state generator object, extract the next state value and insert into the list
# Sorted by ascending state value
# or drop the generator object if it's empty
def push_gen(gen_list, gen):
    for newCost, newState, parentInfo in gen:
        bisect.insort(gen_list, (newCost, newState, parentInfo, gen))
        break

# Global next state generator
# Gets the next cheapest state from the state list
# start - coordinates of the start cell
def super_gen(start):
# sorted list of tuples (last_cost, last_state, parentInfo, gen_obj)
    start = tuple(start)
    activegen = [(0, start, (None, 0), []) ]
    costCache.clear()

    while activegen:
        # super best cost since that was a sorted list
        cost, state, parentInfo, gen = activegen.pop(0)
        push_gen(activegen, gen)
        if state in costCache:
            continue
        costCache[state] = (cost, parentInfo)
        push_gen(activegen, state_gen(state, cost))
        #print len(activegen)
        yield cost, state, parentInfo

def optimum_policy2D():
    found = False
    for cost, state, parentInfo in super_gen(init):
        if state[0:2] == tuple(goal):
            print ("Goal cost is %u" % cost)
            found = True
            break

    policy2D = [[' '] * len(grid[0]) for _ in grid]

    # Using parentInfo cached in costCache, trace back the path from end to start, updating the policy2D array
    if found:
        policy2D[goal[0]][goal[1]] = '*'
        while parentInfo:
            state, act_idx = parentInfo
            if not state:
                break
            if policy2D[state[0]][state[1]] == ' ':
                policy2D[state[0]][state[1]] = ''
            policy2D[state[0]][state[1]] += action_name[act_idx]
            parentInfo = costCache[state][1]

    return policy2D # Make sure your function returns the expected grid.

z = optimum_policy2D()
for _ in z: print (_)