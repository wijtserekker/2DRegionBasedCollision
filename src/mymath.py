

class Rect:

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def collides(self, other):
        return (self.x + self.w > other.x and
                other.x + other.w > self.x and
                self.y + self.h > other.y and
                other.y + other.h > self.y)

    def up_left_corn(self):
        return self.x, self.y

    def up_right_corn(self):
        return self.x + self.w, self.y

    def down_left_corn(self):
        return self.x, self.y + self.h

    def down_right_corn(self):
        return self.x + self.w, self.y + self.h

    def __str__(self):
        return 'Rect(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.w) + ', ' + str(self.h) + ')'

    def __repr__(self):
        return 'Rect(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.w) + ', ' + str(self.h) + ')'


class Line:

    def __init__(self, x1, y1, x2, y2):
        if x1 < x2:
            self.slope = (y2 - y1) / (x2 - x1)
        else:
            self.slope = (y1 - y2) / (x1 - x2)
        self.start = y1 - self.slope * x1

    def is_above(self, x, y):
        return (self.slope * x + self.start) < y
