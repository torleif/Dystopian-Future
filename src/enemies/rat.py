""" a very simply monster. runs left and right."""
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



class Rat(Enemy):
    """ enemy 101

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'rat')
        hitSoundFile = os.path.join("effects",  "critter2.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.health = 6

    # behavour
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        
        if self.mode == 'idle':
            self.image = g.images['rat'][0].subsurface((0, 0, 32, 32))
        elif self.mode == 'ouch':
            self.image = g.images['rat'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 10:
                self.btimer = 0
                self.mode = 'run'
                self.direction = 0
                if self.rect.x < g.player.rect.x:
                    self.direction = 1
        elif self.mode == 'run':
            belowpos = g.clayer[self.pos[1] + 1][self.pos[0]]
            if belowpos != 1:
                self.direction = not self.direction
            fnum = 1 + (self.timer / 2 % 2 == 0)
            self.image = g.images['rat'][0].subsurface((fnum * 32, 0, 32, 32))
            self.rect.x -= 3
            self.btimer += 1
            if self.btimer > 50:
                self.mode = 'idle'
                self.btimer = 0
            if self.direction == 1:
                self.rect.x += 6
        elif self.mode == 'death':
            self.image = g.images['rat'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 10:
                self.destroy()
        self.loop_hit_death(g, r, 1, canhitplayer = 1)

    # destroy self
    def destroy(self):
        Effect(self.g, 'explosion', (self.rect.x, self.rect.y))

        
        rint = random.randint(1, 2)
        if rint == 1:
            Inventory(self.g, 'health', (self.rect.x, self.rect.y))
        elif rint == 2:
            Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
        self.destryoed.play()
        self.g.sprites.remove(self)


    # if you hit side, rebound
    def rebound(self, h):
        if self.mode == 'run':
            self.direction = not self.direction