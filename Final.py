__author__ = 'Dyachkov'

# -------------------
# Background Information
#
# In this problem, you will build a planner that makes a robot
# car's lane decisions. On a highway, the left lane (in the US)
# generally has a higher traffic speed than the right line.
#
# In this problem, a 2 lane highway of length 5 could be
# represented as:
#
# road = [[80, 80, 80, 80, 80],
#         [60, 60, 60, 60, 60]]
#
# In this case, the left lane has an average speed of 80 km/h and
# the right lane has a speed of 60 km/h. We can use a 0 to indicate
# an obstacle in the road.
#
# To get to a location as quickly as possible, we usually
# want to be in the left lane. But there is a cost associated
# with changing lanes. This means that for short trips, it is
# sometimes optimal to stay in the right lane.
#
# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works).
# This planner should be a function named plan() that takes
# as input four parameters: road, lane_change_cost, init, and
# goal. See parameter info below.
#
# Your function should RETURN the final cost to reach the
# goal from the start point (which should match with our answer).
# You may include print statements to show the optimum policy,
# though this is not necessary for grading.
#
# Your solution must work for a variety of roads and lane
# change costs.
#
# Add your code at line 92.
#
# --------------------
# Parameter Info
#
# road - A grid of values. Each value represents the speed associated
#        with that cell. A value of 0 means the cell in non-navigable.
#        The cost for traveling in a cell must be (1.0 / speed).
#
# lane_change_cost - The cost associated with changing lanes.
#
# init - The starting point for your car. This will always be somewhere
#        in the right (bottom) lane to simulate a highway on-ramp.
#
# goal - The destination. This will always be in the right lane to
#        simulate a highway exit-ramp.
#
# --------------------
# Testing
#
# You may use our test function below, solution_check
# to test your code for a variety of input parameters.
#
# You may also use the build_road function to build
# your own roads to test your function with.

import random

forward = [[-1,  0], # go up
        [0, -1], # go left
        [1,  0], # go down
        [0,  1]] # do right

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']
obstacle = 0

# ------------------------------------------
# build_road - Makes a road according to your specified length and
# lane_speeds. lane_speeds is a list of speeds for the lanes (listed
# from left lane to right). You can also include random obstacles.
#
def build_road(length, lane_speeds, print_flag = False, obstacles = False, obstacle_prob = 0.05):
    num_lanes = len(lane_speeds)
    road = [[lane_speeds[i] for dist in range(length)] for i in range(len(lane_speeds))]
    if obstacles:
        for x in range(len(road)):
            for y in range(len(road[0])):
                if random.random() < obstacle_prob:
                    road[x][y] = 0
    if print_flag:
        for lane in road:
            print("[%s]" % ', '.join('%5.3f' % speed for speed in lane))
    return road

# ------------------------------------------
# plan - Returns cost to get from init to goal on road given a
# lane_change_cost.
#
def plan(road, lane_change_cost, init, goal): # Don't change the name of this function!

    #for orientation in range(4):
    #    for i in range(len(action)): # iteration by action
    #        o2 = (orientation + action[i]) % 4
    #        x2 = forward[o2][0]
    #        y2 = forward[o2][1]
    #        #print (forward_name[o2], forward[o2], action_name[i])

    o2 = 0
    value = [[[999 for col in row ] for row in road] for f in forward]
    policy = [[[' ' for col in row ] for row in road] for f in forward]
    policy2D = [[' ' for row in range(len(road[0]))] for col in range(len(road))]

    change = True
    while change:
        change = False
        for x in range(len(road)):
            for y in range(len(road[0])):
                for orientation in range(4):
                    if goal[0] == x and goal[1] == y:
                        if value[orientation][x][y] > 0:
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = '*'
                            change = True

                    elif road[x][y] != obstacle:

                        cost = [lane_change_cost, float(1.0/road[x][y]), lane_change_cost]

                        for i in range(len(action)): # iteration by action
                            o2 = (orientation + action[i]) % 4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]

                            if len(road) > x2 >= 0 <= y2 < len(road[0]) and road[x2][y2] != obstacle:
                                v2 = value[o2][x2][y2] + cost[i]
                                if v2 < value[orientation][x][y]:
                                    change = True
                                    value[orientation][x][y] = v2
                                    policy[orientation][x][y] = action_name[i]
    x = init[0]
    y = init[1]
    orientation = 3 #init[2] directio to the right
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

    return 0

