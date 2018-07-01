import os
import json
import random
from pprint import pprint
from tkinter import *
from collections import defaultdict
from enum import Enum

# Plot settings
plot_scale = 10

# Grid for occupied areas in the map
grid_size = 40
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]


# Debugging purposes
random.seed(2)
max_rooms = 5


# Tkinter canvas
master = Tk()
canvas = Canvas(master,
                width=plot_scale * grid_size,
                height=plot_scale * grid_size)


class Directions(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class RoomExit():
    """
    Relative to the prefab room or absolute position in map
    """
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class PrefabRoom:
    def __init__(self, prefab_json):
        self.name = prefab_json['name']
        self.width = prefab_json['width']
        self.height = prefab_json['height']
        self.type = prefab_json['type']
        self.exits = []
        for exit in prefab_json['exits']:
            x = exit['x']
            y = exit['y']
            direction_str = exit['direction']
            direction = string_to_direction(direction_str)
            print("Adding exit for {} @ {},{} {}".format(
                  self.name, x, y, direction))
            self.exits.append(RoomExit(x,
                                       self.height - exit['y'] - 1,
                                       direction))


class Room:
    def __init__(self, name, x, y, rotation, exits):
        self.name = name
        self.x = x
        self.y = y
        self.rotation = rotation
        self.exits = []
        # Add offset and rotation
        for exit in exits:
            self.exits.append(RoomExit(x + exit.x,
                                       y + exit.y,
                                       exit.direction))


def get_rooms():
    rooms = defaultdict(list)
    for file in os.listdir("rooms"):
        with open("rooms/" + file, 'r') as f:
            prefab_room = PrefabRoom(json.load(f))
            rooms[prefab_room.name] = prefab_room
    return rooms


def string_to_direction(string):
    if string == "left":
        return Directions.LEFT
    if string == "right":
        return Directions.RIGHT
    if string == "down":
        return Directions.DOWN
    if string == "up":
        return Directions.UP


def add_room(room_list, prefab_room_list, name, x, y):
    print("Adding room {} @ {} {}".format(name, x, y))
    if name in prefab_room_list.keys():
        room_list.append(Room(name, x, y, 0, prefab_room_list[name].exits))
        prefab_room = prefab_room_list[name]
        print("Exits len:", len(prefab_room.exits))
        # for exit in prefab_room.exits:
#            # print("Adding unconnected exit @{},{}".format(exit.x, exit.y))
#            # unconnected_exits.append(RoomExit(x + exit.x,
#            #                                  y + exit.y,
#            #                                  exit.direction))


def plot_rooms(rooms_in_map, prefab_room_list, unconnected_exits):
    for room in rooms_in_map:
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
                                                        exit.direction),
                                  fill="green")
    # Plot unconnected exits
    for exit in unconnected_exits:
        canvas.create_polygon(create_polygon_points(exit.x,
                                                    exit.y,
                                                    exit.direction),
                              fill="red")


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
        canvas.create_line(x * spacing, 0, x * spacing, grid_size * spacing,
                           dash=(3, 1))
        canvas.create_line(0, x * spacing, grid_size * spacing, (x * spacing),
                           dash=(3, 1))


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
    print("There are {} unconnected exits".format(len(unconnected_exits)))
    connected_exits = []
    for exit1 in unconnected_exits:
        for exit2 in unconnected_exits:
            if exit1.direction == opposite_direction(exit2.direction):
                dir_offset_x, dir_offset_y = direction_offset(exit1.direction)
                if ((exit1.x + dir_offset_x) == exit2.x and
                        (exit1.y + dir_offset_y) == exit2.y):
                    connected_exits.append(exit1)
    for exit in connected_exits:
        if exit in unconnected_exits:
            unconnected_exits.remove(exit)


def add_room_to_random_exit():
    uc_exit = random.choice(unconnected_exits)

    print("unconnected exit found at {} {} direction: {}"
          .format(uc_exit.x, uc_exit.y, uc_exit.direction))
    # Find a room that has an exit that fits
    # TODO: Randomize this
    tries = 0
    while tries < 30:
        random_room_name = random.choice(list(prefab_room_list.keys()))
        prefab_room = prefab_room_list[random_room_name]
        print("Trying to add:", random_room_name)
        for prefab_exit in prefab_room.exits:
            dir_offset_x, dir_offset_y = direction_offset(uc_exit.direction)
            if prefab_exit.direction == opposite_direction(uc_exit.direction):
                if (uc_exit.direction in (Directions.UP, Directions.DOWN)):
                    print("Unhandled direction")
                    continue
                if (uc_exit.direction == Directions.RIGHT):
                    new_room_x = uc_exit.x + 1
                    new_room_y = uc_exit.y - prefab_exit.y
                if (uc_exit.direction == Directions.LEFT):
                    new_room_x = uc_exit.x - prefab_room.width
                    new_room_y = uc_exit.y - prefab_exit.y
                # TODO: Check if room fits in map area (no overlap or OOB)
                if not new_room_overlap_or_oob(prefab_room.name,
                                               new_room_x,
                                               new_room_y):
                    add_room(prefab_room.name, new_room_x, new_room_y)
                    return True
        tries += 1

    print("Could not find a room that matches exit")
    return False


def new_room_overlap_or_oob(name, x, y):
    return False


def get_unconnected_exits(rooms):
    unconnected_exits = []
    for room in rooms:
        for exit in room.exits:
            if not get_matching_exit(exit, rooms):
                unconnected_exits.append(exit)
    return unconnected_exits


def get_matching_exit(exit_to_match, rooms):
    for room in rooms:
        for exit in room.exits:
            if (exit_to_match.direction == opposite_direction(exit.direction)):
                dir_offset_x, dir_offset_y = direction_offset(exit_to_match.direction)
                if ((exit_to_match.x + dir_offset_x) == exit.x and
                        (exit_to_match.y + dir_offset_y) == exit.y):
                            return True
    return False


def main():
    prefab_room_list = get_rooms()

    # Array of rooms
    rooms_in_map = []

    add_room(rooms_in_map, prefab_room_list, "mid1", 10, 10)
    uc_exits = get_unconnected_exits(rooms_in_map)


    # room_added = True
    #while (room_added and len(rooms_in_map) < max_rooms):
    #    room_added = add_room_to_random_exit()
    #    remove_connected_exits_from_unconnected_list()

    plot_rooms(rooms_in_map, prefab_room_list, uc_exits)
    draw_grid(grid_size, plot_scale)

    canvas.pack()
    mainloop()


if __name__ == "__main__":
    main()
