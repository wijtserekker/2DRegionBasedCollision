from entity import Entity
from mymath import Rect


class World:

    def __init__(self, regions: [Rect], w: int, h: int):
        self.regions = regions
        self.entities = []
        self.w = w
        self.h = h

    def update(self):
        for entity in self.entities:
            entity.update()
