from rotation import *
from rect import *
from json import JSONEncoder


class RoomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Room:
    def __init__(self, name, x, y, width, height, rotation, exits, type):
        self.name = name
        self.type = type
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

    def move(self, x, y):
        xdiff = x - self.x
        ydiff = y - self.y
        self.x, self.y = x, y
        for exit in self.exits:
            exit.x += xdiff
            exit.y += ydiff

    def overlaps(self, room):
        room_rect = Rect(room.x, room.y, room.width, room.height)
        self_room_rect = Rect(self.x, self.y, self.width, self.height)
        return room_rect.overlaps(self_room_rect)

    def is_in_grid(self, grid_size, margin=0):
        room_rect = Rect(x=self.x,
                         y=self.y,
                         width=self.width,
                         height=self.height)
        return room_rect.is_in_grid(grid_size, margin)


class RoomExit():
    """
    Relative to the prefab room or absolute position in map
    """
    def __init__(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation

    def __eq__(self, exit):
        return (self.x == exit.x and
                self.y == exit.y and
                self.rotation == exit.rotation)

    def mirror(self):
        """
        Return a mirrored exit that matches this exit
        """
        off_x, off_y = rotation_offset(self.rotation)
        x = self.x + off_x
        y = self.y + off_y
        return RoomExit(x, y, opposite_rotation(self.rotation))

    def deserialize(json):
        x = json['x']
        y = json['y']
        direction_str = json['direction']
        rotation = string_to_rotation(direction_str)
        return RoomExit(x, y, rotation)


def create_room_from_json(room_json):
    # name, x, y, width, height, rotation, exits

    exits = []
    for exit in room_json['exits']:
            exits.append(RoomExit.deserialize(exit))

    return Room(name=room_json['name'],
                x=0,
                y=0,
                width=int(room_json['width']),
                height=int(room_json['height']),
                rotation=0,
                exits=exits,
                type=room_json['type'])


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
