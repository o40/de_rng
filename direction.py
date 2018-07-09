import math


def string_to_rotation(string):
    if string == "left":
        return 0
    if string == "up":
        return 90
    if string == "right":
        return 180
    if string == "down":
        return 270


def opposite_rotation(rotation):
    return (rotation + 180) % 360


def rotation_offset(rotation):
    # TODO: Fix coordinate system so that y+ means up
    return int(math.cos(rotation * math.pi / 180)), \
           -(int(math.sin(rotation * math.pi / 180)))
