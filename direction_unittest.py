import unittest
from direction import *


class TestDirection(unittest.TestCase):

    def test_direction_offset(self):
        x, y = direction_offset(0)
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)
        x, y = direction_offset(90)
        self.assertEqual(x, 0)
        self.assertEqual(y, -1)
        x, y = direction_offset(180)
        self.assertEqual(x, -1)
        self.assertEqual(y, 0)
        x, y = direction_offset(270)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)

    def test_direction_opposite(self):
        self.assertEqual(opposite_direction(0), 180)
        self.assertEqual(opposite_direction(90), 270)
        self.assertEqual(opposite_direction(180), 0)
        self.assertEqual(opposite_direction(270), 90)


if __name__ == '__main__':
    unittest.main()
