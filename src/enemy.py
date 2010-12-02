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
    changedDirLastTick = 0

    def __init__(self, g, pos, name):
        # texture for the avatar
        self.image = pygame.Surface((32,32), SRCALPHA)
        Sprite.__init__(self, self.image, Rect(0,0,32,32))
        g.removeOnLeave.append(self)
        self.groups = g.string2groups('shot')
        self.g = g
        self.rect.x,self.rect.y = pos[0],pos[1] # meh hack
        self._rect.x,self._rect.y = self.rect.x,self.rect.y
        self.startrect = Rect(pos[0], pos[1], 32,32)
        self.name = name
        g.sprites.append(self)
        if name == 'bird':
            hitSoundFile = os.path.join("effects",  "critter.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.rect.y += 8 # offset
        elif name == 'rat':
            hitSoundFile = os.path.join("effects",  "critter2.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.health = 6
        elif name == 'monster0':
            hitSoundFile = os.path.join("effects",  "critter3.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.health = 6
        elif name == 'monster1': # mushroom head
            hitSoundFile = os.path.join("effects",  "critter4.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.health = 20
            self.rect.height = 64
            self.waketype = 'near' # either near or water
            self.wet = 0
            self.squirt2 = pygame.mixer.Sound(os.path.join("effects",  "squirt2.wav"))
        elif name == 'monster2': # slime mold
            hitSoundFile = os.path.join("effects",  "critter4.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.health = 3
            self.rect.height = 16
        elif name == 'nurse': # a nurse that runs around, trying to stab you
            hitSoundFile = os.path.join("effects",  "critter6.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.health = 2
            self.speed = 4
            self.direction = random.randint(0, 2) % 2
            self.mode = 'walking'
        elif name == 'monster5': # a plant like monster with electrial shots
            hitSoundFile = os.path.join("effects",  "critter7.wav")
            self.birdhit = pygame.mixer.Sound(hitSoundFile)
            self.health = 8
            self.speed = 3
            self.direction = random.randint(0, 2) % 2
            self.mode = 'idle'
            self.jumpvel = 0.0
            self.jumpstart = 8.0
        elif name == 'bugs':
            self.frm1 = g.images['inventory'][0].subsurface((7 * 32, 7 * 32, 32, 32))
            self.frm2 = g.images['inventory'][0].subsurface((6 * 32, 7 * 32, 32, 32))
            self.rect.y += 2
            self.rect.x += random.randint(-4,4)
            self.flying = 0
            self.vecx = random.randint(-5,5)
            self.vecy = 0
        elif name == 'drip':# not really an enemy
            self.frm1 = g.images['inventory'][0].subsurface((0 * 32, 8 * 32, 32, 32))
            self.frm2 = g.images['inventory'][0].subsurface((1 * 32, 8 * 32, 32, 32))
            self.frm3 = g.images['inventory'][0].subsurface((2 * 32, 8 * 32, 32, 32))
            self.frm4 = g.images['inventory'][0].subsurface((3 * 32, 8 * 32, 32, 32))
            self.timer = random.randint(0, 50)
        elif name == 'drop':# not really an enemy
            self.image = g.images['inventory'][0].subsurface((4 * 32, 8 * 32, 32, 32))
            self.rect.height = 8
            self.speed = 6
        elif name == 'monster6': # a ghost monster that floats around and shoots
            print 'new monster 6'
            self.image = pygame.Surface((64,64), SRCALPHA)
            self.startpos = self.rect.x,self.rect.y
            self.targeting = 0
            self.float_target = (0,0)
            self.gravity = 0
            self.bump = 0
        hitSoundFile = os.path.join("effects",  "exp1.wav")
        self.destryoed = pygame.mixer.Sound(hitSoundFile)

        
    # upon each loop
    def loop(self, g, r):
        self.pos = g.screen_to_tile((self.rect.x - g.view.x + 8, self.rect.y - g.view.y + 16))
        canbehit = 1
        canhitplayer = 1

        if self.name == 'bird':
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
        elif self.name == 'rat':
            if self.mode == 'idle':
                self.image = g.images['rat'][0].subsurface((0, 0, 32, 32))
            elif self.mode == 'ouch':
                self.image = g.images['rat'][0].subsurface((3 * 32, 0, 32, 32))
                self.btimer += 1
                if self.btimer > 10:
                    self.btimer = 0
                    self.mode = 'run'
                    self.direction = 0
                    if self.rect.x < g.player.rect.x:
                        self.direction = 1
            elif self.mode == 'run':
                belowpos = g.clayer[self.pos[1] + 1][self.pos[0]]
                if belowpos != 1:
                    self.direction = not self.direction
                fnum = 1 + (self.timer / 2 % 2 == 0)
                self.image = g.images['rat'][0].subsurface((fnum * 32, 0, 32, 32))
                self.rect.x -= 3
                self.btimer += 1
                if self.btimer > 50:
                    self.mode = 'idle'
                    self.btimer = 0
                if self.direction == 1:
                    self.rect.x += 6
            elif self.mode == 'death':
                self.image = g.images['rat'][0].subsurface((3 * 32, 0, 32, 32))
                self.btimer += 1
                if self.btimer > 10:
                    self.destroy()
        elif self.name == 'monster0':
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
        elif self.name == 'monster1':
            canbehit = 0
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
                    e = Enemy(self.g, (self.rect.x, self.rect.y + 48), 'monster2')
                    e.direction = self.direction
                    self.direction = not self.direction
                    self.squirt2.play()
            elif self.mode == 'death':
                frme = (self.btimer / 4)
                self.image = g.images['monster1'][0].subsurface((frme * 32, 128, 32, 64))
                self.btimer += 1
                if (self.btimer / 4) > 6:
                    self.destroy()
        elif self.name == 'monster2': # green slime
            self.pos = g.screen_to_tile((self.rect.x - g.view.x + 16, self.rect.y - g.view.y + 32))
            canbehit = 0
            frme = (self.timer / 4) % 7
            self.image = g.images['monster2'][0].subsurface((frme * 32, 0, 32, 16))
            belowpos = g.clayer[self.pos[1] ][self.pos[0]]

            if belowpos != 1:
                if self.changedDirLastTick:
                    self.rect.y += 10
                else:
                    self.direction = not self.direction
                    self.changedDirLastTick = 1
            else:
                self.changedDirLastTick = 0

            self.rect.x -= 1
            if self.direction == 1:
                self.rect.x += 2
            self.btimer += 1
            if self.btimer > 200:
                self.destroy()
        elif self.name == 'nurse': # doctors children
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
        elif self.name == 'monster5':
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
        elif self.name == 'bugs': # bugs
            if self.flying == 1:
                if (self.timer / 2) % 2 == 0:
                    self.image = self.frm1
                else:
                    self.image = self.frm2
                self.rect.x += math.sin(self.timer / 3) * 3 + self.vecx
                self.rect.y += self.vecy
                if self.timer > self.timerout:
                    self.vecy += .5
            # start flying
            if self.pos == g.player.pos and self.flying == 0:
                self.flying = 1
                self.vecy = -1.0 -  random.randint(0,2)
                self.vecx = random.randint(-5,5)
                self.timer = 0
                self.timerout = 50 + random.randint(0,50)
            self.timer += 1
            return
        elif self.name == 'drip':
            frme = (self.timer / 3) % 30
            if frme == 1:
                self.image = self.frm2
            elif frme == 2:
                self.image = self.frm3
            elif frme == 3:
                self.image = self.frm4
            elif frme == 4:
                Enemy(g, (self.rect.x, self.rect.y), 'drop')
                self.timer += 3 # hack. to the next frame
            else:
                self.image = self.frm1
            self.timer += 1
            return
        elif self.name == 'drop':
            self.rect.y += self.speed
            return
        elif self.name == 'monster6':
            if self.targeting:
                self.float_target = (g.player.rect.x,g.player.rect.y)
            if self.timer % 30 == 0:
                self.float_target = (self.startpos[0] + random.randint(-30, 30), self.startpos[1] + random.randint(-30, 30))

            self.rect.y += self.gravity - self.bump
            timerstart = 5 # time between bumps
            self.direction = self.float_target[1] > self.rect.y
            if self.float_target[0] > self.rect.x:
                timerstart = 3 # bumping up, less wait time
            if self.timer % (timerstart + random.randint(0, 3)) == 0:
                self.bump = 1

            print self.gravity, self.bump
            self.gravity -= 1
            if self.gravity < -4:
                self.gravity = -4
            
            if self.bump != 0:
                self.bump += 1
                if self.bump == 1:
                    self.gravity = 0
                if self.bump > 3:
                    self.image = g.images['monster6'][0].subsurface((0 * 64, 0 * 64, 64, 64))
                else:
                    self.image = g.images['monster6'][0].subsurface((0 * 64, 0 * 64, 64, 64))
                if self.bump > 6:
                    self.bump = 0
            else:
                # normal
                self.image = g.images['monster6'][0].subsurface((0 * 64, 0 * 64, 64, 64))





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

        #spawn a random inventory
        if self.name == 'bird':
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
        elif self.name == 'rat':
            rint = random.randint(1, 2)
            if rint == 1:
                Inventory(self.g, 'health', (self.rect.x, self.rect.y))
            elif rint == 2:
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
        elif self.name == 'monster0':
            rint = random.randint(1, 3)
            if rint == 1:
                Inventory(self.g, 'shot4', (self.rect.x, self.rect.y))
            elif rint == 2:
                Inventory(self.g, 'health', (self.rect.x, self.rect.y))
            elif rint == 3:
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
        elif self.name == 'monster5':
            rint = random.randint(1, 3)
            if rint == 1:
                Inventory(self.g, 'shot7', (self.rect.x, self.rect.y))
            elif rint == 2:
                Inventory(self.g, 'health', (self.rect.x, self.rect.y))
            elif rint == 3:
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))
                Inventory(self.g, 'skyberry', (self.rect.x, self.rect.y))

        # boom
        self.destryoed.play()
        self.g.sprites.remove(self)

    # hit 
    def hit(self, g, s, b):
        print g,s,b

    def rebound(self, h):
        if self.name == 'bird':
            self.destroy()
        elif self.name == 'rat':
            if self.mode == 'run':
                self.direction = not self.direction
        elif self.name == 'monster1':
            if self.mode == 'walk':
                self.direction = not self.direction
        elif self.name == 'monster2':
            self.direction = not self.direction
        elif self.name == 'monster5':
            self.direction = not self.direction
            if self.mode == 'jump':
                if self.jumpvel < 0:
                    self.mode = 'idle'
                else:
                    self.jumpvel = -10
        elif self.name == 'nurse':
            self.direction = not self.direction
            self.mode = 'walking'
        elif self.name == 'bugs':
            if h == 1:
                self.flying = 0
            elif h == 2:
                self.vecx = -5
            elif h == 3:
                self.vecx = 5
        elif self.name == 'drop':
            self.g.sprites.remove(self)

    # if you touch it, how much health to take off
    def get_damage(self):
        return 1