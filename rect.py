class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + height

    def overlaps(self, rect):
        print("Check overlap_x", self.x, self.x2, rect.x, rect.x2)
        print("Check overlap_y", self.y, self.y2, rect.y, rect.y2)
        # TODO: Check ranges?
        x_overlap = (self.x < rect.x < self.x2 or
                     self.x < rect.x2 < self.x2 or
                     rect.x < self.x < rect.x2 or
                     rect.x < self.x2 < rect.x2)

        y_overlap = (self.y < rect.y < self.y2 or
                     self.y < rect.y2 < self.y2 or
                     rect.y < self.y < rect.y2 or
                     rect.y < self.y2 < rect.y2)

        if x_overlap and y_overlap:
            print("OVERLAPPING")
            return True
        print("NOT OVERLAPPING")
        return False
