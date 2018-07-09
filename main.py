import os
import json
import random
from pprint import pprint
from tkinter import *
from collections import defaultdict
from rect import *
from room import *
from plot import *
from direction import *

"""

TODO:
* Randomize order in which exits in rooms are checked for match.

"""

# Plot settings
plot_scale = 10

# Grid for occupied areas in the map
grid_size = 40

# Debugging purposes
# random.seed(2)
max_rooms = 10

# Tkinter canvas
master = Tk()
canvas = Canvas(master,
                width=plot_scale * grid_size,
                height=plot_scale * grid_size)


def get_rooms():
    rooms = defaultdict(list)
    for file in os.listdir("rooms"):
        with open("rooms/" + file, 'r') as f:
            prefab_room = PrefabRoom(json.load(f))
            rooms[prefab_room.name] = prefab_room
    return rooms


def add_room(room_list, prefab_room_list, name, x, y):
    print("Adding room {} @ {} {}".format(name, x, y))
    if name in prefab_room_list.keys():
        room_list.append(Room(name, x, y, 0, prefab_room_list[name].exits))


def add_room_to_random_exit(rooms_in_map, prefab_room_list):
    unconnected_exits = get_unconnected_exits(rooms_in_map)
    uc_exit = random.choice(unconnected_exits)

    # TODO: Randomize this
    tries = 0
    while tries < 30:
        random_room_name = random.choice(list(prefab_room_list.keys()))
        prefab_room = prefab_room_list[random_room_name]
        print("Trying to add:", random_room_name)
        for prefab_exit in prefab_room.exits:
            dir_offset_x, dir_offset_y = rotation_offset(uc_exit.rotation)
            if prefab_exit.rotation == opposite_rotation(uc_exit.rotation):
                if (uc_exit.rotation == 90):
                    new_room_x = uc_exit.x - prefab_exit.x
                    new_room_y = uc_exit.y + 1
                if (uc_exit.rotation == 270):
                    new_room_x = uc_exit.x - prefab_exit.x
                    new_room_y = uc_exit.y - prefab_exit.height
                if (uc_exit.rotation == 0):
                    new_room_x = uc_exit.x + 1
                    new_room_y = uc_exit.y - prefab_exit.y
                if (uc_exit.rotation == 180):
                    new_room_x = uc_exit.x - prefab_room.width
                    new_room_y = uc_exit.y - prefab_exit.y
                # TODO: Check if room fits in map area (no overlap or OOB)
                if not new_room_overlap_or_oob(rooms_in_map,
                                               prefab_room.name,
                                               prefab_room_list,
                                               new_room_x,
                                               new_room_y):
                    add_room(rooms_in_map,
                             prefab_room_list,
                             prefab_room.name,
                             new_room_x,
                             new_room_y)
                    return True
        tries += 1

    print("Could not find a room that matches exit:",
          uc_exit.x, uc_exit.y, uc_exit.rotation)
    return False


def new_room_overlap_or_oob(rooms_in_map, name, prefab_room_list, x, y):
    # Get rectangle for current room
    new_rect = Rect(x,
                    y,
                    prefab_room_list[name].width,
                    prefab_room_list[name].height)

    if (new_rect.x < 0 or (new_rect.x2 >= grid_size) or
            new_rect.y < 0 or (new_rect.y2 >= grid_size)):
            return True

    # Loop over the rectangles for all rooms in map
    for room in rooms_in_map:
        room_rect = Rect(room.x,
                         room.y,
                         prefab_room_list[name].width,
                         prefab_room_list[name].height)
        if new_rect.overlaps(room_rect):
            return True
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
            if (exit_to_match.rotation == opposite_rotation(exit.rotation)):
                dir_offset_x, dir_offset_y = (
                    rotation_offset(exit_to_match.rotation)
                )
                if ((exit_to_match.x + dir_offset_x) == exit.x and
                        (exit_to_match.y + dir_offset_y) == exit.y):
                            return True
    return False


def main():
    prefab_room_list = get_rooms()

    # Array of rooms
    rooms_in_map = []

    add_room(rooms_in_map, prefab_room_list, "mid1", 10, 10)

    # room_added = True
    # while (room_added and len(rooms_in_map) < max_rooms):
    #    room_added = add_room_to_random_exit(rooms_in_map, prefab_room_list)

    uc_exits = get_unconnected_exits(rooms_in_map)
    plot_rooms(canvas, rooms_in_map, uc_exits, prefab_room_list, plot_scale)
    draw_grid(canvas, grid_size, plot_scale)

    canvas.pack()
    mainloop()


if __name__ == "__main__":
    main()
