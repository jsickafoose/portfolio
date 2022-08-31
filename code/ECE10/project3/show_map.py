#!/usr/bin/env python3
import pickle
from turtle import position
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

f = open('project3_part1.pickle','rb')
res = pickle.load(f)

# Class to create a node to represent every pixel of the math
class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # Current Distance Traveled
        self.h = 0 # Estimated Distance to goal 
        self.f = 0 # Estimated total distance of path

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    # Beginning and end of the path
    start_node = Node(None, start)
    end_node = Node(None, end)
    # Create 2 lists for open and closed:
        # Open means the node has not been explored yet,
        # Closed means the node has been explored, and is the lowest cost it can be
    open = []
    closed = []

    open.append(start_node)
    # Look for more nodes while they are available
    while len(open) > 0:
        # Initialize to first node
        current_node = open[0]
        current_index = 0
        # Look for item in the open list with the lowest f cost (Total distance of path with point)
        for index, item in enumerate(open):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # When selecting the current node, select the node with lowest cost in open
        open.pop(current_index)
        closed.append(current_node)

        # If the current node is the end node, then the path has been found
            # Go through the parent nodes to find the path
        if current_node == end_node:
            path = []
            point = current_node
            while point.parent:
                path.append(point.position)
                point = point.parent
            return path
        children = []
        for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        # for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])
            # Check for bounds
            if new_position[1] > len(maze) - 1 or new_position[0] < 0 or new_position[0] > len(maze[len(maze)-1]) -1 or new_position[1] < 0:
                continue
            # Check to see if already evaluated
            if Node(current_node, new_position) in closed: 
                continue
            # Check to see if there is a wall
            if maze[new_position[1]][new_position[0]] != 0:
                continue
            # Create new node if it is a valid neighbor
            new_node = Node(current_node, new_position)
            # Add the child of current node to list
            children.append(new_node)
        # Loop through the nodes connected to current node
        for child in children:
            # Add more distance if it is a diagonal reach
            if(abs(current_node.position[0] - child.position[0]) == abs(current_node.position[1] - child.position[1])):
                child.g = current_node.g + 14
            else:
                child.g = current_node.g + 10
            # Get the estimated distance to travel
            child.h = sqrt(((child.position[0] - end_node.position[0])**2) + ((child.position[1] - end_node.position[1])**2))
            child.f = child.g + child.h
            # Check to make sure you have lowest cost version of the node
            if child in open:
                for open_node in open:
                    if child == open_node and child.g < open_node.g:
                        open_node = child            
            else:
                open.append(child)
# Create the maze from the pickle
maze = res['map'].tolist()
# Set start and end points
start = (12, 36)
end = (38, 6)
# Create path
path = astar(maze, start, end)
# Get values of path to plot them
xvals = []
yvals = []
for x,y in path:
    xvals.append(x)
    yvals.append(y)
# Plot maze, path, and start/end points
plt.matshow(res['map'])
start = res['start']
plt.text(start[0], start[1], 'S', color='r',fontweight='bold')
goal = res['goal']
plt.text(goal[0], goal[1], 'G', color='g',fontweight='bold')
plt.plot(xvals, yvals)
plt.show()