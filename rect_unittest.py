import unittest
from rect import *


class TestRect(unittest.TestCase):

    def test_rect_overlaps_with_itself(self):
        a = Rect(10, 10, 2, 2)
        self.assertTrue(a.overlaps(a))

    def test_rect_overlaps_by_one_in_both_directions(self):
        a = Rect(10, 10, 2, 2)
        b = Rect(11, 11, 2, 2)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_rect_does_not_overlaps_when_adjacent(self):
        a = Rect(10, 10, 2, 2)
        b = Rect(10, 12, 2, 2)
        c = Rect(12, 10, 2, 2)
        d = Rect(8, 10, 2, 2)
        e = Rect(10, 8, 2, 2)
        self.assertFalse(a.overlaps(b))
        self.assertFalse(a.overlaps(c))
        self.assertFalse(a.overlaps(d))
        self.assertFalse(a.overlaps(e))

    def test_rect_overlaps_when_one_rect_contains_the_other(self):
        a = Rect(10, 10, 2, 2)
        b = Rect(9, 9, 4, 4)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_rect_overlap_when_three_sides_are_overlapping(self):
        a = Rect(x=10, y=10, width=2, height=4)
        b = Rect(x=10, y=12, width=2, height=2)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_rect_inside_of_margin_in_the_corners(self):
        grid_size = 10  # (0..9)
        margin = 2
        a = Rect(x=2, y=2, width=2, height=2)
        b = Rect(x=5, y=2, width=2, height=2)
        c = Rect(x=2, y=5, width=2, height=2)
        d = Rect(x=5, y=5, width=2, height=2)
        self.assertTrue(a.is_in_grid(grid_size, margin))
        self.assertTrue(b.is_in_grid(grid_size, margin))
        self.assertTrue(c.is_in_grid(grid_size, margin))
        self.assertTrue(d.is_in_grid(grid_size, margin))

    def test_rect_not_inside_of_margin(self):
        grid_size = 10  # (0..9)
        margin = 2
        a = Rect(x=1, y=4, width=2, height=2)
        b = Rect(x=6, y=4, width=2, height=2)
        c = Rect(x=4, y=1, width=2, height=2)
        d = Rect(x=4, y=1, width=2, height=2)
        self.assertFalse(a.is_in_grid(grid_size, margin))
        self.assertFalse(b.is_in_grid(grid_size, margin))
        self.assertFalse(c.is_in_grid(grid_size, margin))
        self.assertFalse(d.is_in_grid(grid_size, margin))


if __name__ == '__main__':
    unittest.main(exit=False)
