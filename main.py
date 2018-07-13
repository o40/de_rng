import os
import json
import random
import copy
from tkinter import *
from collections import defaultdict
from rect import *
from room import *
from plot import *
from rotation import *

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
random.seed(4)
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
            prefab_room = create_room_from_json(json.load(f))
            rooms[prefab_room.name] = prefab_room
    return rooms


def add_room(room_list, room):
    room_list.append(room)


def get_matching_exit(exit_to_match, exit_list):
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


def get_random_unconnected_exit(world):
    unconnected_exits = get_unconnected_exits(world)
    return random.choice(unconnected_exits)


def get_random_prefab_room(prefab_room_list):
    random_room_name = random.choice(list(prefab_room_list.keys()))
    prefab_room = copy.deepcopy(prefab_room_list[random_room_name])
    # Rotate the room randomly
    rotation = random.choice([0, 90, 180, 270])
    prefab_room.rotate(rotation)
    return prefab_room


def get_coordinates_for_matched_prefab_room(uc_exit, prefab_exit, prefab_room):
    dir_offset_x, dir_offset_y = rotation_offset(uc_exit.rotation)
    origo_offset_x, origo_offset_y = origo_offset_from_exit(uc_exit, prefab_exit, prefab_room)
    new_x = uc_exit.x + origo_offset_x
    new_y = uc_exit.y + origo_offset_y
    return new_x, new_y


def add_room_to_random_exit(world, prefab_room_list):
    tries = 0
    while tries < 300:
        tries += 1

        # get random exit to connect
        uc_exit = get_random_unconnected_exit(world)

        # Get random room from list (with random rotation)
        prefab_room = get_random_prefab_room(prefab_room_list)

        # Get exit from room that matches the unconnected exit
        prefab_exit = get_matching_exit(uc_exit, prefab_room.exits)

        if prefab_exit is None:
            continue

        new_room_x, new_room_y = get_coordinates_for_matched_prefab_room(uc_exit, prefab_exit, prefab_room)

        prefab_room.move(new_room_x, new_room_y)

        # TODO: Check if room fits in map area (no overlap or OOB, or blocks and exit)
        if not new_room_overlap_or_oob(world, prefab_room, new_room_x, new_room_y):
            add_room(world, prefab_room)
            return True

    print("Could not find a room that matches exit:",
          uc_exit.x, uc_exit.y, uc_exit.rotation)
    return False


def new_room_overlap_or_oob(world, room, x, y):
    # Check if room is in grid
    if not room.is_in_grid(grid_size):
        return True

    # Loop over the rectangles for all rooms in map
    for world_room in world:
        if world_room.overlaps(room):
            return True

    # TODO: Check that this rect does not block exit from other room

    return False


def main():
    prefab_room_list = get_rooms()

    # The world is an array of rooms
    world = []
    room = copy.deepcopy(prefab_room_list["mid1"])
    room.move(10, 10)
    add_room(world, room)

    room_added = True
    while (room_added and len(world) < max_rooms):
        room_added = add_room_to_random_exit(world, prefab_room_list)

    uc_exits = get_unconnected_exits(world)
    plot_rooms(canvas, world, uc_exits, plot_scale, grid_size)
    draw_grid(canvas, grid_size, plot_scale, 4)

    canvas.pack()
    mainloop()


if __name__ == "__main__":
    main()
