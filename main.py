import os
import json
import random
from tkinter import *
from collections import defaultdict
from rect import *
from room import *
from plot import *
from direction import *

"""

TODO:
* Randomize order in which exits in rooms are checked for match.
* Ditch the 0.5 offset?
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
master.update()


def get_rooms():
    rooms = defaultdict(list)
    for file in os.listdir("rooms"):
        with open("rooms/" + file, 'r') as f:
            prefab_room = PrefabRoom(json.load(f))
            rooms[prefab_room.name] = prefab_room
    return rooms


def add_room(room_list, prefab_room_list, name, x, y):
    if name in prefab_room_list.keys():
        prefab_room = prefab_room_list[name]
        room_list.append(Room(name, x, y, prefab_room.width, prefab_room.height, 0, prefab_room.exits))


def get_matching_exit(exit_to_match, exit_list):
    print(exit_list)
    shuffled_exits = exit_list[:]
    for exit in shuffled_exits:
        if exit.rotation != opposite_rotation(exit_to_match.rotation):
            continue
        return exit
    return None


def origo_offset_from_exit(uc_exit, prefab_exit, prefab_room):
    if (uc_exit.rotation == 90):
        return -prefab_exit.x, 1
    if (uc_exit.rotation == 270):
        return -prefab_exit.x, -prefab_room.height
    if (uc_exit.rotation == 0):
        return 1, -prefab_exit.y
    if (uc_exit.rotation == 180):
        return -prefab_room.width, -prefab_exit.y


def add_room_to_random_exit(rooms_in_map, prefab_room_list):
    unconnected_exits = get_unconnected_exits(rooms_in_map)
    uc_exit = random.choice(unconnected_exits)

    # TODO: Randomize this more, with rotation as well
    tries = 0
    while tries < 30:
        tries += 1
        random_room_name = random.choice(list(prefab_room_list.keys()))
        prefab_room = prefab_room_list[random_room_name]
        print("Trying to add:", random_room_name)

        prefab_exit = get_matching_exit(uc_exit, prefab_room.exits)

        if prefab_exit is None:
            continue

        # TODO: This is dirty, refactor!
        dir_offset_x, dir_offset_y = rotation_offset(uc_exit.rotation)
        origo_offset_x, origo_offset_y = origo_offset_from_exit(uc_exit, prefab_exit, prefab_room)
        new_room_x = uc_exit.x + origo_offset_x
        new_room_y = uc_exit.y + origo_offset_y

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

    print("Could not find a room that matches exit:",
          uc_exit.x, uc_exit.y, uc_exit.rotation)
    return False


def new_room_overlap_or_oob(rooms_in_map, name, prefab_room_list, x, y):
    # Get rectangle for current room
    new_rect = Rect(x,
                    y,
                    prefab_room_list[name].width,
                    prefab_room_list[name].height)

    # Check if rectangle is in grid
    if not new_rect.is_in_grid(grid_size):
        return True

    # Loop over the rectangles for all rooms in map
    for room in rooms_in_map:
        room_rect = Rect(room.x,
                         room.y,
                         prefab_room_list[name].width,
                         prefab_room_list[name].height)
        if new_rect.overlaps(room_rect):
            return True

    # TODO: Check that this rect does not block exit from other room

    return False


def main():
    prefab_room_list = get_rooms()

    # Array of rooms
    rooms_in_map = []

    add_room(rooms_in_map, prefab_room_list, "mid1", 10, 10)

    room_added = True
    while (room_added and len(rooms_in_map) < max_rooms):
        room_added = add_room_to_random_exit(rooms_in_map, prefab_room_list)

    uc_exits = get_unconnected_exits(rooms_in_map)
    plot_rooms(canvas, rooms_in_map, uc_exits, prefab_room_list, plot_scale, grid_size)
    draw_grid(canvas, grid_size, plot_scale, 4)

    canvas.pack()
    mainloop()


if __name__ == "__main__":
    main()
