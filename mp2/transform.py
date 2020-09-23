
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    limit = arm.getArmLimit()
    width = int((limit[0][1]-limit[0][0])/granularity)+1
    height = int((limit[1][1]-limit[1][0])/granularity)+1
    alphaOffset = limit[0][0]
    betaOffset = limit[1][0]
    temp = arm.getArmAngle()
    startA = temp[0]
    startB = temp[1]
    maze = [['x' for i in range(height)] for j in range(width)]
    for i in range(width):
        for j in range(height):
            alpha = idxToAngle((i,), (alphaOffset,), granularity)
            alpha = alpha[0]
            temp = []
            temp2 = []
            temp.append(j)
            temp2.append(betaOffset)
            beta = idxToAngle((j,), (betaOffset,), granularity)
            beta = beta[0]
            arm.setArmAngle((alpha, beta))
            if doesArmTouchObjects(arm.getArmPosDist(), obstacles):
                maze[i][j] = '%'
                continue
            if not isArmWithinWindow(arm.getArmPos(), window):
                maze[i][j] = '%'
                continue
            if doesArmTouchObjects(arm.getArmPosDist(), goals, True):
                if doesArmTipTouchGoals(arm.getEnd(), goals):
                    maze[i][j] = '.'
                else:
                    maze[i][j] = '%'
                continue
            maze[i][j] = " "

    alpha = angleToIdx((startA,), (alphaOffset,), granularity)
    beta = angleToIdx((startB,), (betaOffset,), granularity)
    maze[alpha[0]][beta[0]] = 'P'

    return Maze(maze, (alphaOffset, betaOffset), granularity)
