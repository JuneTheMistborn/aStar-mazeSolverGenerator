"""
Author: June Christine Simmons
6/23/22 - 7/24/22
Uses my Python implementation of the a* pathfinding algorithm, with a window to input a maze and watch it be solved
Version 1
May add possibility to move diagonally to nodes
"""
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import solverFuncs
import animationFuncs
import os


class MazeWindow:
    def __init__(self):
        self.maze, self.maze_size, self.goal_index, self.start_index = solverFuncs.convert_maze("mazeOut.txt")
        self.maze_plot = animationFuncs.create_plot(self.maze)
        self.open_list = [solverFuncs.Node(None, self.start_index, 0)]
        self.open_list[0].calc_vals(self.goal_index)
        self.closed_list = []

        self.root = tk.Tk()
        self.root.title("Maze Generation and Solving")
        self.root.geometry("1000x900")
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit)

        self.fig = plt.figure(figsize=(6, 6))
        self.plot1 = self.fig.add_subplot(1, 1, 1, frameon=False)
        self.plot1.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        self.plot1.set_position([0, 0, 1, 1])
        self.im = self.plot1.imshow(self.maze_plot, "tab20")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        self.after_id = None
        self.delay = 0
        self.cont_run = True

        run_button = tk.Button(master=self.root, command=self.animation, height=2, width=10, text="Run solution")
        run_button.pack()

        plot_button = tk.Button(master=self.root, command=self.pause_maze, height=2, width=10,
                                text="Pause Maze")
        plot_button.pack()

        quit_button = tk.Button(master=self.root, text="Quit", command=self.root.quit)
        quit_button.pack()

        self.root.mainloop()

    def plot(self, maze_list):
        self.im.set_data(maze_list)
        self.canvas.draw()

    def advance_frame(self):
        new_nodes = []
        self.open_list, self.closed_list, finished_maze, new_node_amount = \
            solverFuncs.a_star_step(self.maze, self.maze_size, self.goal_index, self.start_index, self.open_list,
                                    self.closed_list)

        if new_node_amount != 0:
            new_nodes = self.open_list[-new_node_amount:]

        self.maze_plot = animationFuncs.change_plot(self.maze_plot, new_nodes, self.closed_list[len(self.closed_list)-2]
                                                    , self.closed_list[len(self.closed_list)-1])
        return finished_maze

    def animation(self):
        self.cont_run = True
        finished_maze = self.advance_frame()
        self.plot(self.maze_plot)
        self.root.update()

        if finished_maze is not None:
            self.maze_plot = animationFuncs.show_finished(self.maze_plot, finished_maze)
            self.im.set_data(self.maze_plot)
            self.canvas.draw()

        if self.cont_run and finished_maze is None:
            self.after_id = self.root.after(self.delay, self.animation)

    def pause_maze(self):
        self.root.after_cancel(self.after_id)
        self.cont_run = False


if __name__ == "__main__":
    window = MazeWindow()
