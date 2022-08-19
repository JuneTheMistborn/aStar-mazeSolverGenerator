class Node:
    def __init__(self, parent, index, g):  # takes parent, index g value, and type of node
        self.g = g  # cost of moving to node
        self.h = 0  # heuristic cost to move from this node to goal
        self.f = 0  # overall value, g+h, lower is better node
        self.parent = parent  # parent of this node
        self.index = index  # index of node (y, x)

    def calc_vals(self, goal_index, h_weight=1, g_weight=1):  # calculate h and f values
        self.h = abs(self.index[0] - goal_index[0]) + abs(self.index[1] - goal_index[1])  # heuristic function,
        # absolute value of current node index - goal index
        self.f = (self.h*h_weight) + (self.g*g_weight)  # value of node, h + g, lower makes node "better"


def convert_maze(maze_file):
    with open(maze_file) as file:  # read file and create maze in nested list
        line_num = 0
        maze = []
        for line in file.readlines():
            maze.append([])  # new y list
            char_num = 0
            for char in line:
                if char.strip():
                    maze[line_num].append(char)  # new x val in y list
                if char == "g":
                    goal_index = (line_num, char_num)
                if char == "o":
                    start_index = (line_num, char_num)
                char_num += 1
            line_num += 1

    return maze, (len(maze)-1, len(maze[0])-1), goal_index, start_index


def a_star_step(maze, maze_size, goal_index, start_index, open_list, closed_list, h_weight=1, g_weight=1):
    lowest_f_value = open_list[0].f
    lowest_f_index = 0
    for node_ind, node in enumerate(open_list):
        if open_list[node_ind].f < lowest_f_value:
            lowest_f_value = node.f
            lowest_f_index = node_ind

    current_node = open_list[lowest_f_index]
    closed_list.append(open_list.pop(lowest_f_index))

    new_nodes = 0

    for ind_add in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_index = (current_node.index[0] - ind_add[0], current_node.index[1] - ind_add[1])
        if maze_size[0] >= new_index[0] >= 0 and maze_size[1] >= new_index[1] >= 0:

            if maze[new_index[0]][new_index[1]] == "g":
                path = [current_node.index]
                parent_node = current_node.parent
                while parent_node.index != start_index:
                    path.append(parent_node.index)
                    parent_node = parent_node.parent
                return open_list, closed_list, path, 0

            if maze[new_index[0]][new_index[1]] != "x":
                for node in open_list + closed_list:
                    if node.index == new_index:
                        break
                else:
                    new_node = Node(current_node, new_index, current_node.g + 1)
                    open_list.append(new_node)
                    open_list[len(open_list) - 1].calc_vals(goal_index, h_weight, g_weight)
                    new_nodes += 1

    if len(open_list) > 0:
        return open_list, closed_list, None, new_nodes

    else:
        return open_list, closed_list, [], new_nodes


def a_star_full(maze, maze_size, goal_index, start_index, h_weight=1, g_weight=1):
    open_list = [Node(None, start_index, 0)]
    open_list[0].calc_vals(goal_index, h_weight, g_weight)
    closed_list = []
    finished_path = None

    while len(open_list) > 0 and finished_path is None:
        open_list, closed_list, *finished_path = a_star_step(maze, maze_size, goal_index, start_index, open_list,
                                                             closed_list)

    if finished_path[0] is not None:
        return finished_path[0]


def write_solution(path, maze_txt, maze_name):
    maze_string = ""
    for y_ind, y_list in enumerate(maze_txt):
        for x_ind, x_char in enumerate(y_list):
            print("current index: " + str((y_ind, x_ind)))
            if (y_ind, x_ind) not in path:
                maze_string += x_char
            else:
                maze_string += "*"
        maze_string += "\n"
    with open(maze_name + "Solution.txt", "w+") as outFile:
        outFile.write(maze_string)
