# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)
import heapq
import pdb

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = maze.getObjectives()
    queue = []
    path = []
    visit = {} # 0 means not visited, 1 means visited
    last = {}
    for i in range(maze.rows):
        for j in range(maze.cols):
            visit[(i,j)] = 0
    queue.append(start)
    while len(queue)>0:
        current = queue.pop(0)
        neighbors = maze.getNeighbors(current[0],current[1])
        for entry in neighbors:
            for i in range(len(objectives)):
                if objectives[i] == entry:
                    objectives.pop(i)
                    break
            if len(objectives) == 0:
                path.append(entry)
                temp = current
                path.insert(0,temp)
                while temp!=start:
                    temp = last[temp]
                    path.insert(0, temp)
                return path
            if visit[(entry[0], entry[1])] == 0:
                queue.append(entry)
                visit[(entry[0], entry[1])] = 1
                last[entry] = current
    return path


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = maze.getObjectives()
    queue = []
    path = []
    visit = {}  # 0 means not visited, 1 means visited
    last = {}
    for i in range(maze.rows):
        for j in range(maze.cols):
            visit[(i, j)] = 0
    heapq.heappush(queue, (0, start))
    while len(queue) > 0:
        current = heapq.heappop(queue)
        neighbors = maze.getNeighbors(current[1][0], current[1][1])
        for entry in neighbors:
            if objectives[0] == entry:
                path.append(entry)
                temp = current[1]
                path.insert(0, temp)
                while temp != start:
                    temp = last[temp]
                    path.insert(0, temp)
                return path
            if visit[(entry[0], entry[1])] == 0:
                distance = (entry[0]-objectives[0][0])**2 + (entry[1]-objectives[0][1])**2
                heapq.heappush(queue, (distance, entry))
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
    return path

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = maze.getObjectives()
    queue = []
    path = []
    partialPath= []
    visit = {}  # 0 means not visited, 1 means visited
    last = {}
    path.append(start)
    for i in range(maze.rows):
        for j in range(maze.cols):
            visit[(i, j)] = 0
    visit[(start[0], start[1])] = 1
    MST = MSTfunc(objectives)
    heapq.heappush(queue, (0, start))
    active = (0,0)
    # A star starts here
    while len(queue) > 0:
        current = heapq.heappop(queue)
        temp = float("inf")
        for o in objectives:
            temp2 = (o[0] - current[1][0]) ** 2 + (o[1] - current[1][1]) ** 2
            if temp2 < temp:
                temp = temp2
                active = o
        neighbors = maze.getNeighbors(current[1][0], current[1][1])
        for entry in neighbors:
            if active == entry:
                objectives.remove(active)
                partialPath.clear()
                partialPath.append(entry)
                temp = current[1]
                if temp != start:
                    partialPath.insert(0, temp)
                    while last[temp] != start:
                        temp = last[temp]
                        partialPath.insert(0, temp)
                path += partialPath
                if len(objectives)==0:
                    print(path)
                    return path
                MST = MSTfunc(objectives)
                for i in range(maze.rows):
                    for j in range(maze.cols):
                        visit[(i, j)] = 0
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
                queue.clear()
                heapq.heappush(queue, (0, entry))
                start = entry
                break
            if visit[(entry[0], entry[1])] == 0:
                distance = (entry[0]-active[0])**2 + (entry[1]-active[1])**2
                distance += MST
                heapq.heappush(queue, (distance, entry))
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
    return path

def MSTfunc(objectives):
    MST = 0
    tree = []
    queue = []
    size = len(objectives)
    # MST Calculation
    for i in range(size):
        for j in range(i, size):
            if i != j:
                distance = (objectives[i][0] - objectives[j][0]) ** 2 + (objectives[i][1] - objectives[j][1]) ** 2
                queue.append((distance, objectives[i], objectives[j]))
    heapq.heapify(queue)
    while (len(queue) != 0):
        temp = heapq.heappop(queue)
        if temp[1] not in tree and temp[2] not in tree:
            tree.append(temp[1])
            tree.append(temp[2])
            MST += temp[0]
    ##############################
    return MST

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = maze.getObjectives()
    queue = []
    path = []
    partialPath = []
    visit = {}  # 0 means not visited, 1 means visited
    last = {}
    path.append(start)
    for i in range(maze.rows):
        for j in range(maze.cols):
            visit[(i, j)] = 0
    visit[(start[0], start[1])] = 1
    MST = MSTfunc(objectives)
    heapq.heappush(queue, (0, start))
    active = (0, 0)
    # A star starts here
    while len(queue) > 0:
        current = heapq.heappop(queue)
        temp = float("inf")
        for o in objectives:
            temp2 = (o[0] - current[1][0]) ** 2 + (o[1] - current[1][1]) ** 2
            if temp2 < temp:
                temp = temp2
                active = o
        neighbors = maze.getNeighbors(current[1][0], current[1][1])
        for entry in neighbors:
            if active == entry:
                objectives.remove(active)
                partialPath.clear()
                partialPath.append(entry)
                temp = current[1]
                if temp != start:
                    partialPath.insert(0, temp)
                    while last[temp] != start:
                        temp = last[temp]
                        partialPath.insert(0, temp)
                path += partialPath
                if len(objectives) == 0:
                    print(path)
                    return path
                MST = MSTfunc(objectives)
                for i in range(maze.rows):
                    for j in range(maze.cols):
                        visit[(i, j)] = 0
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
                queue.clear()
                heapq.heappush(queue, (0, entry))
                start = entry
                break
            if visit[(entry[0], entry[1])] == 0:
                distance = (entry[0] - active[0]) ** 2 + (entry[1] - active[1]) ** 2
                distance += MST
                heapq.heappush(queue, (distance, entry))
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
    return path


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objectives = maze.getObjectives()
    queue = []
    path = []
    partialPath = []
    visit = {}  # 0 means not visited, 1 means visited
    last = {}
    path.append(start)
    for i in range(maze.rows):
        for j in range(maze.cols):
            visit[(i, j)] = 0
    visit[(start[0], start[1])] = 1
    MST = MSTfunc(objectives)
    heapq.heappush(queue, (0, start))
    active = (0, 0)
    # A star starts here
    while len(queue) > 0:
        current = heapq.heappop(queue)
        temp = float("inf")
        for o in objectives:
            temp2 = (o[0] - current[1][0]) ** 2 + (o[1] - current[1][1]) ** 2
            if temp2 < temp:
                temp = temp2
                active = o
        neighbors = maze.getNeighbors(current[1][0], current[1][1])
        for entry in neighbors:
            if active == entry:
                objectives.remove(active)
                partialPath.clear()
                partialPath.append(entry)
                temp = current[1]
                if temp != start:
                    partialPath.insert(0, temp)
                    while last[temp] != start:
                        temp = last[temp]
                        partialPath.insert(0, temp)
                path += partialPath
                if len(objectives) == 0:
                    print(path)
                    return path
                MST = MSTfunc(objectives)
                for i in range(maze.rows):
                    for j in range(maze.cols):
                        visit[(i, j)] = 0
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
                queue.clear()
                heapq.heappush(queue, (0, entry))
                start = entry
                break
            if visit[(entry[0], entry[1])] == 0:
                distance = (entry[0] - active[0]) ** 2 + (entry[1] - active[1]) ** 2
                distance += MST
                heapq.heappush(queue, (distance, entry))
                visit[(entry[0], entry[1])] = 1
                last[entry] = current[1]
    return path
