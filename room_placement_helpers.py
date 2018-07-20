from room import *
from rotation import *
import copy


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


def room_in_world_has_blocked_exit(world):
    unconnected_exits = get_unconnected_exits(world)
    for exit in unconnected_exits:
        # Check if the exit ends up "overlapping" another room
        mirror_exit = exit.mirror()
        # Hackish way of doing this. Refactor!
        r = Room(x=mirror_exit.x,
                 y=mirror_exit.y,
                 width=1, height=1,
                 name="", type="", rotation=0, exits=[])
        for room in world:
            if r.overlaps(room):
                return True
    return False


def room_blocks_exit_from_room_in_world(room, world):
    world_copy = copy.deepcopy(world)
    world_copy.append(room)
    return room_in_world_has_blocked_exit(world_copy)
