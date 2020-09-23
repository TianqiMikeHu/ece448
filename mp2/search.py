# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush
from util import *
import pdb

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    start = maze.getStart()
    start = angleToIdx(start, maze.offsets, maze.granularity)
    temp = maze.getObjectives()
    objectives = []
    for t in temp:
        objectives.append(angleToIdx(t, maze.offsets, maze.granularity))
    queue = []
    path = []
    visit = {}  # 0 means not visited, 1 means visited
    last = {}
    dimensions = maze.getDimensions()
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            visit[(i, j)] = 0
    queue.append(start)
    while len(queue) > 0:
        current = queue.pop(0)
        current2 = idxToAngle(current, maze.offsets, maze.granularity)
        neighbors = []
        temp = maze.getNeighbors(current2[0],current2[1])
        for t in temp:
            neighbors.append(angleToIdx(t, maze.offsets, maze.granularity))
        for entry in neighbors:
            for i in range(len(objectives)):
                if objectives[i] == entry:
                    path.append(idxToAngle(entry, maze.offsets, maze.granularity))
                    temp = current
                    path.insert(0, idxToAngle(temp, maze.offsets, maze.granularity))
                    while temp != start:
                        temp = last[temp]
                        path.insert(0, idxToAngle(temp, maze.offsets, maze.granularity))
                    return path
            if visit[(entry[0], entry[1])] == 0:
                queue.append(entry)
                visit[(entry[0], entry[1])] = 1
                last[entry] = current
    return None
