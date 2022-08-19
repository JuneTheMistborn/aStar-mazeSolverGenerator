def create_plot(maze):
    anim = []
    for y_ind, y_val in enumerate(maze):
        anim.append([])
        for x in y_val:
            if x == "-":  # if text is g, node is goal
                anim[y_ind].append(19)
            elif x == "x":  # if text is o, node is start
                anim[y_ind].append(0)
            elif x == "o":
                anim[y_ind].append(4)
            else:
                anim[y_ind].append(16)

    return anim


def change_plot(maze_plot, new_open, new_closed, current_node):
    for node in new_open:
        maze_plot[node.index[0]][node.index[1]] = 12

    if int(maze_plot[new_closed.index[0]][new_closed.index[1]]) != 4:
        maze_plot[new_closed.index[0]][new_closed.index[1]] = 13
        maze_plot[current_node.index[0]][current_node.index[1]] = 6
    return maze_plot


def show_finished(maze_plot, finished_list):
    for node in finished_list:
        maze_plot[node[0]][node[1]] = 7

    return maze_plot
