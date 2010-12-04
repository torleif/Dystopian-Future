""" a ghost type floating monster"""
import pygame
from pygame.locals import *
import random
import os
import sys; sys.path.insert(0, "..")
from shot import Shot, Laser0
from enemy import Enemy

from effect import Effect


class Ghost(Enemy):
    """ Ghost. floats around, and chances you if you shoot it

    """

    def __init__(self, g, pos):
        print 'new monster 6'
        Enemy.__init__(self, g, pos, 'ghost')
        self.rect.width,self.rect.height = 64, 64
        self.shape.w,self.shape.h = 64, 64
        self.image = pygame.Surface((64,64), SRCALPHA)
        self.startpos = self.rect.x,self.rect.y
        self.targeting = 0
        self.float_target = (0,0)
        self.gravity = 0.0
        self.bump = 0
        self.rect_double_y = float(self.rect.y)
        hitSoundFile = os.path.join("effects",  "critter8.wav")
        self.health = 40
        self.birdhit = pygame.mixer.Sound(hitSoundFile)

    # ghost behavour
    def loop(self, g, r):
        if self.mode == 'death':
            self.btimer += 1
            if self.btimer < 3:
                self.image = g.images['monster6'][0].subsurface((3 * 64, 1 * 64, 64, 64))
            else:
                Effect(self.g, 'explosion', (self.rect.x + 32, self.rect.y + 32))
                self.destryoed.play()
                self.g.sprites.remove(self)
            return



        if self.targeting:
            self.float_target = (g.player.rect.x,g.player.rect.y)
        if self.timer % 150 == 0:
            self.float_target = (self.startpos[0] + random.randint(-200, 200),
                    self.startpos[1] + random.randint(-200, 200))

        timerstart = 25 # time between bumps
        if self.float_target[1] < self.rect.y:
            timerstart = 10 # bumping up, less wait time
        if self.timer % (timerstart) == 0:
            self.bump = 1
        dx = self.rect.x - self.float_target[0]
        self.direction = dx > 0
        
        if self.mode != 'shooting':
            self.rect_double_y += self.gravity
            self.rect.y = int(self.rect_double_y)
            if dx > 5: # float left
                self.rect.x -= 3
            if dx < -5: # float right
                self.rect.x += 3

        self.gravity += 0.7
        if self.gravity > 2.0:
            self.gravity = 2.0

        dy = self.rect.y - g.player.rect.y
        if dy > -5 and dy < 5:
            if self.mode == 'idle' or self.mode == 'ouch':
                if self.direction == 0 and self.rect.x < g.player.rect.x or \
                    self.direction == 1 and self.rect.x > g.player.rect.x:
                    self.mode = 'shooting'
                    self.btimer = 0

        if self.mode == 'idle':
            if self.bump != 0:
                self.bump += 1
                if self.bump == 2:
                    self.gravity = -3.0
                if self.bump > 3:
                    self.image = g.images['monster6'][0].subsurface((1 * 64, 0 * 64, 64, 64))
                else:
                    self.image = g.images['monster6'][0].subsurface((2 * 64, 0 * 64, 64, 64))
                if self.bump > 6:
                    self.bump = 0
            else:
                # normal
                self.image = g.images['monster6'][0].subsurface((0 * 64, 0 * 64, 64, 64))
        elif self.mode == 'ouch':
            self.targeting = 1
            self.timer = 0
            self.image = g.images['monster6'][0].subsurface((3 * 64, 0 * 64, 64, 64))
            self.btimer += 1
            if self.btimer > 4:
                self.btimer = 0
                self.mode = 'idle'
        elif self.mode == 'shooting':
            self.btimer += 1
            frameno = (self.btimer / 3)
            if self.btimer == 3:
                offset = 15
                if not self.direction:
                    offset = 70
                s = Laser0(g, self.direction, (self.rect.x + offset, self.rect.y + 45), 'enemy')
            if frameno < 3:
                self.image = g.images['monster6'][0].subsurface((frameno * 64, 1 * 64, 64, 64))
            else:
                self.mode = 'idle'
                self.image = g.images['monster6'][0].subsurface((0 * 64, 0 * 64, 64, 64))
        else:
            self.image = g.images['monster6'][0].subsurface((3 * 64, 0 * 64, 64, 64))

        self.loop_hit_death(g, r, canbehit = 1, canhitplayer = 1)


    # if you hit the roof, you float away from it. You also forget if you're targeting the player
    def rebound(self, h):
        self.targeting = 0
        if h == 4:
            self.gravity = 3.0
        if h == 1:
            self.gravity = -3.0