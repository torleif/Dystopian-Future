""" a mushroom head monster. walks around pulling his guts out"""
import pygame
from pygame.locals import *
import os
import sys; sys.path.insert(0, "..")
from enemy import Enemy
from enemies.monster2 import Monster2


class Monster1(Enemy):
    """ Mushroom head. runs around, doesn't do much

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'monster1')
        hitSoundFile = os.path.join("effects",  "critter4.wav")
        self.birdhit = pygame.mixer.Sound(hitSoundFile)
        self.health = 20
        self.rect.height = 64
        self.waketype = 'near' # either near or water
        self.wet = 0
        self.squirt2 = pygame.mixer.Sound(os.path.join("effects",  "squirt2.wav"))

    # behavour
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        canbehit = 0
        canhitplayer = 1
        if self.mode == 'idle':
            canhitplayer = 0
            self.image = g.images['monster1'][0].subsurface((0, 64, 32, 64))
            if self.waketype == 'near':
                dy = self.rect.x - g.player.rect.x
                dh = self.rect.y - g.player.rect.y
                canhitplayer = 0
                if dy < 70 and dy > -70:
                    if dh < 70 and dh > -70:
                        self.mode = 'waking'
                        self.btimer = 0
            elif self.waketype == 'water' and self.wet:
                self.mode = 'waking'
                self.btimer = 0
        elif self.mode == 'waking':
            self.image = g.images['monster1'][0].subsurface(((self.btimer / 5) * 32, 64, 32, 64))
            self.btimer += 1
            canhitplayer = 0
            if (self.btimer / 5) > 2:
                self.mode = 'awake'
                self.btimer = 0
        elif self.mode == 'awake':
            self.image = g.images['monster1'][0].subsurface((0, 0, 32, 64))
            self.btimer += 1
            if self.btimer > 15:
                self.mode = 'walk'
                self.timer = 0
        elif self.mode == 'walk':
            canbehit = 1
            self.btimer += 1
            frme = (self.timer / 4) % 5 + 1
            self.image = g.images['monster1'][0].subsurface((frme * 32, 0, 32, 64))
            belowpos = g.clayer[self.pos[1] + 2][self.pos[0]]
            if belowpos != 1:
                self.direction = not self.direction
            self.rect.x -= 2
            if self.direction == 1:
                self.rect.x += 4
            dy = self.rect.x - g.player.rect.x
            dh = self.rect.y - g.player.rect.y
            if dy < 50 and dy > -90:
                if dh < 50 and dh > -50:
                    if self.btimer > 10:
                        self.mode = 'attack'
                        self.btimer = 0
        elif self.mode == 'ouch':
            self.image = g.images['monster1'][0].subsurface((7 * 32, 0, 32, 64))
            self.btimer += 1
            if self.btimer > 10:
                self.mode = 'walk'
        elif self.mode == 'attack':
            frme = (self.btimer / 4) + 3
            self.image = g.images['monster1'][0].subsurface((frme * 32, 64, 32, 64))
            self.btimer += 1
            if (self.btimer / 4) > 4:
                self.image = g.images['monster1'][0].subsurface((0, 0, 32, 64))
                self.btimer = 0
                self.mode = 'walk'
                e = Monster2(self.g, (self.rect.x, self.rect.y + 48))
                e.direction = self.direction
                self.direction = not self.direction
                self.squirt2.play()
        elif self.mode == 'death':
            frme = (self.btimer / 4)
            self.image = g.images['monster1'][0].subsurface((frme * 32, 128, 32, 64))
            self.btimer += 1
            if (self.btimer / 4) > 6:
                self.destroy()
        self.loop_hit_death(g, r, canbehit, canhitplayer)


    # walk away from the wall
    def rebound(self, h):
        if self.mode == 'walk':
            self.direction = not self.direction