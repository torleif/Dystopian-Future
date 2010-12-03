""" a slime monster """
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



class Monster2(Enemy):
    """ Slime. runs around trying to slob you

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'monster2')
        hitSoundFile = os.path.join("effects",  "critter4.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.health = 3
        self.rect.height = 16
        self.changedDirLastTick = 0

    # behavour
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        canbehit = 0
        canhitplayer = 1
        
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 16, self.rect.y - g.view.y + 32))
        canbehit = 0
        frme = (self.timer / 4) % 7
        self.image = g.images['monster2'][0].subsurface((frme * 32, 0, 32, 16))
        belowpos = g.clayer[self.pos[1] ][self.pos[0]]

        if belowpos != 1:
            if self.changedDirLastTick:
                self.rect.y += 10
            else:
                self.direction = not self.direction
                self.changedDirLastTick = 1
        else:
            self.changedDirLastTick = 0

        self.rect.x -= 1
        if self.direction == 1:
            self.rect.x += 2
        self.btimer += 1
        if self.btimer > 200:
            self.destroy()
        self.loop_hit_death(g, r, canbehit, canhitplayer)


    # walk away from the wall
    def rebound(self, h):
        self.direction = not self.direction