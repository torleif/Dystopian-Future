""" bugs that chill on the ground till you distrub them """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import random
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
import math
from effect import Effect
from shot import Shot
from enemy import Enemy
from inventory import Inventory



class Bugs(Enemy):
    """ little bugs

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'bugs')
        self.frm1 = g.images['inventory'][0].subsurface((7 * 32, 7 * 32, 32, 32))
        self.frm2 = g.images['inventory'][0].subsurface((6 * 32, 7 * 32, 32, 32))
        self.rect.y += 2
        self.rect.x += random.randint(-4,4)
        self.flying = 0
        self.vecx = random.randint(-5,5)
        self.vecy = 0

    # behavour
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        

        if self.flying == 1:
            if (self.timer / 2) % 2 == 0:
                self.image = self.frm1
            else:
                self.image = self.frm2
            self.rect.x += math.sin(self.timer / 3) * 3 + self.vecx
            self.rect.y += self.vecy
            if self.timer > self.timerout:
                self.vecy += .5
        # start flying
        if self.pos == g.player.pos and self.flying == 0:
            self.flying = 1
            self.vecy = -1.0 -  random.randint(0,2)
            self.vecx = random.randint(-5,5)
            self.timer = 0
            self.timerout = 50 + random.randint(0,50)
        self.timer += 1

    # walk away from the wall
    def rebound(self, h):
        if h == 1:
            self.flying = 0
        elif h == 2:
            self.vecx = -5
        elif h == 3:
            self.vecx = 5