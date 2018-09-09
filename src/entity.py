import math
import time

from mymath import Rect, Line


class Entity(Rect):

    def __init__(self, x: int, y: int, w: int, h: int, max_speed: int, world: 'World'):
        super().__init__(x, y, w, h)
        self.max_speed = max_speed
        self.direction = 0
        self.speed = 0
        self.world = world

    def update(self):
        if self.speed > 0:
            dx = int(self.speed * math.sin(self.direction))
            dy = int(self.speed * math.cos(self.direction))

            # Define broad collision rect
            bx = self.x + dx if dx < 0 else self.x
            by = self.y + dy if dy < 0 else self.y
            bw = self.w + abs(dx)
            bh = self.h + abs(dy)
            br = Rect(bx, by, bw, bh)

            extra_check = dx != 0 and dy != 0

            if extra_check:
                if (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                    u_line = Line(self.x + self.w, self.y, self.x + self.w + dx, self.y + dy)
                    l_line = Line(self.x, self.y + self.h, self.x + dx, self.y + self.h + dy)
                else:
                    u_line = Line(self.x, self.y, self.x + dx, self.y + dy)
                    l_line = Line(self.x + self.w, self.y + self.h, self.x + self.w + dx, self.y + self.h + dy)

            # Check for collisions with this rect
            for region in self.world.regions:
                if br.collides(region):
                    if extra_check:
                        if (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                            x1, y1 = region.up_right_corn()
                            x2, y2 = region.down_left_corn()
                        else:
                            x1, y1 = region.up_left_corn()
                            x2, y2 = region.down_right_corn()
                        if not (u_line.is_above(x2, y2) and not l_line.is_above(x1, y1)):
                            continue
                    return

            self.x += dx
            self.y += dy
