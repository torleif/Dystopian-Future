""" Boss battle """
import pygame
from pygame.locals import *
import random
import os
import sys; sys.path.insert(0, "..")

from shot import Laser0
from enemy import Enemy
from inventory import Inventory
from effect import Effect


class FoxZombie(Enemy):
    """ Boss bro. Come at me
    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'fox_zombie')
        self.rect.width,self.rect.height = 64, 64
        self.shape.w,self.shape.h = 64, 64
        self.image = pygame.Surface((64,64), SRCALPHA)
        self.health = 40
        self.birdhit = pygame.mixer.Sound(os.path.join("effects",  "critter8.wav"))
        self.death = pygame.mixer.Sound(os.path.join("effects",  "cry1.wav"))

    # ghost behavour
    def loop(self, g, r):
        self.image = g.images['zombie'][0].subsurface(((self.timer / 3 % 2) * 32, 0, 64, 64))

        self.loop_hit_death(g, r, canbehit = 1, canhitplayer = 1)


    # if you hit the roof, you float away from it. You also forget if you're targeting the player
    def rebound(self, h):
        self.targeting = 0
        if h == 4:
            self.gravity = 3.0
        if h == 1:
            self.gravity = -3.0

   # drop some gimp prizes
    def destroy(self):
        
        self.death.play()
        self.g.sprites.remove(self)