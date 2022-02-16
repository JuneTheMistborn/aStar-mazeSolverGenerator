"""
Author: June Christine Simmons
2/14/22 - 2/15/22
Python implementation of growing tree algorithm
Version 1.0
"""
from random import randint
import matplotlib.pyplot as plt
import matplotlib.animation as anim


size = (60, 60)
maze = []
cellNum = 0
visitedList = []
mazeAnim = [[]]
frame = 0
animate = False
saveAni = False
mazeStr = ""


def make_odd(integer):
    if integer % 2 == 0:
        return integer + 1
    else:
        return integer


yOdd = randint(0, (2 * size[0]))
randomIndex = (make_odd(randint(0, (2 * size[0]))), make_odd(randint(0, (2 * size[0]))))
cList = [randomIndex]
appendNum = 1

for y in range(size[0]):
    maze.append([])
    for i in range((size[0] * 2) + 1):
        maze[y*2].append("x")
    maze.append([])
    for x in range(size[1]):
        maze[appendNum].append("x")
        maze[appendNum].append("-")

    maze[appendNum].append("x")
    appendNum += 2
maze.append([])
for i in range((size[0] * 2) + 1):
    maze[len(maze)-1].append("x")

if animate:
    for y_val in range(len(maze)):  # for height of frame
        mazeAnim[frame].append([])  # add new x list
        for x_val in range(len(maze[0])):  # for length of frame
            if maze[y_val][x_val] == "x":
                mazeAnim[frame][y_val].append(0)
            else:
                mazeAnim[frame][y_val].append(1)

while len(cList) > 0:
    popList = []
    randOrNext = randint(1, 100)
    if randOrNext > 25:
        cellNum = randint(0, len(cList) - 1)
    else:
        cellNum = len(cList) - 1

    currIndex = cList[cellNum]
    neighbors = [(currIndex[0] - 2, currIndex[1]), (currIndex[0], currIndex[1] + 2),
                 (currIndex[0] + 2, currIndex[1]), (currIndex[0], currIndex[1] - 2)]
    for neighbor in neighbors:
        if neighbor in cList or neighbor in visitedList or neighbor[0] > size[0] * 2 or neighbor[1] > size[1] * 2 or \
                neighbor[0] < 0 or neighbor[1] < 0:
            popList.append(neighbors.index(neighbor))

    popList.sort(reverse=True)
    for toPop in popList:
        neighbors.pop(toPop)

    visitedList.append(currIndex)

    if not neighbors:
        cList.pop(cellNum)
        continue
    randNext = randint(0, len(neighbors) - 1)
    # print(currIndex[0], " ", neighbors[randNext][0], " ", (currIndex[0]+neighbors[randNext][0])//2)
    # print(currIndex[1], " ", neighbors[randNext][1], " ", (currIndex[1]+neighbors[randNext][1])//2, "\n")
    maze[(currIndex[0] + neighbors[randNext][0]) // 2][(currIndex[1] + neighbors[randNext][1]) // 2] = "-"
    cList.append(neighbors[randNext])

    if animate:
        frame += 1  # increase frame (time dimension)
        mazeAnim.append([])  # add new frame
        for y_val in range(len(maze)):  # for height of frame
            mazeAnim[frame].append([])  # add new x list
            for x_val in range(len(maze[0])):  # for length of frame
                if maze[y_val][x_val] == "x":
                    mazeAnim[frame][y_val].append(0)
                elif (y_val, x_val) == currIndex:
                    mazeAnim[frame][y_val].append(.325)
                else:
                    mazeAnim[frame][y_val].append(1)


def animation(k):  # function to animate plot
    sub_plot.clear()
    im = sub_plot.imshow(mazeAnim[k], "tab20", animated=True)
    return [im]


figure = plt.figure()  # new mpl figure
sub_plot = figure.add_subplot(1, 1, 1)  # new plot in figure
if animate:
    ani = anim.FuncAnimation(figure, animation, interval=1, frames=len(mazeAnim), blit=True)  # animation of plot
    if saveAni:
        ani.save("mazeGen.gif")
    plt.show()

for y in range(len(maze)):
    for x in maze[y]:
        mazeStr += x
    mazeStr += "\n"


with open("mazeOut.txt", "w+") as file:
    file.write(mazeStr)
