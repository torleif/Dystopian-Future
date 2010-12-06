""" Boom! """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
import random
import math


class Effect(Sprite):
    """ effects.

    """
    timer = 0
    direction = 0
    keep_alive = 6
    

    def __init__(self, g, name, pos, mymsg = ''):
        # texture for the avatar
        self.image = g.images['inventory'][0].subsurface((0, 0, 0, 0))
        Sprite.__init__(self, self.image, Rect(0,0,32,32))
        self.groups = g.string2groups('shot')
        self.g = g
        self.rect.x,self.rect.y = pos[0],pos[1]
        self._rect.x,self._rect.y = self.rect.x,self.rect.y
        self.name = name
        if name == 'explosion':
            self.keep_alive = 4
        elif name == 'shot':

            g.exp4.play()
        elif name == 'health':
            self.healthchange = 0
            self.keep_alive = 30
            self.rect.x += 5
            self.rect.y -= 15
        elif name == 'msg':
            self.keep_alive = 20
            self.image = self.g.font.render(mymsg,1,(0,255,0))
            self.rect.x += self.image.get_rect().x / 2
            self.rect.y -= 15
        elif name == 'snow':
            self.keep_alive = 15
            self.image = g.images['inventory'][0].subsurface((1 * 32, 4 * 32, 32, 32))
            self.mvrectx = random.randint(-2, 2)
            self.mvrecty = random.randint(0, 2)
        elif name == 'water':
            self.keep_alive = 15
            self.image = g.images['inventory'][0].subsurface((4 * 32, 4 * 32, 32, 32))
            self.mvrectx = float(random.randint(-4, 4)) / 4
            self.mvrecty = float(random.randint(5, 6)) / 3
            self.floatx = float(self.rect.x)
            self.floaty = float(self.rect.y)
        elif name == 'bubble':
            self.image = g.images['inventory'][0].subsurface((6 * 32, 4 * 32, 32, 32))
            self.keep_alive = 60
            self.startx = pos[0]
            self.timer = random.randint(0, 30)
        elif name == 'lift':
            self.image = g.images['inventory'][0].subsurface((2 * 32, 5 * 32, 32, 32))
        elif name == 'leaf'  or self.name == 'dirt':
            self.image = g.images['inventory'][0].subsurface((5 * 32, 8 * 32, 32, 32))
            self.orginalimage = self.image
            self.rotationAmount = float(random.randint(-5, 5))
            self.vecx = float(random.randint(-2, 2))
            self.vecy = float(random.randint(-6, 2))
            self.keep_alive = 25
            if self.name == 'dirt':
                self.image = g.images['inventory'][0].subsurface((5 * 32, 7 * 32, 32, 32))
                self.orginalimage = self.image
        elif name == 'foxentrance':
            Effect(g, 'leaf', pos)
            Effect(g, 'leaf', pos)
            Effect(g, 'leaf', pos)
            Effect(g, 'leaf', pos)
            Effect(g, 'dirt', pos)
            Effect(g, 'dirt', pos)
            Effect(g, 'dirt', pos)
            Effect(g, 'dirt', pos)
            self.keep_alive = 0
        if name == 'explosion0':
            self.keep_alive = 7
            self.image = g.images['inventory'][0].subsurface((0 * 32, 11 * 32, 32, 32))
            g.exp3.play()
        if name == 'explosion1':
            self.keep_alive = 4
            self.image = g.images['inventory'][0].subsurface((4 * 32, 11 * 32, 32, 32))
            g.exp5.play()

        g.sprites.append(self)
    
    # upon each loop
    def loop(self, g, r):
        if self.name == 'shot':
            self.image = g.images['inventory'][0].subsurface(((1 + self.timer / 2) * 32, 32, 32, 32))
        elif self.name == 'explosion':
            self.image = g.images['inventory'][0].subsurface(((5 + self.timer / 2) * 32, 32, 32, 32))
        elif self.name == 'health':
            if self.healthchange > 0:
                mstr = '+'+str(self.healthchange)
                self.image = self.g.font.render(mstr,1,(0,0,0))
                self.image.blit(self.g.font.render(mstr,1,(255,0,0)), (-1,-1))
            else:
                mstr = str(self.healthchange)
                self.image = self.g.font.render(mstr,1,(0,0,0))
                self.image.blit(self.g.font.render(mstr,1,(0,0,255)), (-1,-1))

            self.rect.y -= 1
        elif self.name == 'msg':
            self.rect.y -= 1
        elif self.name == 'snow':
            self.rect.x -= self.mvrectx
            self.rect.y -= self.mvrecty
        elif self.name == 'water':
            self.floatx -= self.mvrectx
            self.floaty -= self.mvrecty
            self.mvrecty -= .3
            # float to int
            self.rect.x = int(self.floatx)
            self.rect.y = int(self.floaty)
        elif self.name == 'bubble':
            self.rect.x = self.startx + math.sin(float(self.timer) / 20.0) * 20.0
            self.rect.y -= .3
        elif self.name == 'lift':
            self.rect.y -= 3
            return
        elif self.name == 'leaf' or self.name == 'dirt':
            self.image = pygame.transform.rotate(self.orginalimage, self.rotationAmount * self.timer)
            self.rect.x += self.vecx
            self.rect.y += self.vecy
            self.vecy += .5
        elif self.name == 'explosion0':
            self.image = g.images['inventory'][0].subsurface(((self.timer / 2) * 32, 11 * 32, 32, 32))
        elif self.name == 'explosion1':
            self.image = g.images['inventory'][0].subsurface(((4 + (self.timer / 2)) * 32, 11 * 32, 32, 32))



        # die after a while
        if self.timer > self.keep_alive:
            g.sprites.remove(self)

        self.timer += 1
