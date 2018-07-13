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
* Ditch the 0.5 offset?
* Add checker when adding room so that an exit does not end up in already existing room
* Add checker when adding room so that no new exit is near world edge (2 squares?)
* Add spawns, bombsites, mid and large rooms first before adding rest
* Verify that all areas of map can be reached. Should be possible to traverse.
"""

# Plot settings
plot_scale = 10

# Grid for occupied areas in the map
grid_size = 40

# Debugging purposes
# random.seed(4)
max_rooms = 50

# Tkinter canvas
master = Tk()
canvas = Canvas(master,
                width=plot_scale * grid_size,
                height=plot_scale * grid_size)
master.update()


def get_rooms():
    """
    Read the prefab room json files from the rooms folder and parse
    them to Room objects which then is placed in a dictionary with the
    room name as key.
    """
    rooms = defaultdict(list)
    for file in os.listdir("rooms"):
        with open("rooms/" + file, 'r') as f:
            prefab_room = create_room_from_json(json.load(f))
            rooms[prefab_room.name] = prefab_room
    return rooms


def add_room(world, room):
    """
    Add a room to the world list
    """
    world.append(room)


def get_matching_exit(exit_to_match, exit_list):
    """
    Get exit from room that matches the rotation of the given exit
    """
    shuffled_exits = exit_list[:]
    for exit in shuffled_exits:
        if exit.rotation != opposite_rotation(exit_to_match.rotation):
            continue
        return exit
    return None


def origo_offset_from_exit(uc_exit, prefab_exit, prefab_room):
    """
    Get the coordinates to where the exit ends up outside the room
    """
    if (uc_exit.rotation == 90):
        return -prefab_exit.x, 1
    if (uc_exit.rotation == 270):
        return -prefab_exit.x, -prefab_room.height
    if (uc_exit.rotation == 0):
        return 1, -prefab_exit.y
    if (uc_exit.rotation == 180):
        return -prefab_room.width, -prefab_exit.y


def get_random_unconnected_exit(world):
    """
    Compose a list of exits that are not connected and return
    a random exit from the list
    """
    # TODO: How to handle when list is empty?
    unconnected_exits = get_unconnected_exits(world)
    return random.choice(unconnected_exits)


def get_random_room(room_list):
    """
    Get a copy of a random room in the room list. The room is
    rotated randomly before returned.
    """
    random_room_name = random.choice(list(room_list.keys()))
    room = copy.deepcopy(room_list[random_room_name])
    rotation = random.choice([0, 90, 180, 270])
    room.rotate(rotation)
    return room


def get_coordinates_for_matched_prefab_room(uc_exit, prefab_exit, prefab_room):
    """
    Get the coordinates for the bottom left coordinates to place the room
    so that the given exit lines up with the exit from the room to add.
    """
    dir_offset_x, dir_offset_y = rotation_offset(uc_exit.rotation)
    origo_offset_x, origo_offset_y = origo_offset_from_exit(uc_exit,
                                                            prefab_exit,
                                                            prefab_room)
    new_x = uc_exit.x + origo_offset_x
    new_y = uc_exit.y + origo_offset_y
    return new_x, new_y


def add_room_to_random_exit(world, prefab_room_list):
    """
    Find a random exit in the current world and try to attach
    a room to it.
    """
    tries = 0
    while tries < 300:
        tries += 1

        # get random exit to connect
        try:
            uc_exit = get_random_unconnected_exit(world)
        except IndexError:
            print("There are no unconnected exits")
            return False

        # Get random room from list (with random rotation)
        prefab_room = get_random_room(prefab_room_list)

        # Get exit from room that matches the unconnected exit
        prefab_exit = get_matching_exit(uc_exit, prefab_room.exits)

        if prefab_exit is None:
            continue

        x, y = get_coordinates_for_matched_prefab_room(uc_exit,
                                                       prefab_exit,
                                                       prefab_room)

        prefab_room.move(x, y)

        if not verify_room_placement(world, prefab_room, uc_exit):
            add_room(world, prefab_room)
            return True

    print("Could not find a room that matches exit:",
          uc_exit.x, uc_exit.y, uc_exit.rotation)
    return False


def verify_room_placement(world, room, uc_exit):
    """
    Verify that the room can be placed in the world without breaking
    the rules:
    * The room must be in the grid
    * The room can not overlap another room
    * The room can not block an exit from another room
    * The room exit can not be too close to the world edge
    """
    # Check if room is in grid
    if not room.is_in_grid(grid_size):
        return True

    # Loop over the rectangles for all rooms in map
    for world_room in world:
        if world_room.overlaps(room):
            return True

    for exit in room.exits:
        margin = 3
        ro_x, ro_y = rotation_offset(exit.rotation)
        x = exit.x + ro_x
        y = exit.y + ro_y

        if ((x - margin < 0) or (y - margin < 0) or
           (x + margin >= grid_size) or (y + margin >= grid_size)):
            return True

    # TODO: Check that this rect does not block exit from other room

    # Create exit to exclude when looping over list
    offset_x, offset_y = rotation_offset(uc_exit.rotation)
    excluded_exit = RoomExit(x=uc_exit.x + offset_x,
                             y=uc_exit.y + offset_y,
                             rotation=opposite_rotation(uc_exit.rotation))
    exits_to_check = [exit for exit in room.exits if exit != excluded_exit]
    for exit in exits_to_check:
        for room in world:
            # Check if the exit ends up "overlapping" another room
            exit_offset_x, exit_offset_y = rotation_offset(uc_exit.rotation)
            # Hackish way of doing this. Refactor!
            r = Room(x=exit.x + exit_offset_x,
                     y=exit.y + exit_offset_y,
                     width=1, height=1,
                     name="", type="", rotation=0, exits=[])
            if r.overlaps(room):
                return True

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
