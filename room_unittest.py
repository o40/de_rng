import unittest
from room import *
from rotation import *


class TestRoom(unittest.TestCase):

    def test_room_rotation_box_room(self):
        exits = []
        exits.append(RoomExit(x=0, y=0, rotation=270))

        # A 4x4 room at 0,0, with an exit at 0,0, facing down
        room = Room(name="test", type="test",
                    x=0, y=0,
                    width=4, height=4,
                    rotation=0,
                    exits=exits)

        room.rotate(90)
        self.assertEqual(room.rotation, 90)
        self.assertEqual(room.width, 4)
        self.assertEqual(room.height, 4)
        self.assertEqual(room.exits[0].x, 3)
        self.assertEqual(room.exits[0].y, 0)
        self.assertEqual(room.exits[0].rotation, 0)

        room.rotate(90)
        self.assertEqual(room.rotation, 180)
        self.assertEqual(room.width, 4)
        self.assertEqual(room.height, 4)
        self.assertEqual(room.exits[0].x, 3)
        self.assertEqual(room.exits[0].y, 3)
        self.assertEqual(room.exits[0].rotation, 90)

        room.rotate(90)
        self.assertEqual(room.rotation, 270)
        self.assertEqual(room.width, 4)
        self.assertEqual(room.height, 4)
        self.assertEqual(room.exits[0].x, 0)
        self.assertEqual(room.exits[0].y, 3)
        self.assertEqual(room.exits[0].rotation, 180)

        room.rotate(90)
        self.assertEqual(room.rotation, 0)
        self.assertEqual(room.width, 4)
        self.assertEqual(room.height, 4)
        self.assertEqual(room.exits[0].x, 0)
        self.assertEqual(room.exits[0].y, 0)
        self.assertEqual(room.exits[0].rotation, 270)

    def test_room_rotation_rectangular_room(self):
        exits = []
        exits.append(RoomExit(x=0, y=0, rotation=270))

        # A 4x2 room at 0,0, with an exit at 0,0, facing down
        room = Room(name="test", type="test",
                    x=0, y=0,
                    width=4, height=2,
                    rotation=0,
                    exits=exits)

        room.rotate(90)
        self.assertEqual(room.rotation, 90)
        self.assertEqual(room.width, 2)
        self.assertEqual(room.height, 4)
        self.assertEqual(room.exits[0].x, 1)
        self.assertEqual(room.exits[0].y, 0)
        self.assertEqual(room.exits[0].rotation, 0)

        room.rotate(90)
        self.assertEqual(room.rotation, 180)
        self.assertEqual(room.width, 4)
        self.assertEqual(room.height, 2)
        self.assertEqual(room.exits[0].x, 3)
        self.assertEqual(room.exits[0].y, 1)
        self.assertEqual(room.exits[0].rotation, 90)

        room.rotate(90)
        self.assertEqual(room.rotation, 270)
        self.assertEqual(room.width, 2)
        self.assertEqual(room.height, 4)
        self.assertEqual(room.exits[0].x, 0)
        self.assertEqual(room.exits[0].y, 3)
        self.assertEqual(room.exits[0].rotation, 180)

        room.rotate(90)
        self.assertEqual(room.rotation, 0)
        self.assertEqual(room.width, 4)
        self.assertEqual(room.height, 2)
        self.assertEqual(room.exits[0].x, 0)
        self.assertEqual(room.exits[0].y, 0)
        self.assertEqual(room.exits[0].rotation, 270)

    def test_room_rotation_more_difficult_rectangular_room(self):
        exits = []
        exits.append(RoomExit(x=0, y=1, rotation=180))

        # A 5x3 room at 0,0, with an exit at 0,1, facing left
        room = Room(name="test", type="test",
                    x=0, y=0,
                    width=5, height=3,
                    rotation=0,
                    exits=exits)

        room.rotate(90)
        self.assertEqual(room.rotation, 90)
        self.assertEqual(room.width, 3)
        self.assertEqual(room.height, 5)
        self.assertEqual(room.exits[0].x, 1)
        self.assertEqual(room.exits[0].y, 0)
        self.assertEqual(room.exits[0].rotation, 270)

        room.rotate(90)
        self.assertEqual(room.rotation, 180)
        self.assertEqual(room.width, 5)
        self.assertEqual(room.height, 3)
        self.assertEqual(room.exits[0].x, 4)
        self.assertEqual(room.exits[0].y, 1)
        self.assertEqual(room.exits[0].rotation, 0)

        room.rotate(90)
        self.assertEqual(room.rotation, 270)
        self.assertEqual(room.width, 3)
        self.assertEqual(room.height, 5)
        self.assertEqual(room.exits[0].x, 1)
        self.assertEqual(room.exits[0].y, 4)
        self.assertEqual(room.exits[0].rotation, 90)

        room.rotate(90)
        self.assertEqual(room.rotation, 0)
        self.assertEqual(room.width, 5)
        self.assertEqual(room.height, 3)
        self.assertEqual(room.exits[0].x, 0)
        self.assertEqual(room.exits[0].y, 1)
        self.assertEqual(room.exits[0].rotation, 180)


if __name__ == '__main__':
    unittest.main(exit=False)
