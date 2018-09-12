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
            self.move(int(self.speed * math.sin(self.direction)), int(self.speed * math.cos(self.direction)))

    def move(self, dx, dy):
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
        colliding_regions = []
        for region in self.world.regions:
            if self.collides(region):
                return
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
                colliding_regions.append(region)

        if len(colliding_regions) > 0:
            print('===================================================')
            print('Colliding REGIONS: ' + str(colliding_regions))
            print('DX='+str(dx), 'DY='+str(dy))
            print('STARTPOS: ' + str(self))
            dxa = dx
            dya = dy
            if dx == 0 and dy < 0:    # UP =========================================================

                for region in colliding_regions:
                    region: 'Rect'
                    if self.y + dya < region.y + region.h:
                        dya += (region.y + region.h) - (self.y + dya)
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.y += dya
                print('ENDPOS:   ' + str(self))

            elif dx > 0 and dy < 0:   # UP RIGHT ===================================================

                dxdy_scale = -1 * dx / dy
                last_direction_was_down = False
                for region in colliding_regions:
                    if self.x + self.w + dxa > region.x and self.y + dya < region.y + region.h:
                        # Correction needed in downward direction
                        yt1 = (region.y + region.h) - (self.y + dya)
                        xt1 = (dxdy_scale * yt1)
                        # Correction needed in leftward direction
                        xt2 = (self.x + self.w + dxa) - region.x
                        yt2 = (xt2 / dxdy_scale)
                        if xt1 < xt2:
                            dxa -= xt1
                            dya += yt1
                            last_direction_was_down = True
                        else:
                            dxa -= xt2
                            dya += yt2
                            last_direction_was_down = False
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.x += dxa
                self.y += dya
                print('ENDPOS:   ' + str(self))
                if last_direction_was_down:
                    self.move(dx - dxa, 0)
                else:
                    self.move(0, dy - dya)

            elif dx > 0 and dy == 0:  # RIGHT ======================================================

                for region in colliding_regions:
                    region: 'Rect'
                    if self.x + self.w + dxa > region.x:
                        dxa += region.x - (self.x + self.w + dxa)
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.x += dxa
                print('ENDPOS:   ' + str(self))

            elif dx > 0 and dy > 0:   # DOWN RIGHT =================================================

                dxdy_scale = dx / dy
                last_direction_was_up = False
                for region in colliding_regions:
                    if self.x + self.w + dxa > region.x and self.y + self.h + dya > region.y:
                        # Correction needed in upward direction
                        yt1 = self.y + self.h + dya - region.y
                        xt1 = (dxdy_scale * yt1)
                        # Correction needed in leftward direction
                        xt2 = self.x + self.w + dxa - region.x
                        yt2 = (xt2 / dxdy_scale)
                        if xt1 < xt2:
                            dxa -= xt1
                            dya -= yt1
                            last_direction_was_up = True
                        else:
                            dxa -= xt2
                            dya -= yt2
                            last_direction_was_up = False
                self.x += dxa
                self.y += dya
                print('ENDPOS:   ' + str(self))
                if last_direction_was_up:
                    self.move(dx - dxa, 0)
                else:
                    self.move(0, dy - dya)

            elif dx == 0 and dy > 0:  # DOWN =======================================================

                for region in colliding_regions:
                    region: 'Rect'
                    if self.y + self.h + dya > region.y:
                        dya += region.y - (self.y + self.h + dya)
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.y += dya
                print('ENDPOS:   ' + str(self))

            elif dx < 0 and dy > 0:   # DOWN LEFT ==================================================

                dxdy_scale = -1 * dx / dy
                last_direction_was_up = False
                for region in colliding_regions:
                    if self.x + dxa < region.x + region.w and self.y + self.h + dya > region.y:
                        # Correction needed in upward direction
                        yt1 = (self.y + self.h + dya) - region.y
                        xt1 = (dxdy_scale * yt1)
                        # Correction needed in rightward direction
                        xt2 = (region.x + region.w) - (self.x + dxa)
                        yt2 = (xt2 / dxdy_scale)
                        if xt1 < xt2:
                            dxa += xt1
                            dya -= yt1
                            last_direction_was_up = True
                        else:
                            dxa += xt2
                            dya -= yt2
                            last_direction_was_up = False
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.x += dxa
                self.y += dya
                print('ENDPOS:   ' + str(self))
                if last_direction_was_up:
                    self.move(dx - dxa, 0)
                else:
                    self.move(0, dy - dya)

            elif dx < 0 and dy == 0:  # LEFT =======================================================

                for region in colliding_regions:
                    region: 'Rect'
                    if self.x + dxa < region.x + region.w:
                        dxa += (region.x + region.w) - (self.x + dxa)
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.x += dxa
                print('ENDPOS:   ' + str(self))

            elif dx < 0 and dy < 0:   # UP LEFT ====================================================

                dxdy_scale = dx / dy
                last_direction_was_down = False
                for region in colliding_regions:
                    if self.x + dxa < region.x + region.w and self.y + dya < region.y + region.h:
                        # Correction needed in downward direction
                        yt1 = (region.y + region.h) - (self.y + dya)
                        xt1 = (dxdy_scale * yt1)
                        # Correction needed in rightward direction
                        xt2 = (region.x + region.w) - (self.x + dxa)
                        yt2 = (xt2 / dxdy_scale)
                        if xt1 < xt2:
                            dxa += xt1
                            dya += yt1
                            last_direction_was_down = True
                        else:
                            dxa += xt2
                            dya += yt2
                            last_direction_was_down = False
                        print('ALTERED DX='+str(dxa), 'DY='+str(dya))
                self.x += dxa
                self.y += dya
                print('ENDPOS:   ' + str(self))
                if last_direction_was_down:
                    self.move(dx - dxa, 0)
                else:
                    self.move(0, dy - dya)

        else:
            self.x += dx
            self.y += dy























