from direction import *


class Room:
    def __init__(self, name, x, y, width, height, rotation, exits):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.exits = []
        # Add offset and rotation
        for exit in exits:
            self.exits.append(RoomExit(x + exit.x,
                                       y + exit.y,
                                       exit.rotation))

    def rotate(self, rotation):
        """
        Rotate the room counter clockwise (in degrees)
        """
        if (rotation % 90) != 0:
            raise ValueError("Can only rotate in 90 degree steps")

        self.rotation = (self.rotation + rotation) % 360
        for exit in self.exits:
            rotate_exit(exit, self.width, self.height, rotation)
        if (rotation % 180) != 0:
            self.width, self.height = self.height, self.width


class RoomExit():
    """
    Relative to the prefab room or absolute position in map
    """
    def __init__(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation


class PrefabRoom:
    def __init__(self, prefab_json):
        self.name = prefab_json['name']
        self.width = int(prefab_json['width'])
        self.height = int(prefab_json['height'])
        self.type = prefab_json['type']
        self.exits = []
        for exit in prefab_json['exits']:
            x = exit['x']
            y = exit['y']
            direction_str = exit['direction']
            rotation = string_to_rotation(direction_str)
            self.exits.append(RoomExit(x, y, rotation))


def rotate_exit(exit, width, height, rotation):
    """
    The 0.5 is to get the middle position of a cell rather than bottom left.
    Exits also needs to be adjusted if width != height
    """
    mid_x = width / 2
    mid_y = height / 2
    theta = (rotation / 180) * math.pi

    # Adjust to middle of cell
    x = exit.x + 0.5
    y = exit.y + 0.5

    # Set origo in middle of rectangle
    x = x - mid_x
    y = y - mid_y

    # Do rotation
    exit.x = math.cos(theta) * x - math.sin(theta) * y
    exit.y = math.sin(theta) * x + math.cos(theta) * y

    # Set origo in bottom left of rectangle (if rotated 90 or 270, inverse adjustment)
    if rotation in (0, 180):
        exit.x += mid_x
        exit.y += mid_y
    else:
        exit.x += mid_y
        exit.y += mid_x

    # Adjust to bottom right corner of cell
    exit.x -= 0.5
    exit.y -= 0.5

    # Round (TODO: Round better?)
    exit.x = int(round(exit.x))
    exit.y = int(round(exit.y))

    exit.rotation = (exit.rotation + rotation) % 360


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
