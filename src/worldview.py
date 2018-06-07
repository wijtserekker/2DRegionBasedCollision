import math
import os
from tkinter import *

from entity import Entity
from world import World


class WorldView:

    def __init__(self, world: World, player: Entity):

        self.world = world
        self.player = player
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.root = Tk()
        self.canvas = Canvas(self.root, width=world.w, height=world.h)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)

        self.canvas.pack()
        self.root.update()

    def draw(self):
        self.canvas.delete('all')

        for entity in self.world.entities:
            self.canvas.create_rectangle(entity.x, entity.y, entity.x + entity.w, entity.y + entity.h
                                         , fill='black', width=0)

    def update(self):
        self.root.after_idle(self.draw)

    def loop(self):
        self.root.mainloop()

    def on_key_press(self, event):
        if event.keycode == 111:
            self.up = True
            self.player_input_update()
        elif event.keycode == 114:
            self.right = True
            self.player_input_update()
        elif event.keycode == 116:
            self.down = True
            self.player_input_update()
        elif event.keycode == 113:
            self.left = True
            self.player_input_update()

    def on_key_release(self, event):
        if event.keycode == 111:
            self.up = False
            self.player_input_update()
        elif event.keycode == 114:
            self.right = False
            self.player_input_update()
        elif event.keycode == 116:
            self.down = False
            self.player_input_update()
        elif event.keycode == 113:
            self.left = False
            self.player_input_update()

    def player_input_update(self):
        dx = 1 if self.right else 0
        dx = -1 if self.left else dx
        dy = 1 if self.down else 0
        dy = -1 if self.up else dy

        if (dx, dy) == (0, 0):
            self.player.speed = 0
        else:
            self.player.speed = self.player.max_speed
            self.player.direction = math.atan2(dx, dy)
