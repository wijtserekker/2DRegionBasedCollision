from entity import Entity
from rect import Rect


class World:

    def __init__(self, regions: [Rect], player: Entity, w: int, h: int):
        self.regions = regions
        self.entities = [player]
        self.w = w
        self.h = h

    def update(self):
        for entity in self.entities:
            entity.update()
