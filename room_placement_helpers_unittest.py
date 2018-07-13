import unittest
from room import *
from rotation import *
from room_placement_helpers import *

class TestRoomPlacementHelpers(unittest.TestCase):

    def test_room_exits_near_grid_edge(self):

        grid_size = 12
        margin = 3

        # room_has_exit_near_grid_edge
        exits = []
        exits.append(RoomExit(x=2, y=1, rotation=0))
        exits.append(RoomExit(x=1, y=2, rotation=90))
        exits.append(RoomExit(x=0, y=1, rotation=180))
        exits.append(RoomExit(x=1, y=0, rotation=270))

        # A 3x3 room at 0,0, with an exit on all sides
        room = Room(name="test", type="test",
                    x=0, y=0,
                    width=3, height=3,
                    rotation=0,
                    exits=exits)

        # Just inside the "safe area" in the middle
        room.move(4, 4)
        self.assertFalse(room_has_exit_near_grid_edge(room, grid_size, margin))
        room.move(5, 5)
        self.assertFalse(room_has_exit_near_grid_edge(room, grid_size, margin))

        # One room outside of the "safe area"
        room.move(3, 5)
        self.assertTrue(room_has_exit_near_grid_edge(room, grid_size, margin))
        room.move(6, 5)
        self.assertTrue(room_has_exit_near_grid_edge(room, grid_size, margin))
        room.move(5, 3)
        self.assertTrue(room_has_exit_near_grid_edge(room, grid_size, margin))
        room.move(5, 6)
        self.assertTrue(room_has_exit_near_grid_edge(room, grid_size, margin))

    def test_room_added_blocks_already_existing_room_exits(self):
        # Create exit origin
        origin_exit = RoomExit(x=10, y=10, rotation=90)

        # Create room that should be added
        exits = []
        exits.append(RoomExit(x=2, y=1, rotation=0))
        exits.append(RoomExit(x=1, y=2, rotation=90))
        exits.append(RoomExit(x=0, y=1, rotation=180))
        exits.append(RoomExit(x=1, y=0, rotation=270))

        # A 3x3 room at 9,11, with an exit on all sides
        room_to_add = Room(name="test", type="test",
                           x=0, y=0,
                           width=3, height=3,
                           rotation=0,
                           exits=exits)
        room_to_add.move(9, 11)

        # Create room already existing in world, that blocks one exit from
        # the room we want to add
        world = []
        world.append(Room(name="test", type="test",
                          x=12, y=10,
                          width=3, height=3,
                          rotation=0,
                          exits=[]))

        # Create room that should be added
        self.assertTrue(room_blocks_exit_from_room_in_world(room_to_add,
                                                            world))


if __name__ == '__main__':
    unittest.main(exit=False)
