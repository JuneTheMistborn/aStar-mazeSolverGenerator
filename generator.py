"""
Author: June Christine Simmons
2/14/22 - 2/16/22
Python implementation of growing tree algorithm
Version 1.1
"""
from random import randint
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np


size = (40, 10)
maze = []
mazeStr = ""
cellNum = 0
visitedList = []
mazeAnim = np.zeros(((size[0]*2)+1, (size[1]*2)+1), dtype=float)
artistList = []
frame = 0
animate = True
saveAni = False

figure = plt.figure()  # new mpl figure
sub_plot = figure.add_subplot(1, 1, 1)  # new plot in figure


def make_odd(integer):
    if integer % 2 == 0 and integer != 0:
        return integer - 1
    elif integer == 0:
        return integer + 1
    else:
        return integer


yOdd = randint(0, (2 * size[0]))
randomIndex = (make_odd(randint(0, (2 * size[0]))), make_odd(randint(0, (2 * size[1]))))
prevIndex = randomIndex
cList = [randomIndex]
appendNum = 1
xVal = 1

for y in range(size[0]):
    maze.append([])
    for i in range((size[1] * 2) + 1):
        maze[y*2].append("x")
    maze.append([])
    xVal = 1
    for x in range(size[1]):
        maze[appendNum].append("x")
        maze[appendNum].append("-")
        if animate:
            mazeAnim[appendNum, xVal] = 1
            xVal += 2

    maze[appendNum].append("x")
    appendNum += 2

maze.append([])

for i in range((size[1] * 2) + 1):
    maze[len(maze)-1].append("x")


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
    print(currIndex[0], " ", neighbors[randNext][0], " ", (currIndex[0]+neighbors[randNext][0])//2)
    print(currIndex[1], " ", neighbors[randNext][1], " ", (currIndex[1]+neighbors[randNext][1])//2, "\n")
    maze[(currIndex[0] + neighbors[randNext][0]) // 2][(currIndex[1] + neighbors[randNext][1]) // 2] = "-"
    if animate:
        mazeAnim[(currIndex[0] + neighbors[randNext][0]) // 2, (currIndex[1] + neighbors[randNext][1]) // 2] = 1
        mazeAnim[currIndex[0], currIndex[1]] = .325
        mazeAnim[prevIndex[0], prevIndex[1]] = 1
        prevIndex = currIndex
    cList.append(neighbors[randNext])

    if animate:
        im = sub_plot.imshow(mazeAnim, "tab20", animated=True)
        artistList.append([im])

    # print("Pass number " + str(frame))
    # frame += 1

for y in range(len(maze)):
    for x in maze[y]:
        mazeStr += x
    mazeStr += "\n"

with open("mazeOut.txt", "w+") as file:
    file.write(mazeStr)

if animate:
    ani = anim.ArtistAnimation(figure, artistList, interval=50, blit=True)  # animation of plot
    if saveAni:
        ani.save("mazeGen.gif")
    plt.show()
