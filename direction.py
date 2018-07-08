from enum import Enum


class Directions(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


def string_to_direction(string):
    if string == "left":
        return Directions.LEFT
    if string == "right":
        return Directions.RIGHT
    if string == "down":
        return Directions.DOWN
    if string == "up":
        return Directions.UP


def opposite_direction(direction):
    if direction == Directions.UP:
        return Directions.DOWN
    if direction == Directions.DOWN:
        return Directions.UP
    if direction == Directions.LEFT:
        return Directions.RIGHT
    if direction == Directions.RIGHT:
        return Directions.LEFT
    return "INVALID"


def direction_offset(direction):
    if direction == Directions.RIGHT:
        return 1, 0
    if direction == Directions.LEFT:
        return -1, 0
    if direction == Directions.UP:
        return 0, -1
    if direction == Directions.DOWN:
        return 0, 1
