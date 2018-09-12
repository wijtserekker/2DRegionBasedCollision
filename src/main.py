import os
import time
from threading import Thread

from entity import Entity
from mymath import Rect
from world import World
from worldview import WorldView

tick_length = 1 / 30
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
            else:
                print('Tick took ' + str((end_time - start_time) - tick_length) + ' too long!')


os.system('xset r off')
try:
    r = [Rect(100, 100, 400, 200), Rect(150, 150, 400, 200)]
    # r = []
    # import random
    # for i in range(0, 50):
    #     r.append(Rect(int(random.random() * world_width), int(random.random() * world_height), 20, 20))
    w = World(r, world_width, world_height)
    p = Entity(701, 200, 40, 40, 10, w)
    w.entities.append(p)
    v = WorldView(w, p)
    c = Clock(w, v)
    c.start()
    v.loop()
finally:
    os.system('xset r on')
