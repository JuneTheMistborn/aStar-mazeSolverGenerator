"""
Author: June Christine Simmons
2/8/22 - 2/14/22
Python implementation of a* maze solving algorithm without external libraries
Version 1.1
May add possibility to move diagonally to nodes, may add ability to define indication of wall, path, start, and goal
"""
import matplotlib.pyplot as plt
import matplotlib.animation as anim
maze = []  # nested lists maze is stored in
animate = True  # whether to show algorithm solving problem
saveAni = True  # whether to save animation of algorithm solving problem

with open("maze.txt") as file:  # read file and create maze in nested list
    lineNum = 0
    for line in file.readlines():
        maze.append([])  # new y list
        for char in line:
            if char.strip():
                maze[lineNum].append(char)  # new x val in y list
        lineNum += 1

for i in range(len(maze)):  # find where goal and start in maze are
    for j in range(len(maze[i])):
        if maze[i][j] == "g":  # if text is g, node is goal
            goalIndex = (i, j)
        if maze[i][j] == "o":  # if text is o, node is start
            startIndex = (i, j)
mazeSize = (len(maze) - 1, len(maze[0]) - 1)  # index where walls of maze are (y, x)
# print(maze)


class Node:
    def __init__(self, parent, index, g, node_type):  # takes parent, index g value, and type of node
        self.g = 0 + g  # cost of moving to node
        self.h = 0  # heuristic cost to move from this node to goal
        self.f = 0  # overall value, g+h, lower is better node
        self.parent = parent  # parent of this node
        self.adjacentNodes = []  # all nodes adjacent to this node
        self.index = index  # index of node (y, x)
        self.adjacentsLeft = True  # does node have adjacents
        self.indexSub = -1  # value to add for getting index of adjacent nodes
        self.type = node_type  # node type (start, goal, path, wall)

    def populate_adjacent(self):  # generate all nodes adjacent to this node
        # while self.adjacentsLeft:
        # if index "above" is not out of list range and node at said position is not a wall
        if self.index[0] - 1 >= 0 and maze[self.index[0]-1][self.index[1]] != "x":
            # pass self as parent, index as one "above" current node (y-1, x), this node's g plus one,
            # node type (text at given index in maze)
            self.adjacentNodes.append(Node(self, (self.index[0]-1, self.index[1]), self.g+1,
                                           maze[self.index[0]-1][self.index[1]]))
        # if index "below" is not out of list range
        if self.index[0] + 1 <= mazeSize[0] and maze[self.index[0]+1][self.index[1]] != "x":
            self.adjacentNodes.append(Node(self, (self.index[0]+1, self.index[1]), self.g+1,
                                           maze[self.index[0]+1][self.index[1]]))
        # if index "left" is not out of list range
        if self.index[1] - 1 >= 0 and maze[self.index[0]][self.index[1]-1] != "x":
            self.adjacentNodes.append(Node(self, (self.index[0], self.index[1]-1), self.g+1,
                                           maze[self.index[0]][self.index[1]-1]))
        # if index "right" is not out of list range
        if self.index[1] + 1 <= mazeSize[1] and maze[self.index[0]][self.index[1]+1] != "x":
            self.adjacentNodes.append(Node(self, (self.index[0], self.index[1]+1), self.g+1,
                                           maze[self.index[0]][self.index[1]+1]))

    def calc_vals(self):  # calculate h and f values
        self.h = abs(self.index[0] - goalIndex[0]) + abs(self.index[1] - goalIndex[1])  # heuristic function,
        # absolute value of current node index - goal index
        self.f = self.h + self.g  # value of node, h + g, lower makes node "better"


# print(maze[start.index[0]][start.index[1]])  # uncomment to print value at what program thinks is start node


