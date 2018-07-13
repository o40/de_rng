from room import *
from rotation import *


def room_has_exit_near_grid_edge(room, grid_size, margin=3):
    """
    Check if the room has en exit that ends up closer than
    "margin" units from the grid edge
    """
    for exit in room.exits:
        ro_x, ro_y = rotation_offset(exit.rotation)
        x = exit.x + ro_x
        y = exit.y + ro_y
        if ((x - margin < 0) or (y - margin < 0) or
           (x + margin >= grid_size) or (y + margin >= grid_size)):
            return True
    return False


def room_blocks_exit_from_room_in_world(room, world, origin_exit):
    offset_x, offset_y = rotation_offset(origin_exit.rotation)
    excluded_exit = RoomExit(x=origin_exit.x + offset_x,
                             y=origin_exit.y + offset_y,
                             rotation=opposite_rotation(origin_exit.rotation))
    exits_to_check = [exit for exit in room.exits if exit != excluded_exit]
    for exit in exits_to_check:
        for room in world:
            # Check if the exit ends up "overlapping" another room
            exit_offset_x, exit_offset_y = rotation_offset(origin_exit.rotation)
            # Hackish way of doing this. Refactor!
            r = Room(x=exit.x + exit_offset_x,
                     y=exit.y + exit_offset_y,
                     width=1, height=1,
                     name="", type="", rotation=0, exits=[])
            if r.overlaps(room):
                return True
