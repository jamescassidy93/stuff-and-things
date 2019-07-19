#!/usr/bin/env python
import argparse
from math import sqrt,pow
from numpy import arange

class Circle():
    def __init__(self,center_x,center_y,radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def createPoint(self,x):
        point = {}
        y = sqrt(abs(pow(self.radius,2) - pow(x,2)))
        point[self.center_x+x] = (self.center_y-y,self.center_y+y)
        return point

class Ellipse():
    def __init__(self,x,y,a,b):
        self.center_x = x
        self.center_y = y
        self.major_axis = a
        self.minor_axis = b

    def createPoint(self,x):
        point = {}
        y = sqrt(abs(pow(self.minor_axis,2) - (pow(self.minor_axis,2)*pow(x,2))/pow(self.major_axis,2)))
        point[self.center_x + x] = (self.center_y - y, self.center_y + y)
        return point

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x",help="x coordinate for center",type=int,default=0)
    parser.add_argument("-y",help="y coordinate for center",type=int,default=0)
    parser.add_argument("-r","--radius",help="radius of circle",type=int,default=1)
    parser.add_argument("-a","--major_axis",help="major axis of ellipse",type=int,default=2)
    parser.add_argument("-b","--minor_axis",help="minor axis of ellipse",type=int,default=1)
    parser.add_argument("shape",help="shape to draw with generated points",default="circle")
    parser.add_argument("num_points",help="number of points to generate around the center",type=float)
    args = parser.parse_args()

    if args.shape == "circle":
        base = Circle(args.x,args.y,args.radius)
        step_range = 2 * args.radius / (args.num_points-1)
        points = []
        for i in arange(-1*args.radius,args.radius,step_range):
            points.append(base.createPoint(i))
        points.append(base.createPoint(args.radius))
        print("Circle Coords")
        print("X coord - negative Y coord - positive Y coord")
        file = open("circle_coords.txt","w")
        pos = True
        for point in points:
            x_coord = next(iter(point))
            print(str(x_coord) + " - " + str(point[x_coord][0]) + " - " + str(point[x_coord][1]))
            if pos:
                file.write("        POSITION "+str(int(x_coord))+" "+str(int(point[x_coord][0]))+"\n")
                pos = False
            else:
                file.write("        POSITION "+str(int(x_coord))+" "+str(int(point[x_coord][1]))+"\n")
                pos = True
    elif args.shape == "ellipse":
        base = Ellipse(args.x,args.y,args.major_axis,args.minor_axis)
        step_range = 2 * args.major_axis / (args.num_points - 1)
        points = []
        for i in arange(-1 * args.major_axis, args.major_axis, step_range):
            points.append(base.createPoint(i))
        print("Ellipse Coords")
        print("X coord - negative Y coord - positive Y coord")
        file = open("ellipse_coords.txt", "w")
        pos = True
        node_num = 119
        for point in points:
            x_coord = next(iter(point))
            print(str(x_coord) + " - " + str(point[x_coord][0]) + " - " + str(point[x_coord][1]))
            file.write("\nNODE ES"+str(node_num)+"\n        LABEL ES"+str(node_num)+"\n")
            if pos:
                file.write("        POSITION " + str(int(x_coord)) + " " + str(int(point[x_coord][0])) + "\n")
            else:
                file.write("        POSITION " + str(int(x_coord)) + " " + str(int(point[x_coord][1])) + "\n")
            pos = not pos
            node_num+=1

if __name__ == '__main__':
    main()