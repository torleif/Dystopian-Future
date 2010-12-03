""" a plant like monster with electrial shots """
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



class Monster5(Enemy):
    """ Plant. a plant like monster with electrial shots

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'monster5')
        hitSoundFile = os.path.join("effects",  "critter7.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.health = 8
        self.speed = 3
        self.direction = random.randint(0, 2) % 2
        self.mode = 'idle'
        self.jumpvel = 0.0
        self.jumpstart = 8.0

    # behavour
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        canbehit = 1
        canhitplayer = 1

        if self.mode == 'idle':
            self.image = g.images['monster5'][0].subsurface((0, 0, 32, 32))
            mdx,mdy = g.player.rect.x - self.rect.x, g.player.rect.y - self.rect.y
            # getting bored, going for a little walk
            self.btimer += 1
            if self.btimer > 100:
                self.mode = 'run'
                self.btimer = 0
                self.direction = random.randint(0,1)
            # getting close will cause it to jump
            if mdx < 50 and mdx > -50:
                if mdy < 50 and mdy > -50:
                    self.mode = 'jump'
                    self.jumpvel = self.jumpstart
        elif self.mode == 'ouch':
            self.image = g.images['monster5'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 1:
                self.btimer = 0
                self.mode = 'jump'
                self.jumpvel = self.jumpstart
                self.direction = self.rect.x < g.player.rect.x
        elif self.mode == 'run':
            d = self.btimer / 4
            self.image = g.images['monster5'][0].subsurface((d * 32, 0, 32, 32))
            belowpos = g.clayer[self.pos[1] + 1][self.pos[0]]
            if belowpos != 1:
                self.direction = not self.direction
            fnum = (self.timer / 2 % 3)
            self.image = g.images['monster5'][0].subsurface(((1+fnum) * 32, 0, 32, 32))
            self.btimer += 1
            self.rect.x += (self.direction * 2 - 1) * self.speed
            if self.btimer > 10:
                self.mode = 'idle'
                self.btimer = 0
        elif self.mode == 'jump':
            d = 1
            if self.jumpvel < -5:
                d = 3
            elif self.jumpvel < 10:
                d = 2

            self.image = g.images['monster5'][0].subsurface(((d) * 32, 32, 32, 32))
            self.rect.y -= self.jumpvel
            self.jumpvel -= .5
            self.rect.x += (self.direction * 2 - 1) * self.speed
        elif self.mode == 'death':
            self.image = g.images['monster5'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 10:
                self.destroy()
        self.loop_hit_death(g, r, canbehit, canhitplayer)

    # destroy self
    def destroy(self):
        Effect(self.g, 'explosion', (self.rect.x, self.rect.y))

        rint = random.randint(1, 3)
        if rint == 1:
            Inventory(self.g, 'shot7', (self.rect.x, self.rect.y))
        elif rint == 2:
            Inventory(self.g, 'health', (self.rect.x, self.rect.y))
        elif rint == 3:
            Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
            Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
            Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
        self.destryoed.play()
        self.g.sprites.remove(self)

    # walk away from the wall
    def rebound(self, h):
        self.direction = not self.direction
        if self.mode == 'jump':
            if self.jumpvel < 0:
                self.mode = 'idle'
            else:
                self.jumpvel = -10