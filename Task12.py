#!/usr/bin/env python

#!/usr/bin/env python

p = [0, 1, 0, 0, 0]
world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
pHit = 0.6
pMiss = 0.2

def sense(p, Z):
    q = [ ]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
        
    summ = sum(q)
    for i in range(len(q)):
        q[i] = q[i]/summ
    return q

def move(p, U):
    q = [ ]
    for i in range(len(p)):
        q.append(p[(i-U) % len (p)])
    return q

for i in range(len(measurements)):
    p = sense(p, measurements[i])

print(move(p, 1))

