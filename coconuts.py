#!/usr/bin/env python



def cocos(x):
    for i in range(5):
        x = (x*5.0/4.0)+1
        print (x)
        if int(x) != x: return False
    return x

i = 1
while True:
    result = cocos((i*5)+1)
    if result:
        print (result)
        print (i)
        break
    i += 1