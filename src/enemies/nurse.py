""" a nurse type monster. Also is a NPC at one point."""
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



class Nurse(Enemy):
    """ Nurse. runs around trying to stab you

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'nurse')
        hitSoundFile = os.path.join("effects",  "critter6.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.health = 2
        self.speed = 4
        self.direction = random.randint(0, 2) % 2
        self.mode = 'walking'
        self.changedDirLastTick = 0

    # behavour
    def loop(self, g, r):
        canhitplayer = 0
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 16, self.rect.y - g.view.y + 32))
        belowpos = g.clayer[self.pos[1] ][self.pos[0]]

        if belowpos != 1:
            if self.changedDirLastTick:
                self.rect.y += 10
            else:
                self.direction = not self.direction
                self.changedDirLastTick = 1
        else:
            self.changedDirLastTick = 0
        # if you're walking
        if self.mode == 'walking':
            frme = 1 + (self.timer / 4) % 4
            self.image = g.images['nurse'][0].subsurface((frme * 32, 0, 32, 32))
            self.rect.x += self.speed
            if self.direction == 1:
                self.rect.x -= self.speed * 2
            self.btimer += 1
            if self.btimer < 10:
                self.direction = 0
                if self.rect.x > g.player.rect.x:
                    self.direction = 1
            if self.btimer > 150:
                self.btimer = 0
                self.mode = 'idle'
            dy = self.rect.x - g.player.rect.x
            dh = self.rect.y - g.player.rect.y
            if dy < 30 and dy > -30:
                if dh < 30 and dh > -30:
                    self.mode = 'attack'
                    self.timer = 0
        elif self.mode == 'idle':
            self.image = g.images['nurse'][0].subsurface((0, 0, 32, 32))
            self.btimer += 1
            if self.btimer > 40:
                self.btimer = 0
                self.mode = 'walking'
        elif self.mode == 'attack':
            frme = (self.timer / 4)
            self.image = g.images['nurse'][0].subsurface((frme * 32, 32, 32, 32))
            if frme > 3:
                canhitplayer = 1
            if frme >= 4:
                self.btimer = 0
                self.mode = 'walking'
        elif self.mode == 'death':
            self.destroy()
            
        self.loop_hit_death(g, r, 1, canhitplayer)


    # if you hit the roof, you float away from it. You also forget if you're targeting the player
    def rebound(self, h):
        self.direction = not self.direction
        self.mode = 'walking'