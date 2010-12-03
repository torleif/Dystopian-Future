""" a very simply monster. flys up and down."""
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



class Bird(Enemy):
    """ enemy 101

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'bird')
        hitSoundFile = os.path.join("effects",  "critter.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.rect.y += 8 # offset

    # behavour
    def loop(self, g, r):
        self.image = g.images['bird'][0].subsurface(((self.timer / 3 % 2) * 32, 0, 32, 32))
        if self.mode == 'ouch':
            self.image = g.images['bird'][0].subsurface((2 * 32, 0, 32, 32))
            self.timer -= 1
            self.btimer += 1
            if self.btimer % 2 == 0:
                self.image = g.make_image_white(self.image)
            if self.btimer > 5:
                self.btimer = 0
                self.mode = 'idle'
        if self.mode == 'death':
            self.image = g.images['bird'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            self.rect.x += (1-self.direction*2) * 2
            self.rect.y += math.sqrt(self.btimer) * 2 - 5
            canbehit = 0
        if self.mode == 'shoot':
            self.timer -= 1
            self.image = g.images['bird'][0].subsurface((2 * 32, 0, 32, 32))
            if self.btimer == 0:
                s = Shot(g, not self.direction, (self.rect.x, self.rect.y + 10), 'shot2', 'enemy')
            self.btimer += 1
            if self.btimer > 10:
                self.mode = 'idle'
        if self.mode == 'idle':
            self.direction = 0
            if self.rect.x < g.player.rect.x:
                self.direction = 1
            self.rect.y = self.startrect.y + math.sin(float(self.timer) / 30) * 40
            dy = self.rect.x - g.player.rect.x
            dh = self.rect.y - g.player.rect.y
            if dy < 50 and dy > -50:
                if dh < 60 and dh > -60:
                    rint = random.randint(1, 10)
                    if rint == 1:
                        self.mode = 'shoot'
                        self.btimer = 0
        self.loop_hit_death(g, r, 1, canhitplayer = 1)

    # destroy self
    def destroy(self):
        Effect(self.g, 'explosion', (self.rect.x, self.rect.y))

        rint = random.randint(1, 4)
        if rint == 1:
            Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
            Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
        elif rint == 2:
            Inventory(self.g, 'shot2', (self.rect.x, self.rect.y))
        elif rint == 3:
            Inventory(self.g, 'shot2', (self.rect.x, self.rect.y))
        elif rint == 4:
            Inventory(self.g, 'health', (self.rect.x, self.rect.y))
        self.destryoed.play()
        self.g.sprites.remove(self)


    # boom!
    def rebound(self, h):
        self.destroy()