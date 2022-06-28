"""
Author: June Christine Simmons
6/23/22 - //22
Uses my Python implementation of the a* pathfinding algorithm, with a window to input a maze and watch it be solved
Version 1
May add possibility to move diagonally to nodes
"""
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time
import solverFuncs


"""def change_plot(maze_plot, open_list, closed_list):
    for node in open_list:"""




maze, maze_size, goalIndex, startIndex = solverFuncs.convert_maze("maze.txt")
mazePlot = maze
solution = solverFuncs.a_star(maze, maze_size, goalIndex, startIndex, False)
print(solution)

# solverFuncs.write_solution(solution, maze, "maze")