################# TESTING ##################

# ------------------------------------------
# solution check - Checks your path function using
# data from list called test[]. Uncomment the call
# to solution_check at the bottom to test your code.
#
def solution_check(test, epsilon = 0.00001):
    answer_list = []
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i], test[3][i])
        true_cost = test[4][i]
        if abs(user_cost - true_cost) < epsilon:
            answer_list.append(1)
        else:
            answer_list.append(0)
    correct_answers = 0
    print()
    for i in range(len(answer_list)):
        if answer_list[i] == 1:
            print('Test case', i + 1, 'passed!')
            correct_answers += 1
        else:
            print('Test case', i + 1, 'failed.')
    if correct_answers == len(answer_list):
        print("\nYou passed all test cases!")
        return True
    else:
        print("\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!")
        return False

# Test Case 0 (FAST left lane)

road = [[100, 100, 100, 100, 100, 100],
        [10, 10, 10, 10, 10, 10],
        [1, 1, 1, 1, 1, 1]]

road2 = [[1.0/100, 1.0/100, 1.0/100, 1.0/100, 1.0/100, 1.0/100],
        [1.0/10, 1.0/10, 1.0/10, 1.0/10, 1.0/10, 1.0/10],
        [1.0/1, 1.0/1, 1.0/1, 1.0/1, 1.0/1, 1.0/1]]


road1 = [[1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]]

goal = [1, 5] # final position
init = [1, 0, 3] # first 2 elements are coordinates, third is direction
init = [1, 0]
cost = 1.0 / 1000.0 # the cost of turns
obstacle = 0.0

test = plan(road, cost, init, goal)

# Test Case 1 (FAST left lane)
test_road1 = build_road(8, [100, 10, 1])
lane_change_cost1 = 1.0 / 1000.0
test_init1 = [len(test_road1) - 1, 0]
test_goal1 = [len(test_road1) - 1, len(test_road1[0]) - 1]
true_cost1 = 1.244



test = plan(test_road1, lane_change_cost1, test_init1, test_goal1)

# Test Case 2 (more realistic road)
test_road2 = build_road(14, [80, 60, 40, 20])
lane_change_cost2 = 1.0 / 100.0
test_init2 = [len(test_road2) - 1, 0]
test_goal2 = [len(test_road2) - 1, len(test_road2[0]) - 1]
true_cost2 = 0.293333333333

# Test Case 3 (Obstacles included)
test_road3 = [[50, 50, 50, 50, 50, 40, 0, 40, 50, 50, 50, 50, 50, 50, 50], # left lane: 50 km/h
            [40, 40, 40, 40, 40, 30, 20, 30, 40, 40, 40, 40, 40, 40, 40],
            [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]] # right lane: 30 km/h

lane_change_cost3 = 1.0 / 500.0
test_init3 = [len(test_road3) - 1, 0]
test_goal3 = [len(test_road3) - 1, len(test_road3[0]) - 1]
true_cost3 = 0.355333333333

# Test Case 4 (Slalom)
test_road4 = [[50, 50, 50, 50, 50, 40,  0, 40, 50, 50,  0, 50, 50, 50, 50], # left lane: 50 km/h
              [40, 40, 40, 40,  0, 30, 20, 30,  0, 40, 40, 40, 40, 40, 40],
              [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]] # right lane: 30 km/h

lane_change_cost4 = 1.0 / 65.0
test_init4 = [len(test_road4) - 1, 0]
test_goal4 = [len(test_road4) - 1, len(test_road4[0]) - 1]
true_cost4 = 0.450641025641

testing_suite = [[test_road1, test_road2, test_road3, test_road4],
    [lane_change_cost1, lane_change_cost2, lane_change_cost3, lane_change_cost4],
    [test_init1, test_init2, test_init3, test_init4],
    [test_goal1, test_goal2, test_goal3, test_goal4],
    [true_cost1, true_cost2, true_cost3, true_cost4]]

#solution_check(testing_suite) #UNCOMMENT THIS LINE TO TEST YOUR CODE




