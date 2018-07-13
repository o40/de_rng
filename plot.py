from room import *


def plot_rooms(canvas, world, unconnected_exits, plot_scale, grid_size):
    canvas_width = int(canvas.cget("width"))
    canvas_height = int(canvas.cget("height"))
    for room in world:
        x = room.x
        y = grid_size - room.y
        x2 = x + room.width
        y2 = y - room.height
        canvas.create_rectangle(
            x * plot_scale,
            y2 * plot_scale,
            x2 * plot_scale,
            y * plot_scale,
            outline="blue", fill="pink")
        for exit in room.exits:
            canvas.create_polygon(create_polygon_points(exit.x,
                                                        grid_size - exit.y,
                                                        exit.rotation,
                                                        plot_scale),
                                  fill="green")

    for exit in unconnected_exits:
        canvas.create_polygon(create_polygon_points(exit.x,
                                                    grid_size - exit.y,
                                                    exit.rotation,
                                                    plot_scale),
                              fill="red")


def create_polygon_points(x, y, rotation, plot_scale):
    points = []
    cell_mid_x = x + 0.5
    cell_mid_y = y - 0.5
    points.append([cell_mid_x * plot_scale, cell_mid_y * plot_scale])
    if rotation in (0, 270):
        points.append([(x + 1) * plot_scale, y * plot_scale])
    if rotation in (270, 180):
        points.append([x * plot_scale, y * plot_scale])
    if rotation in (180, 90):
        points.append([x * plot_scale, (y - 1) * plot_scale])
    if rotation in (90, 0):
        points.append([(x + 1) * plot_scale, (y - 1) * plot_scale])
    return points


def draw_grid(canvas, grid_size, plot_scale, spacing):
    canvas_width = canvas.cget("width")
    canvas_height = canvas.cget("height")
    for line_offset in range(0, grid_size * plot_scale, plot_scale * spacing):
        canvas.create_line(line_offset, 0, line_offset, canvas_height,
                           dash=(3, 1))
        canvas.create_line(0, line_offset, canvas_width, line_offset,
                           dash=(3, 1))
