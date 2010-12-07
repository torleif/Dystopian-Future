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
    speed = 12
    keep_alive = 10
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
        elif type == 'shot3': # fox spray bullet
            g.shootSound3.play()
            self.orginalimg = g.images['inventory'][0].subsurface((5 * 32, 2*32, 32, 32))
            self.speed = 15
            self.keep_alive = 8
            self.damage = 1
            self.reload = 10
            self.yvel = random.randint(-2, 2)
        #elif type == 'shot4': # monster shot
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

    def move(self):
        if self.direction != 2 and self.direction != 3:
            self.rect.x -= self.speed * (self.direction * 2 - 1)
        elif self.direction == 2:
            self.rect.y -= self.speed
        elif self.direction == 3:
            self.rect.y += self.speed

        # die after a while
        if self.timer > self.keep_alive:
            self.destroy()
        self.timer += 1

    # some missiles should only be visible after it comes out of the gun.
    def loop_end(self):
        if self.invisible_timer > 0:
            self.invisible_timer -= 1
            self.image = self.g.images['inventory'][0].subsurface((0, 0, 0, 0))


    # upon each loop
    def loop(self, g, r):
        self.move()
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
        elif self.type == 'shot3':
            t = 5 + (self.timer / 2 % 3 == 0)
            self.orginalimg = g.images['inventory'][0].subsurface((t * 32, 2*32, 32, 32))
            self.rect.y += self.yvel
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
        self.loop_end()


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
        Effect(self.g, 'shot', (self.rect.x - 10, self.rect.y - 11))
        self.remove_sprite()

    # time between shots
    def get_reload_time(self):
        return self.reload

    # destroy the shot
    def get_damage(self):
        return self.damage

    def remove_sprite(self):
        if self in self.g.sprites:
            self.g.sprites.remove(self)
        if self in self.g.removeOnLeave:
            self.g.removeOnLeave.remove(self)
        if self in self.g.bullets:
            self.g.bullets.remove(self)

class Laser0(Shot):
    def __init__(self, g, direction, pos, owner = 'player'):
        Shot.__init__(self, g, direction, pos, 'laser0', owner)
        self.laser_color = Color(0xc7e3a3FF) # a yellowy color
        g.shootSound5.play()

        lenpus = 0
        while 1:
            self.pos = g.screen_to_tile((self.rect.x - g.view.x + (lenpus * -(direction*2-1)), \
                self.rect.y - g.view.y ))

            lenpus += 10
            if self.pos[0] >= g.size[0] or  self.pos[1] >= g.size[1] or \
                    g.view.x < 0 or g.view.y < 0:
                break
            if g.clayer[self.pos[1]][self.pos[0]] == 1:
                break;
            # limit to 500 pixels. It's fucking anyoing if you get shot accros the level
            if lenpus > 500:
                break;
        if direction == 1:
            self.rect.x -= lenpus

        self.image = pygame.Surface((lenpus, 10), SRCALPHA)
        self.image.fill(self.laser_color)
        self.keep_alive = 5
        self.rect.width = lenpus
        self.irect.width = lenpus

    def loop(self, g, r):
        # die after a while
        if self.timer > self.keep_alive:
            self.destroy()
        if self.timer == 1:
            self.image.fill((255,255,255,255), Rect(0, 0, self.image.get_width(), 1), BLEND_RGBA_SUB)
            self.image.fill((255,255,255,255), Rect(0, 9, self.image.get_width(), 1), BLEND_RGBA_SUB)
        if self.timer == 2:
            self.image.fill((255,255,255,255), Rect(0, 1, self.image.get_width(), 1), BLEND_RGBA_SUB)
            self.image.fill((255,255,255,255), Rect(0, 8, self.image.get_width(), 1), BLEND_RGBA_SUB)
        if self.timer == 3:
            self.image.fill((255,255,255,255), Rect(0, 2, self.image.get_width(), 1), BLEND_RGBA_SUB)
            self.image.fill((255,255,255,255), Rect(0, 7, self.image.get_width(), 1), BLEND_RGBA_SUB)
        if self.timer == 4:
            self.image.fill((255,255,255,255), Rect(0, 3, self.image.get_width(), 1), BLEND_RGBA_SUB)
            self.image.fill((255,255,255,255), Rect(0, 6, self.image.get_width(), 1), BLEND_RGBA_SUB)
        self.timer += 1

        # other bullets only check point, so we check rect for this one
        if self.rect.colliderect(g.player.rect):
            g.player.touch(self)

    def rebound(self, n):
        pass

    def destroy(self):
        self.remove_sprite()

# green 'bio' bullet
class Shot2(Shot):
    def __init__(self, g, direction, pos, owner = 'player'):
        Shot.__init__(self, g, direction, pos, 'shot2', owner)
        g.shootSound2.play()
        self.speed = 14
        self.keep_alive = 10
        self.damage = 2 + self.level
        self.reload = 15

    def loop(self, g, r):
        self.move()
        if self.level == 0:
            self.image = g.images['inventory'][0].subsurface((6 * 32, 5*32, 32, 32))
        elif self.level == 1:
            t = 4 + (self.timer / 2 % 2 == 0)
            self.image = g.images['inventory'][0].subsurface((t * 32, 5*32, 32, 32))
        elif self.level == 2:
            t = 3 + (self.timer / 2 % 2 == 0)
            self.image = g.images['inventory'][0].subsurface((t * 32, 2*32, 32, 32))
        self.loop_end()

    def rebound(self, n):
        self.destroy()

    def destroy(self):
        Effect(self.g, 'explosion0', (self.rect.x - 16, self.rect.y - 16))
        self.remove_sprite()

# bubble 'water' shot
class Shot4(Shot): 
    def __init__(self, g, direction, pos, owner = 'player'):
        Shot.__init__(self, g, direction, pos, 'shot4', owner)
        g.shootSound4.play()
        self.image = self.g.images['inventory'][0].subsurface((0, 0, 0, 0))
        self.speed = 9 + self.level * 2
        self.keep_alive = 11
        self.damage = 2 + self.level
        self.reload = 7
        self.rect.height = 10
        self.yvel = random.randint(-1, 0)
        self.invisible_timer = 2

    def loop(self, g, r):
        self.move()
        if self.level == 0:
            t = 3 + (self.timer / 2 % 2 == 0)
            self.image = g.images['inventory'][0].subsurface((t * 32, 6*32, 32, 32))
        elif self.level == 1:
            t = (self.timer / 2 % 2 == 0)
            self.image = g.images['inventory'][0].subsurface((t * 32, 6*32, 32, 32))
        elif self.level == 2:
            t = 5 + (self.timer / 2 % 3 == 0)
            self.image = g.images['inventory'][0].subsurface((t * 32, 3*32, 32, 32))
        if  self.direction != 2 and self.direction != 3:
            self.rect.y += self.yvel
        else:
            self.rect.x += self.yvel
        self.loop_end()

    def rebound(self, n):
        self.destroy()

    def destroy(self):
        Effect(self.g, 'explosion1', (self.rect.x - 16, self.rect.y - 16))
        self.remove_sprite()

    