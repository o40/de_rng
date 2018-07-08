from room import *

def plot_rooms(canvas, rooms_in_map, unconnected_exits, prefab_room_list, plot_scale):
    for room in rooms_in_map:
        print("Plotting:", room.name, room.x, room.y)
        prefab_room = prefab_room_list[room.name]
        x2 = room.x + prefab_room.width
        y2 = room.y + prefab_room.height
        canvas.create_rectangle(
            room.x * plot_scale,
            room.y * plot_scale,
            x2 * plot_scale,
            y2 * plot_scale,
            outline="blue", fill="lightgray")
        for exit in prefab_room.exits:
            absolute_ex = room.x + exit.x
            absolute_ey = room.y + exit.y
            canvas.create_polygon(create_polygon_points(absolute_ex,
                                                        absolute_ey,
                                                        exit.direction,
                                                        plot_scale),
                                  fill="green")

    for exit in unconnected_exits:
        canvas.create_polygon(create_polygon_points(exit.x,
                                                    exit.y,
                                                    exit.direction,
                                                    plot_scale),
                              fill="red")


def create_polygon_points(x, y, direction, plot_scale):
    points = []
    half_cell_height = 0.5
    cell_mid_x = x + half_cell_height
    cell_mid_y = y + half_cell_height
    points.append([(cell_mid_x) * plot_scale, (cell_mid_y) * plot_scale])
    if direction in (Directions.UP, Directions.LEFT):
        points.append([x * plot_scale, y * plot_scale])
    if direction in (Directions.DOWN, Directions.LEFT):
        points.append([x * plot_scale, (y + 1) * plot_scale])
    if direction in (Directions.UP, Directions.RIGHT):
        points.append([(x + 1) * plot_scale, y * plot_scale])
    if direction in (Directions.DOWN, Directions.RIGHT):
        points.append([(x + 1) * plot_scale, (y + 1) * plot_scale])
    return points


def draw_grid(canvas, grid_size, spacing):
    for x in range(0, grid_size, spacing):
        canvas.create_line(x * spacing, 0, x * spacing, grid_size * spacing,
                           dash=(3, 1))
        canvas.create_line(0, x * spacing, grid_size * spacing, (x * spacing),
                           dash=(3, 1))
