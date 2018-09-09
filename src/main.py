import os
import time
from threading import Thread

from entity import Entity
from mymath import Rect
from world import World
from worldview import WorldView

tick_length = 1 / 20
world_width = 1000
world_height = 700


class Clock(Thread):

    def __init__(self, world: World, view: WorldView):
        super().__init__(daemon=True)
        self.world = world
        self.view = view
        self.running = True

    def run(self):
        while self.running:
            start_time = time.time()
            self.world.update()
            self.view.update()
            end_time = time.time()

            if tick_length > (end_time - start_time):
                time.sleep(tick_length - (end_time - start_time))


os.system('xset r off')
try:
    r = [Rect(20, 20, 400, 200)]
    w = World(r, world_width, world_height)
    p = Entity(500, 200, 40, 40, 100, w)
    w.entities.append(p)
    v = WorldView(w, p)
    c = Clock(w, v)
    c.start()
    v.loop()
finally:
    os.system('xset r on')
