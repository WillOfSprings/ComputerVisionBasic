import random
import math
import matplotlib.pyplot as plt
import imageio.v2 as iio
import numpy as np
from math import atan
import cv2
from functools import reduce

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
 
    def __str__(self):
        return ' '.join([str(i.a) for i in self.queue]).join([str(i.b) for i in self.queue])
 
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def insert(self, data,position):
        self.queue.insert(position,data)

    def size(self):
        return len(self.queue)
 
    # for popping an element based on Priority
    def delete(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i].dist > self.queue[max_val].dist:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return (item,max_val)
        except IndexError:
            print()
            exit()



class Edge:
    def __init__(self,_a,_b,_c,_d):
        self.a = _a
        self.b = _b
        self.c = _c
        self.d = _d
        self.dist = math.sqrt((_a - _c)*(_a - _c) + (_b - _d)*(_b - _d))
        self.m = 0
        base = (_c - _a)
        divide = (_d - _b)
        if base != 0:
            self.m = (divide)/(base) 

def findAngle(M1, M2):
    PI = 3.14159265
     
    angle = abs((M2.m - M1.m) / (1 + M1.m * M2.m))
 
    ret = atan(angle)
 
    val = (ret * 180) / PI
    if(val == 0):
        val = 90
    return (round(val, 4))

def convex_hull_graham(points):
    TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

    def cmp(a, b):
        return (a > b) - (a < b)

    def turn(p, q, r):
        return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

    def _keep_left(hull, r):
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return l.extend(u[i] for i in range(1, len(u) - 1)) or l

if __name__ == '__main__':
    
    image = iio.imread('./images/hand.jpg') #reading the image using opencv

    try:
        red = image[:,:,0] 
        blue = image[:,:,1]
        green = image[:,:,2]
        gray = red*0.33+blue*0.33+green*0.33 
        binary = gray.copy()
        (row,col) = gray.shape[0:2]
        for i in range(row):
            for j in range(col):
                if(gray[i,j]>128):
                    binary[i,j] = 1
                else:
                    binary[i,j] = 0
    except:
        gray = image[:,:]
        binary = gray.copy()
        (row,col) = gray.shape[0:2]
        for i in range(row):
            for j in range(col):
                if(gray[i,j]>128):
                    binary[i,j] = 1
                else:
                    binary[i,j] = 0

    points = []
    for i in range(row):
        for j in range(col): 
            if(binary[i,j] == 1):
                array = [i,j]
                points.append(array)

    #points = [(random.randint(0,100),random.randint(0,100)) for i in range(100)]
       
    h = convex_hull_graham(points)
    xs = [x[0] for x in points]
    ys = [x[1] for x in points]

    plt.plot(xs, ys, "o") 
   
    
    all_Edges = []
    for i in range(len(h)-1):
            a = h[i][0]
            b = h[i][1]
            c = h[i+1][0]
            d = h[i+1][1]
            edger = Edge(a,b,c,d)
            all_Edges.append(edger)

    size = len(h) - 1
    temp_a = h[size][0]
    temp_b = h[size][1]
    temp_c = h[0][0]
    temp_d = h[0][1]
    temp_edge = Edge(temp_a,temp_b,temp_c,temp_d)
    all_Edges.append(temp_edge)
    for i in range(len(all_Edges)-1):
        angle = findAngle(all_Edges[i],all_Edges[i+1])
        if((angle > 170 or angle<10) and [all_Edges[i].c,all_Edges[i].d] in h):
            h.remove([all_Edges[i].c,all_Edges[i].d])
    xs1 = [x[0] for x in h]
    ys1 = [x[1] for x in h]
    xs1.append(h[0][0])
    ys1.append(h[0][1])
    print("N = ",len(h))

    myQueue = PriorityQueue()
   
    plt.plot(xs1, ys1, "o")
    if(len(h)<20):
        for i in range(len(h)-1):
            a = h[i][0]
            b = h[i][1]
            c = h[i+1][0]
            d = h[i+1][1]
            edger = Edge(a,b,c,d)
            myQueue.insert(edger,i)

        size = len(h) - 1
        temp_a = h[size][0]
        temp_b = h[size][1]
        temp_c = h[0][0]
        temp_d = h[0][1]
        temp_edge = Edge(temp_a,temp_b,temp_c,temp_d)
        myQueue.insert(temp_edge,i+1)

        while myQueue.size() < 20:
            node,position = myQueue.delete()
            a = node.a
            b = node.b
            c = node.c
            d = node.d
            midx = (a+c)/2
            midy = (b+d)/2
            node1 = Edge(a,b,midx,midy)
            node2 = Edge(midx,midy,c,d)
            myQueue.insert(node1,position)
            myQueue.insert(node2,position+1)



xs2 = []
ys2 = []
i=0
while i<myQueue.size():
    one = myQueue.queue[i]
    i=i+1
    xs2.append(one.a)
    ys2.append(one.b)
xs2.append(myQueue.queue[0].a)
ys2.append(myQueue.queue[0].b)

print("After normalization = ",len(xs2)-1)
            
plt.plot(xs2, ys2,'ro-')
plt.show()