import unittest
from room import *
from direction import *

# TODO: Change direction to be degrees instead of "enum"

class TestRoom(unittest.TestCase):

    def test_room_rotation(self):
        a = Room("test", 10, 10, )
       
if __name__ == '__main__':
    unittest.main()
