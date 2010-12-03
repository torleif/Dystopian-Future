""" a monster with tenticles. Also is a NPC at one point."""
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



class Monster0(Enemy):
    """ Nurse. runs around trying to stab you

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'monster0')
        hitSoundFile = os.path.join("effects",  "critter3.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.health = 6
        self.mode = 'idle'

    # behavour
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        if self.mode == 'ouch':
            self.image = g.images['monster0'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 5:
                self.btimer = 0
                self.mode = 'idle'
                self.direction = 0
                if self.rect.x < g.player.rect.x:
                    self.direction = 1
        elif self.mode == 'idle':
            belowpos = g.clayer[self.pos[1] + 1][self.pos[0]]
            belowpos2 = g.clayer[self.pos[1]][self.pos[0] + (self.direction * 2 - 1)]
            if belowpos != 1 or belowpos2 == 1:
                self.direction = not self.direction
            fnum = (self.timer / 3 % 3)
            self.image = g.images['monster0'][0].subsurface((fnum * 32, 0, 32, 32))
            self.rect.x -= 2
            if self.direction == 1:
                self.rect.x += 4
            dy = self.rect.x - g.player.rect.x
            dh = self.rect.y - g.player.rect.y
            if dy < 60 and dy > -60:
                if dh < 30 and dh > -30:
                    rint = random.randint(1, 15)
                    if rint == 1:
                        self.mode = 'shoot'
                        self.btimer = 0
        elif self.mode == 'death':
            self.image = g.images['monster0'][0].subsurface((3 * 32, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 5:
                self.destroy()
        elif self.mode == 'shoot':
            self.timer -= 1
            self.image = g.images['monster0'][0].subsurface((3 * 32, 0, 32, 32))
            if self.btimer == 0:
                s = Shot(g, not self.direction, (self.rect.x, self.rect.y + 16), 'shot4', 'enemy')
            self.btimer += 1
            if self.btimer > 10:
                self.mode = 'idle'
        self.loop_hit_death(g, r, 1, canhitplayer = 1)

    # destroy self
    def destroy(self):
        Effect(self.g, 'explosion', (self.rect.x, self.rect.y))

        rint = random.randint(1, 3)
        if rint == 1:
            Inventory(self.g, 'shot4', (self.rect.x, self.rect.y))
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
        self.mode = 'walking'