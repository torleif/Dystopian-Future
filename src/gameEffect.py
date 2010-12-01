""" an effect generator. Contols things like wind """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
import random
import math


""" a leaf in the wind
"""
class Leaf(Sprite):
    # create a new leaf
    def __init__(self, g):
        self.image = g.images['inventory'][0].subsurface((4 * 32, 7 * 32, 32, 32))
        Sprite.__init__(self, self.image, Rect(0,0,32,32))
        self.orginalimage = self.image
        self.init_position(g)
        self.rect.x = random.randint(0, g.view.w) + g.view.x
        self.g = g
        self.groups = g.string2groups('shot')
        self.rotateamount = random.randint(-3, 3)
        self.rotatecounter = 0
        g.sprites.append(self)
        g.removeOnLeave.append(self)

    # init the leaf
    def init_position(self, g):
        self.rect.x = g.view.w + g.view.x
        self.rect.y = random.randint(0, g.view.h) + g.view.y
        self.vecx = -random.randint(10, 15)
        self.vecy = random.randint(-3, 3)

    # remove a sprite
    def rebound(self, v):
        self.init_position(self.g)

    # upon each loop
    def loop(self, g, r):
        self.rect.x += self.vecx
        self.rect.y += self.vecy
        if self.rect.x < self.g.view.x or self.rect.y < self.g.view.y:
            self.rebound(1)
        #if self.rotateamount != 0:
        self.image = pygame.transform.rotate(self.orginalimage, self.rotatecounter * 5)
        self.rotatecounter += self.rotateamount

""" a wad of dirt
"""
class Dirt(Leaf):
    # create a new leaf
    def __init__(self, g):
        Leaf.__init__(self, g)
        self.image = g.images['inventory'][0].subsurface((5 * 32, 7 * 32, 32, 32))
        self.orginalimage = self.image


""" contains all the particles, removes them upon delete
"""
class GameEffect():
    """ effects.

    """
    type = ''
    
    # remove all effects
    def __init__(self, g, type):
        self.type = type
        print 'New effect ', type

        if self.type == 'wind':
            # wind = 10 leaves 20 dots
            for i in range (10):
                s = Leaf(g)
            for i in range (20):
                s = Dirt(g)