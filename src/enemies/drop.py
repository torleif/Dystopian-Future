""" water dropplet """
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



class Drop(Enemy):
    """ falls and dies. nothing special

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'drop')
        self.image = g.images['inventory'][0].subsurface((4 * 32, 8 * 32, 32, 32))
        self.rect.height = 8
        self.speed = 6

    # behavour
    def loop(self, g, r):
        self.rect.y += self.speed

    # walk away from the wall
    def rebound(self, h):
        self.g.sprites.remove(self)