""" Enemy. Things too shoot :) """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import random
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
import math
from effect import Effect
from inventory import Inventory
from shot import Shot



class Enemy(Sprite):
    """ Enemy. an item to shoot at

    """
    timer = 0
    direction = 0 
    mode = 'idle'
    startrect = None
    health = 2
    btimer = 0
    direction = 0

    def __init__(self, g, pos, name):
        # texture for the avatar
        self.image = pygame.Surface((32,32), SRCALPHA)
        Sprite.__init__(self, self.image, Rect(0,0,32,32)) # you may want to override this
        g.removeOnLeave.append(self)
        self.groups = g.string2groups('shot')
        self.g = g
        self.rect.x,self.rect.y = pos[0],pos[1] # meh hack
        self._rect.x,self._rect.y = self.rect.x,self.rect.y
        self.startrect = Rect(pos[0], pos[1], 32,32)
        self.name = name
        g.sprites.append(self)
        hitSoundFile = os.path.join("effects",  "exp1.wav")
        self.destryoed = pygame.mixer.Sound(hitSoundFile)
        
    # upon each loop
    def loop(self, g, r):
        pass


    """ gets called after each loop. does generic things like check if i'm being
        hit by bullets.

    """
    def loop_hit_death(self, g, r, canbehit, canhitplayer):
        self.timer += 1
        self.image = pygame.transform.flip(self.image, self.direction, 0)

        s = Rect(self.rect)
        if self.mode != 'death':
            if s.colliderect (g.player.rect):
                if canhitplayer:
                    g.player.touch(self)

        if canbehit:
            for b in g.bullets:
                if b.owner == 'player':
                    drect = (b.rect.x, b.rect.y)
                    if s.collidepoint(drect):
                        b.destroy()
                        self.health -= b.get_damage()
                        e = Effect(self.g, 'health', (self.rect.x, self.rect.y))
                        e.healthchange = -b.get_damage()
                        if self.mode != 'ouch':
                            self.birdhit.play()
                        self.mode = 'ouch'
                        self.btimer = 0
            #k = Rect(b.rect)
            #k.x -= g.view.x
            #k.y -= g.view.y
            #pygame.draw.rect(g.screen, (0,255,255), k)
        #s.x -= g.view.x
        #s.y -= g.view.y
        #pygame.draw.rect(g.screen, (255,0,255), s)
        

        # dead
        if self.health <= 0:
            if self.mode != 'death':
                self.mode = 'death'
                self.btimer = 0

    def destroy(self):
        Effect(self.g, 'explosion', (self.rect.x, self.rect.y))

        # boom
        self.destryoed.play()
        self.g.sprites.remove(self)

    # hit 
    def hit(self, g, s, b):
        print g,s,b

    def rebound(self, h):
        pass

    # if you touch it, how much health to take off
    def get_damage(self):
        return 1