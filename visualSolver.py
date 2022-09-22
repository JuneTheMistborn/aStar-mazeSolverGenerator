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
from tkinter import filedialog as fd


class MazeWindow:
    def __init__(self):
        self.mazeName = None
        self.maze = None
        self.maze_size = None
        self.goal_index = None
        self.start_index = None
        self.maze_plot = [[0], [0]]
        self.open_list = None
        self.closed_list = None
        self.solved = False

        self.root = tk.Tk()
        self.root.title("Maze Generation and Solving")
        self.root.geometry("1000x900")
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit)

        self.fig_size = 2
        self.mazeoption_size = (321, 353)
        self.relative_height = (self.fig_size*100)/self.mazeoption_size[1]
        self.relative_width = (self.fig_size*100)/self.mazeoption_size[0]

        self.fig = plt.figure(figsize=(self.fig_size, self.fig_size), dpi=100)
        self.plot1 = self.fig.add_subplot(1, 1, 1, frameon=False)
        self.plot1.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        self.plot1.set_position([0, 0, 1, 1])
        self.im = self.plot1.imshow(self.maze_plot, cmap="tab20", alpha=0)
        self.maze_frame = tk.Frame(self.root, height=self.mazeoption_size[1], width=self.mazeoption_size[0], bg="#457fff")
        self.solve_options_frame = tk.Frame(self.maze_frame, bg="#45ff7f")
        self.generate_options_frame = tk.Frame(self.maze_frame, bg="#45ff7f")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.maze_frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().place(height=200, width=200, x=(self.mazeoption_size[0]-(self.fig_size*100))/2)
        self.solve_options_frame.place(y=200, x=53)
        self.after_id = None
        self.delay = 0
        self.cont_run = True
        self.options_pad = 5
        self.randomness_var = tk.IntVar(self.generate_options_frame, 50)
        self.state = "solve"

        run_button = tk.Button(master=self.solve_options_frame, command=self.animation, height=2, width=10,
                               text="Run solution")
        run_button.grid(column=0, row=0, sticky="ew")

        pause_button = tk.Button(master=self.solve_options_frame, command=self.pause_maze, height=2, width=10,
                                 text="Pause maze")
        pause_button.grid(column=1, row=0, sticky="ew")

        file_button = tk.Button(master=self.solve_options_frame, command=self.open_maze, height=2, width=10,
                                text="Open maze")
        file_button.grid(row=3, column=0)

        self.status_label = tk.Label(master=self.solve_options_frame, text="Open a maze", height=2)
        self.status_label.grid(row=2, column=0, columnspan=2)

        quit_button = tk.Button(master=self.root, text="Quit", command=self.root.quit)
        quit_button.pack()

        mode_switch_button = tk.Button(master=self.root, text="Change mode", command=self.move_anim)
        mode_switch_button.pack()

        self.generate_options_frame.columnconfigure(index=0, weight=1)
        self.generate_options_frame.columnconfigure(index=1, weight=10)
        self.generate_options_frame.columnconfigure(index=2, weight=6)

        self.width_entry = tk.Entry(master=self.generate_options_frame)
        self.width_entry.grid(column=1, row=2, sticky="ew")

        self.height_entry = tk.Entry(master=self.generate_options_frame)
        self.height_entry.grid(column=1, row=3, sticky="ew")

        entry_height_label = tk.Label(master=self.generate_options_frame, text="Height", justify="left",
                                      bg="#45ff7f")
        entry_height_label.grid(column=0, row=2, sticky="ew")

        entry_width_label = tk.Label(master=self.generate_options_frame, text="Width", justify="left",
                                     bg="#45ff7f")
        entry_width_label.grid(column=0, row=3, sticky="ew")

        self.randomness_label = tk.Label(master=self.generate_options_frame, justify="left", bg="#45ff7f",
                                         text=f"The random choice percentage is {self.randomness_var.get()}%"
                                              f"\nThe determined choice percentage is {100-self.randomness_var.get()}%")
        self.randomness_label.grid(column=0, row=5, columnspan=3, rowspan=2, sticky="w")

        self.randomness_slider = tk.Scale(master=self.generate_options_frame, orient="horizontal", showvalue=False,
                                          variable=self.randomness_var, command=self.update_random_label)
        self.randomness_slider.grid(column=0, row=4, columnspan=2, sticky="new")

        self.generate_button = tk.Button(master=self.generate_options_frame, text="Generate")
        self.generate_button.grid(column=2, row=2, rowspan=2, sticky="nsew")

        self.inf_label = tk.Label(master=self.generate_options_frame, text="Choose a height and width in cells, and the"
                                                                           " percentage of randomness applied to the "
                                                                           "maze.", wraplength=350, justify="left",
                                  bg="#45ff7f")
        self.inf_label.grid(column=0, row=0, columnspan=3, rowspan=2)

        self.save_sol_button = tk.Button(master=self.solve_options_frame, text="Save Solution", height=2, width=10)
        self.save_sol_button.grid(column=1, row=3)

        self.save_maze_button = tk.Button(master=self.generate_options_frame, text="Save Maze", width=10)
        self.save_maze_button.grid(column=2, row=4, sticky="ew")

        self.maze_frame.pack(side="right")
        self.generate_options_frame.place(y=200, x=344)
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
        if self.solved:
            self.status_label.configure(text="Maze was already solved!")
            return
        if self.maze is None:
            self.status_label.configure(text="You must select a maze file\nbefore running a solution!", fg="red")
            return
        self.status_label.configure(text="Solving maze", fg="green")
        self.cont_run = True
        finished_maze = self.advance_frame()
        self.plot(self.maze_plot)
        self.root.update()

        if finished_maze is not None:
            self.maze_plot = animationFuncs.show_finished(self.maze_plot, finished_maze)
            self.im.set_data(self.maze_plot)
            self.canvas.draw()
            self.status_label.configure(text="Solved!")
            self.solved = True

        if self.cont_run and finished_maze is None:
            self.after_id = self.root.after(self.delay, self.animation)

    def pause_maze(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.cont_run = False

    def open_maze(self):
        if self.after_id is not None:
            self.pause_maze()
        self.mazeName = fd.askopenfilename(filetypes=[('text files', '*.txt')])
        print(self.mazeName)
        if self.mazeName != () and self.mazeName != "":
            self.maze, self.maze_size, self.goal_index, self.start_index = solverFuncs.convert_maze(self.mazeName)
            self.mazeoption_size = ((self.maze_size[0]*3)+4 if (self.maze_size[0]*3)+4 >= 200 else 200,
                                    (self.maze_size[1]*3)+4 if (self.maze_size[1]*3)+4 >= 200 else 200)
            print(self.mazeoption_size)
            self.maze_plot = animationFuncs.create_plot(self.maze)
            self.open_list = [solverFuncs.Node(None, self.start_index, 0)]
            self.open_list[0].calc_vals(self.goal_index)
            self.closed_list = []
            self.maze_frame.config(width=self.mazeoption_size[0] if self.mazeoption_size[0] > 216 else 216,
                                   height=self.mazeoption_size[1]+134)
            self.canvas.get_tk_widget().place(width=self.mazeoption_size[0], height=self.mazeoption_size[1],
                                              x=(216-self.mazeoption_size[0])/2 if (216-self.mazeoption_size[0])/2 > 0
                                              else 0)
            self.solve_options_frame.place(y=self.mazeoption_size[1], x=(self.mazeoption_size[0] - 216) / 2 if
                                     (self.mazeoption_size[0]-216)/2 > 0 else 0)
            self.maze_frame.update()
            self.im = self.plot1.imshow(self.maze_plot, "tab20")
            self.plot(self.maze_plot)
            self.solved = False

    def move_anim(self):
        fin = True
        if self.state == "solve":
            if self.solve_options_frame.winfo_y() < 353:  # to x > 200
                self.solve_options_frame.place(y=self.solve_options_frame.winfo_y()+1)

            elif self.generate_options_frame.winfo_x() > 0:  # to x < 316
                self.generate_options_frame.place(x=self.generate_options_frame.winfo_x()-1)
            else:
                fin = False

        elif self.state == "generate":
            if self.generate_options_frame.winfo_x() < 321:
                self.generate_options_frame.place(x=self.generate_options_frame.winfo_x()+1)

            elif self.solve_options_frame.winfo_y() > 200:
                self.solve_options_frame.place(y=self.solve_options_frame.winfo_y()-1)
            else:
                fin = False

        if fin:
            self.root.after(3, self.move_anim)
        else:
            self.state = "generate" if self.state == "solve" else "solve"

    def update_random_label(self, k):
        self.randomness_label.configure(text=f"The random choice percentage is {self.randomness_var.get()}%"
                                             f"\nThe determined choice percentage is {100-self.randomness_var.get()}%")

    #def gen_maze(self):



if __name__ == "__main__":
    window = MazeWindow()
