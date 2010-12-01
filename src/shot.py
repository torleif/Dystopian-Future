
""" LETS FUCKING SHOOT SOME SHIT """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
from effect import Effect
import random


class Shot(Sprite):
    """ We'll shoot some things

    """
    timer = 0
    direction = 0
    speed = 8
    keep_alive = 15
    damage = 1
    reload = 20
    invisible_timer = 0
    level = 0

    def __init__(self, g, direction, pos, type, owner = 'player'):
        # texture for the avatar
        self.orginalimg = g.images['inventory'][0].subsurface((7 * 32, 0, 32, 32))
        self.image = g.images['inventory'][0].subsurface((0, 0, 0, 0))
        Sprite.__init__(self, self.image, Rect(0,0,8,16))
        g.sprites.append(self)
        g.removeOnLeave.append(self)
        g.bullets.append(self)
        self.groups = g.string2groups('player')
        self.g = g
        self.direction = direction
        self.rect.x,self.rect.y = pos[0],pos[1]  # meh hack
        self._rect.x,self._rect.y = self.rect.x,self.rect.y  # bullshit hacks.
        self.type = type
        self.rect.width = 8
        self.rect.height = 8
        self.owner = owner

        if owner == 'player':
            mkstr = type+'_lvl'
            if mkstr in g.saveData:
                if g.saveData[mkstr] > 10:
                    self.level = 1
                if g.saveData[mkstr] > 20:
                    self.level = 2
                
        if type == 'shot1':
            g.shootSound1.play()
        elif type == 'shot2': # green bird bullet
            g.shootSound2.play()
            self.orginalimg = g.images['inventory'][0].subsurface((3 * 32, 2*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 12
            self.keep_alive = 12
            self.damage = 2 + self.level
            self.reload = 15
        elif type == 'shot3': # fox spray bullet
            g.shootSound3.play()
            self.orginalimg = g.images['inventory'][0].subsurface((5 * 32, 2*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 13
            self.keep_alive = 10
            self.damage = 1
            self.reload = 10
            self.yvel = random.randint(-2, 2)
        elif type == 'shot4': # monster shot
            g.shootSound4.play()
            self.orginalimg = g.images['inventory'][0].subsurface((5 * 32, 3*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 8 + self.level * 2
            self.keep_alive = 13
            self.damage = 2 + self.level
            self.reload = 7
            self.rect.height = 10
            self.yvel = random.randint(-1, 0)
        elif type == 'shot5': # mushroom monster shot (spawns green slime, or explodes)
            self.orginalimg = g.images['inventory'][0].subsurface((1 * 32, 7*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 0
            self.keep_alive = 200
            self.damage = 2
            self.rect.height = 10
            self.yvel = float(random.randint(-6, 0))
            self.xvel = float(random.randint(-4, 4))
            self.rebound = self.rebound_spawner
        elif type == 'shot6': # doctor spawns nurses
            self.orginalimg = g.images['inventory'][0].subsurface((6 * 32, 6*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 0
            self.keep_alive = 200
            self.damage = 2
            self.rect.height = 10
            self.yvel = float(random.randint(-6, 0))
            self.xvel = float(random.randint(-5, 5))
            self.rebound = self.rebound_spawner
        elif type == 'shot7': # an eletrical shot
            self.orginalimg = g.images['inventory'][0].subsurface((1 * 32, 7*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 12
            self.keep_alive = 18
            self.damage = 5 + self.level
            self.reload = 12 - self.level
            g.shootSound5.play()
        elif type == 'shot8': # an eletrical shot
            self.orginalimg = g.images['inventory'][0].subsurface((7 * 32, 9*32, 32, 32))
            #self.image = self.orginalimg
            self.speed = 13
            self.keep_alive = 100
            self.damage = 5 + self.level
            self.reload = 12 - self.level
            g.shootSound5.play()
        self.renderoffset = (-16, -20)

    # upon each loop
    def loop(self, g, r):
        if self.direction != 2 and self.direction != 3:
            self.rect.x -= self.speed * (self.direction * 2 - 1)
        elif self.direction == 2:
            self.rect.y -= self.speed
        elif self.direction == 3:
            self.rect.y += self.speed

        if self.type == 'shot1':
            if self.direction != 2 and self.direction != 3:
                if self.timer / 3 % 2 == 0:
                    self.orginalimg = g.images['inventory'][0].subsurface((0, 32, 32, 32))
                else:
                    self.orginalimg = g.images['inventory'][0].subsurface((7 * 32, 0, 32, 32))
            elif self.direction == 2:
                if self.timer / 3 % 2 == 0:
                    self.orginalimg = g.images['inventory'][0].subsurface((6 * 32, 8 * 32, 32, 32))
                else:
                    self.orginalimg = g.images['inventory'][0].subsurface((7 * 32, 8 * 32, 32, 32))
            elif self.direction == 3:
                if self.timer / 3 % 2 == 0:
                    self.orginalimg = g.images['inventory'][0].subsurface((0, 9 * 32, 32, 32))
                else:
                    self.orginalimg = g.images['inventory'][0].subsurface((1 * 32, 9 * 32, 32, 32))
        elif self.type == 'shot2':
            if self.level == 0:
                self.orginalimg = g.images['inventory'][0].subsurface((6 * 32, 5*32, 32, 32))
            elif self.level == 1:
                t = 4 + (self.timer / 2 % 2 == 0)
                self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 5*32, 32, 32))
            elif self.level == 2:
                t = 3 + (self.timer / 2 % 2 == 0)
                self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 2*32, 32, 32))
        elif self.type == 'shot3':
            t = 5 + (self.timer / 2 % 3 == 0)
            self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 2*32, 32, 32))
            self.rect.y += self.yvel
        elif self.type == 'shot4':
            if self.level == 0:
                t = 3 + (self.timer / 2 % 2 == 0)
                self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 6*32, 32, 32))
            elif self.level == 1:
                t = (self.timer / 2 % 2 == 0)
                self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 6*32, 32, 32))
            elif self.level == 2:
                t = 5 + (self.timer / 2 % 3 == 0)
                self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 3*32, 32, 32))
            if  self.direction != 2 and self.direction != 3:
                self.rect.y += self.yvel
            else:
                self.rect.x += self.yvel
        elif self.type == 'shot5':
            self.orginalimg = g.images['inventory'][0].subsurface((5 * 32, 4*32, 32, 32))
            self.rect.y += self.yvel
            self.rect.x += self.xvel
            self.yvel += .4
        elif self.type == 'shot6':
            self.orginalimg = g.images['inventory'][0].subsurface((6 * 32, 6*32, 32, 32))
            self.rect.y += self.yvel
            self.rect.x += self.xvel
            self.yvel += .4
        elif self.type == 'shot7':
            t = (self.timer / 2 % 3)
            self.orginalimg = g.images['inventory'][0].subsurface(((1 + t) * 32, 7*32, 32, 32))

        self.image = pygame.transform.flip(self.orginalimg, 1-self.direction, 0)

        if self.invisible_timer > 0:
            self.invisible_timer -= 1
            self.image = g.images['inventory'][0].subsurface((0, 0, 0, 0))


        # die after a while
        if self.timer > self.keep_alive:
            self.destroy()
        self.timer += 1

    # rebound
    def rebound_spawner(self, n):
        self.xvel = -self.xvel
        self.rect.x += self.xvel * 2
        if n == 1:
            self.callback((self.rect.x - self.xvel * 2, self.rect.y - self.yvel))
            self.destroy()

    # destroy the bullet
    def rebound(self, n):
        self.destroy()

    # destroy the self
    def destroy(self):
        Effect(self.g, 'shot', (self.rect.x - 10, self.rect.y - 13))
        if self in self.g.sprites:
            self.g.sprites.remove(self)
        if self in self.g.removeOnLeave:
            self.g.removeOnLeave.remove(self)
        if self in self.g.bullets:
            self.g.bullets.remove(self)

    # time between shots
    def get_reload_time(self):
        return self.reload

    # destroy the shot
    def get_damage(self):
        return self.damage