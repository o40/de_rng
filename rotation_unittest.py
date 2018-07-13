import unittest
from rotation import *


class TestRotation(unittest.TestCase):

    def test_rotation_offset(self):
        x, y = rotation_offset(0)
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)
        x, y = rotation_offset(90)
        self.assertEqual(x, 0)
        self.assertEqual(y, 1)
        x, y = rotation_offset(180)
        self.assertEqual(x, -1)
        self.assertEqual(y, 0)
        x, y = rotation_offset(270)
        self.assertEqual(x, 0)
        self.assertEqual(y, -1)

    def test_rotation_opposite(self):
        self.assertEqual(opposite_rotation(0), 180)
        self.assertEqual(opposite_rotation(90), 270)
        self.assertEqual(opposite_rotation(180), 0)
        self.assertEqual(opposite_rotation(270), 90)


if __name__ == '__main__':
    unittest.main(exit=False)
