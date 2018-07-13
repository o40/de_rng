class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + height

    def __str__(self):
        return str(self.__dict__)

    def overlaps(self, rect):
        """
        Since this is used in a discrete system, 0-2 does not overlap with 2-3.
        """
        x_overlap = (self.x <= rect.x < self.x2 or
                     self.x < rect.x2 <= self.x2 or
                     rect.x <= self.x < rect.x2 or
                     rect.x < self.x2 <= rect.x2)

        y_overlap = (self.y <= rect.y < self.y2 or
                     self.y < rect.y2 <= self.y2 or
                     rect.y <= self.y < rect.y2 or
                     rect.y < self.y2 <= rect.y2)

        if x_overlap and y_overlap:
            return True
        return False

    def is_in_grid(self, grid_size, margin=0):
        x = self.x - margin
        y = self.y - margin
        x2 = self.x2 + margin
        y2 = self.y2 + margin
        return (x >= 0 and (x2 < grid_size) and
                y >= 0 and (y2 < grid_size))
