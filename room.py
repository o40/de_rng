from direction import *


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
            self.exits.append(RoomExit(x,
                                       self.height - exit['y'] - 1,
                                       direction))
