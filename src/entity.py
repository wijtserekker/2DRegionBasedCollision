import math

from rect import Rect


class Entity(Rect):

    def __init__(self, x: int, y: int, w: int, h: int, max_speed: int):
        super().__init__(x, y, w, h)
        self.max_speed = max_speed
        self.direction = 0
        self.speed = 0

    def update(self):
        if self.speed > 0:
            self.x += self.speed * math.sin(self.direction)
            self.y += self.speed * math.cos(self.direction)
            # TODO Collision stuffs

