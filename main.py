import os
import json
import random
from pprint import pprint
from tkinter import *
from collections import defaultdict
from enum import Enum


class Directions(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


def string_to_direction(string):
    if string == "left":
        return Directions.LEFT
    if string == "right":
        return Directions.RIGHT
    if string == "down":
        return Directions.DOWN
    if string == "up":
        return Directions.UP


# Plot settings
plot_scale = 10

# Grid for occupied areas in the map
grid_size = 40
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]

# Tkinter canvas
master = Tk()
canvas = Canvas(master,
                width=plot_scale * grid_size,
                height=plot_scale * grid_size)


def get_rooms():
    rooms = defaultdict(list)
    for file in os.listdir("rooms"):
        with open("rooms/" + file, 'r') as f:
            j = json.load(f)
            exits = []
            for exit in j['exits']:
                exits.append([exit['x'],
                              exit['y'],
                              string_to_direction(exit['direction'])])
            rooms[j['name']] = (j['width'], j['height'], j['type'], exits)
    return rooms


prefab_room_list = get_rooms()

# rooms_in_map struct
# x, y, name, rotation (0, 90, 180, 270)
rooms_in_map = []

# unconnected exits contains x, y, direction
unconnected_exits = []


def add_room(name, x, y):
    if name in prefab_room_list.keys():
        rooms_in_map.append([name, x, y, 0])
        rx, ry, rtype, rexits = prefab_room_list[name]
        for exit in rexits:
            ex, ey, edir = exit
            unconnected_exits.append([x + ex, y + ey, edir])


def plot_rooms(rooms_in_map, prefab_room_list, unconnected_exits):
    for room in rooms_in_map:
        name, x, y, rot = room
        prefab_width, prefab_height, prefab_type, prefab_exits = prefab_room_list[name]
        x2 = x + prefab_width
        y2 = y + prefab_height
        canvas.create_rectangle(
            x * plot_scale,
            y * plot_scale,
            x2 * plot_scale,
            y2 * plot_scale,
            outline="blue", fill="lightgray")
        for exit in prefab_exits:
            ex, ey, edir = exit
            absolute_ex = x + ex
            absolute_ey = y + ey
            canvas.create_polygon(create_polygon_points(absolute_ex, absolute_ey, edir), fill="green")
    # Plot unconnected exits
    for exit in unconnected_exits:
        ex, ey, edir = exit
        canvas.create_polygon(create_polygon_points(ex, ey, edir), fill="red")


def create_polygon_points(x, y, direction):
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


def draw_grid(grid_size, spacing):
    for x in range(0, grid_size, spacing):
        canvas.create_line(x * spacing, 0, x * spacing, grid_size * spacing, dash=(3,1))
        canvas.create_line(0, x * spacing, grid_size * spacing, (x * spacing), dash=(3,1))


def opposite_direction(direction):
    if direction == Directions.UP:
        return Directions.DOWN
    if direction == Directions.DOWN:
        return Directions.UP
    if direction == Directions.LEFT:
        return Directions.RIGHT
    if direction == Directions.RIGHT:
        return Directions.LEFT
    return "INVALID"


def direction_offset(direction):
    if direction == Directions.RIGHT:
        return 1, 0
    if direction == Directions.LEFT:
        return -1, 0
    if direction == Directions.UP:
        return 0, -1
    if direction == Directions.DOWN:
        return 0, 1


def remove_connected_exits_from_unconnected_list():
    """
    Remove exits that is connected to other exits.
    TODO: Figure out why there are duplicates.
    """
    connected_exits = []
    for exit1 in unconnected_exits:
        for exit2 in unconnected_exits:
            exit1_x, exit1_y, exit1_dir = exit1
            exit2_x, exit2_y, exit2_dir = exit2
            if exit1_dir == opposite_direction(exit2_dir):
                dir_offset_x, dir_offset_y = direction_offset(exit1_dir)
                if (exit1_x + dir_offset_x == exit2_x) and (exit1_y + dir_offset_y == exit2_y):
                    connected_exits.append(exit1)
    for exit in connected_exits:
        if exit in unconnected_exits:
            unconnected_exits.remove(exit)


def add_room_to_random_exit():
    unconnected_exit = random.choice(unconnected_exits)
    uce_x, uce_y, uce_dir = unconnected_exit
    print("unconnected exit found at {} {} direction: {}"
          .format(uce_x, uce_y, uce_dir))
    # Find a room that has an exit that fits
    for prefab_name, prefab_room in prefab_room_list.items():
        prefab_type, prefab_width, prefab_height, prefab_exits = prefab_room
        for prefab_exit in prefab_exits:
            print(prefab_exit)
            e_x, e_y, e_dir = prefab_exit
            dir_offset_x, dir_offset_y = direction_offset(uce_dir)
            if e_dir == opposite_direction(uce_dir):
                print("Found exit to match the unconnected exit")
                new_room_x = uce_x + e_x + dir_offset_x
                new_room_y = uce_y + e_y + dir_offset_y
                add_room(prefab_name, new_room_x, new_room_y)
                return True
    return False


add_room("mid1", 10, 10)
room_added = True
while (room_added and len(rooms_in_map) < 2):
    room_added = add_room_to_random_exit()
    remove_connected_exits_from_unconnected_list()


# Append random room to any available exits


plot_rooms(rooms_in_map, prefab_room_list, unconnected_exits)
draw_grid(grid_size, plot_scale)

canvas.pack()
mainloop()