def a_star():
    start = Node(None, (startIndex[0], startIndex[1]), 0, maze[startIndex[0]][startIndex[1]])  # node where player start
    open_list = [start]  # list of all nodes not yet examined
    closed_list = []  # list of all nodes that have been examined
    lowest_f_index = 0  # index in openList of node with "best" (lowest) f value
    path = []  # to be path from start to goal node
    frame = 0

    while len(open_list) > 0:  # while there are unexamined nodes
        # if counter % 10000 == 0:  # uncomment to print lists if infinite loop
        #    print(open_list, "\n", closed_list)
        # line below is the highest possible f value so that any node will have a lower value,
        # calculated from (maze area + heuristic of start node)
        lowest_f = (mazeSize[0]*mazeSize[1])+(abs(startIndex[0]-goalIndex[0])+abs(startIndex[1]-goalIndex[1]))
        open_list_index = 0  # index of current node in open_list

        for node in open_list:  # for all nodes left unexamined
            node.calc_vals()  # calculate h and f values of node
            if node.f < lowest_f:  # if node f is lower (node is better), remember node index and f value
                lowest_f = node.f  # new lowest f value
                lowest_f_index = open_list_index  # index in open_list of node with lowest f
            open_list_index += 1  # increment so next node's index is known

        best_node = open_list[lowest_f_index]  # node object at index of best node
        best_node.populate_adjacent()  # calculate all adjacent nodes to best node
        closed_list.append(best_node)  # add the best node to closed_list
        open_list.pop(lowest_f_index)  # remove the best node from open_list
        full_list = open_list+closed_list  # both lists together, for checking if node has already been seen

        for adjacent in best_node.adjacentNodes:  # for each adjacent node, check if it has been seen
            for allNodes in full_list:  # all seen nodes
                if adjacent.index == allNodes.index:  # if node has been seen, exit loop and continue to next adjacent
                    break
            else:  # if loop never breaks
                open_list.append(adjacent)  # add adjacent node to unevaluated nodes
            if adjacent.type == "g":  # if adjacent node is goal
                parent_node = adjacent.parent  # parent of goal node (and then of parent node, etc.)
                while parent_node.index != start.index:  # while parent node isn't the start node
                    path.append(parent_node.index)  # add index of parent node to solution list
                    parent_node = parent_node.parent  # go to node's parent
                return path  # return solution path

        if animate:  # if animate flag is true
            frame += 1  # increase frame (time dimension)
            mazeAnim.append([])  # add new frame
            open_indices = []  # all indices of unexamined nodes
            closed_indices = []  # all indices of examined nodes
            for node in open_list:  # populate index lists
                open_indices.append(node.index)
            for node in closed_list:
                closed_indices.append(node.index)
            for y_val in range(len(maze)):  # for height of frame
                mazeAnim[frame].append([])  # add new x list
                for x_val in range(len(maze[0])):  # for length of frame
                    if maze[y_val][x_val] == "g":  # setting node colors based on node type (rework needed)
                        mazeAnim[frame][y_val].append(.8)
                    elif maze[y_val][x_val] == "o":
                        mazeAnim[frame][y_val].append(.2)
                    elif maze[y_val][x_val] == "x":
                        mazeAnim[frame][y_val].append(0)
                    elif (y_val, x_val) == best_node.index:
                        mazeAnim[frame][y_val].append(.325)
                    elif (y_val, x_val) in open_indices:
                        mazeAnim[frame][y_val].append(.6)
                    elif (y_val, x_val) in closed_indices:
                        mazeAnim[frame][y_val].append(.45)
                    else:
                        mazeAnim[frame][y_val].append(1)


def animation(k):  # function to animate plot
    sub_plot.clear()
    sub_plot.imshow(mazeAnim[k], "tab20", animated=True)


# print(a_star())  # uncomment to print each index of node on solution path
mazeAnim = []  # list of arrays, to be animated
figure = plt.figure()  # new mpl figure
if animate:
    sub_plot = figure.add_subplot(1, 1, 1)  # new plot in figure

    mazeAnim.append([])
    for y in range(len(maze)):  # for size of y-axis of maze
        mazeAnim[0].append([])
        for x in range(len(maze[0])):  # for size of x-axis of maze
            if maze[y][x] == "g":  # if node is goal, mark space as golden (.1)
                mazeAnim[0][y].append(.8)
            elif maze[y][x] == "o":  # if node is start, mark space as green (.15)
                mazeAnim[0][y].append(.2)
            elif maze[y][x] == "x":  # if node is wall, mark space as dark blue (0)
                mazeAnim[0][y].append(0)
            else:  # if node is not special or in solution, mark space as pink (.475)
                mazeAnim[0][y].append(1)

solution = a_star()  # indexes of all nodes on solution path
solutionStr = ""  # output string to print to file

if solution is not None:  # if there is a solution
    for y in range(len(maze)):  # for size of y-axis of maze
        for x in range(len(maze[0])):  # for size of x-axis of maze
            if (y, x) in solution:  # if node index is on solution path
                solutionStr += "*"  # add asterisk to represent correct path node to solutionStr
            else:
                solutionStr += maze[y][x]  # add value at same position in original maze
        solutionStr += "\n"  # add newline for next line of x values

    # print(solutionStr)  # uncomment to print solution to console
    with open("solution.txt", "w+") as outFile:  # write solution to file
        outFile.write(solutionStr)

    # for listthing in mazeAnim:
        # print(listthing)
    if animate:
        ani = anim.FuncAnimation(figure, animation, interval=100, frames=len(mazeAnim))  # animation of plot
        if saveAni:
            ani.save("outAnimation.gif")  # save animation
        plt.show()  # show animation

else:
    print("Maze has no solution.")
