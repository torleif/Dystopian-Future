""" inventory object """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
from effect import Effect
import random
import math

class Inventory(Sprite):
    """ An item that can be picked up

    """
    framecount = 0
    timer = 0
    savedisabletimer = 0
    max_bullet = 0
    flash = 1

    def __init__(self, g, name, pos = (0,0)):
        spawnonce = 0
        # texture for the avatar
        self.orginalimg = g.images['inventory'][0].subsurface((0, 0, 32, 32))
        self.image = self.orginalimg
        self.extraimg = None
        if name == 'save': # save
            self.orginalimg = g.images['inventory'][0].subsurface((4 * 32, 0, 32, 32))
            self.image = self.orginalimg
            self.savetimer = 0
            activateSoundFile = os.path.join("effects",  "save.wav")
            self.savesound = pygame.mixer.Sound(activateSoundFile)
        elif name == 'health': # health one up
            self.orginalimg = g.images['inventory'][0].subsurface((0, 2*32, 32, 32))
            self.image = self.orginalimg
        # increase Max Health. Many of these.
        elif name.find('healthincrease', 0) == 0:
            self.orginalimg = g.images['inventory'][0].subsurface((1*32, 3*32, 32, 32))
            self.image = self.orginalimg
            self.open = 0
            self.displaymsg = 0
        elif name == 'shot2': # a green shot that comes from birds. -2
            self.orginalimg = g.images['inventory'][0].subsurface((2 * 32, 2*32, 32, 32))
            self.image = self.orginalimg
            sprimg = g.images['inventory'][0].subsurface((3 * 32, 2*32, 32, 32))
            self.extraimg = Sprite(sprimg, Rect(0,0,32,32))
            g.sprites.append(self.extraimg)
            g.removeOnLeave.append(self.extraimg)
            self.max_bullet = 3 # max bullets for shot1
        elif name == 'shot4': # blue shot from monsters
            self.orginalimg = g.images['inventory'][0].subsurface((2 * 32, 2*32, 32, 32))
            self.image = self.orginalimg
            sprimg = g.images['inventory'][0].subsurface((5 * 32, 2*32, 32, 32))
            self.extraimg = Sprite(sprimg, Rect(0,0,32,32))
            g.sprites.append(self.extraimg)
            g.removeOnLeave.append(self.extraimg)
            self.max_bullet = 4 # max bullets for shot1
        elif name == 'shot7': # eletric shot from monsters
            self.orginalimg = g.images['inventory'][0].subsurface((2 * 32, 2*32, 32, 32))
            self.image = self.orginalimg
            sprimg = g.images['inventory'][0].subsurface((0, 7*32, 32, 32))
            self.extraimg = Sprite(sprimg, Rect(0,0,32,32))
            g.sprites.append(self.extraimg)
            g.removeOnLeave.append(self.extraimg)
            self.max_bullet = 5 # max bullets for shot1
        elif name == 'switch':
            self.orginalimg = g.images['inventory'][0].subsurface((3*32, 3*32, 32, 32))
            self.image = self.orginalimg
            self.open = 0
            self.displaymsg = 0
            self.pulled = pygame.mixer.Sound(os.path.join("effects",  "switch.wav"))
        elif name == 'spike':
            self.orginalimg = g.images['inventory'][0].subsurface((0, 3*32, 32, 32))
            self.image = self.orginalimg
            self.timerloop = 200
            self.timer = random.randint(0, self.timerloop)
        elif name == 'aspike':
            self.orginalimg = g.images['inventory'][0].subsurface((4*32, 10*32, 32, 32))
            self.image = self.orginalimg
        elif name == 'arms':
            self.orginalimg = g.images['inventory'][0].subsurface((2*32, 4*32, 32, 32))
            self.image = self.orginalimg
            spawnonce = 1
        elif name == 'sprinkler':
            self.image = g.images['inventory'][0].subsurface((3*32, 4*32, 32, 32))
            self.on = 0
            self.timer = 0
        elif name == 'clonevat':
            self.orginalimg = pygame.image.load(os.path.join("textures",  "clonevats.png")).convert_alpha()
        elif name == 'plane':
            self.orginalimg = pygame.image.load(os.path.join("textures",  "plane.png")).convert_alpha()
        elif name == 'flutterbox':
            self.orginalimg = g.images['inventory'][0].subsurface((7*32, 4*32, 32, 32))
            self.image = self.orginalimg
            spawnonce = 1
        elif name == 'flutterswitch':
            self.orginalimg = g.images['inventory'][0].subsurface((0, 5*32, 32, 32))
            self.image = self.orginalimg
        elif name == 'fish0':
            self.orginalimg = pygame.image.load(os.path.join("textures",  "fish0.png")).convert_alpha()
        elif name == 'fish1':
            self.orginalimg = pygame.image.load(os.path.join("textures",  "fish1.png")).convert_alpha()
        elif name == 'skyberry':
            self.orginalimg = g.images['inventory'][0].subsurface((3*32, 5*32, 8, 8))
            self.image = self.orginalimg
            self.rotate_timer = 0
            self.xvel = float(random.randint(-20, 20))
            self.rotate_amount = self.xvel / 2
            self.gravity = 3.0
            self.canget = 1
        elif name == 'newspaper':
            self.gotten = 0
            self.orginalimg = g.images['inventory'][0].subsurface((0, 10*32, 32, 32))
            self.image = self.orginalimg
            spawnonce = 1
        elif name == 'drawingwater':
            # (6, 19)  ( 192 536 + 64 )
            self.orginalimg = g.images['inventory'][0].subsurface((1*32, 10*32, 32, 32))
            print 'drawingwater'
        elif name == 'waterfall':
            # (6, 19)  ( 192 536 + 64 )
            self.orginalimg1 = g.images['inventory'][0].subsurface((2*32, 10*32, 32, 32))
            self.orginalimg2 = g.images['inventory'][0].subsurface((3*32, 10*32, 32, 32))
        elif name == 'coin':
            self.orginalimg = g.images['inventory'][0].subsurface((6*32, 10*32, 32, 32))
            self.image = self.orginalimg
            spawnonce = 1
        elif name == 'jailkey':
            self.orginalimg = g.images['inventory'][0].subsurface((5*32, 10*32, 32, 32))
            self.image = self.orginalimg
            spawnonce = 1
        elif name == 'tape': # imas backup tape
            self.orginalimg = g.images['inventory'][0].subsurface((7*32, 10*32, 32, 32))
            self.image = self.orginalimg
            spawnonce = 1

        Sprite.__init__(self, self.image, Rect(pos[0],pos[1],32,32))
        self.rect.x,self.rect.y = pos[0],pos[1]
        self._rect.x,self._rect.y = self.rect.x,self.rect.y
        g.sprites.append(self)
        self.groups = g.string2groups('inventory')
        self.g = g

        if name == 'microwave' or spawnonce: # spawn once items
            if 'i_' + name in g.saveData:
                g.sprites.remove(self)
                print 'found i_' + name
        elif name.find('healthincrease', 0) == 0: # open once
            if 'i_' + name in g.saveData:
                self.open = 1
        self.name = name
        g.removeOnLeave.append(self)
        
        # small skyberry
        if name == 'skyberry':
            self.rect.width,self.rect.height = 8,8

    # pulls the switch
    def pull_switch(self):
        self.open = not self.open

    def rebound(self,v):
        if self.name == 'skyberry' and v == 1:
            self.gravity = None


    # upon each loop
    def loop(self, g, r):
        self.image = self.orginalimg
        # get my cell position. Probally should be in Sprite
        myPos = g.screen_to_tile((self.rect.x - g.view.x + 16, self.rect.y - g.view.y + 16))

        #
        if self.name == 'save': # save is animated
            frameno = (self.timer /3 % 6)
            if frameno > 3:
                frameno = 6 - frameno
            if self.savetimer > 0: # disable the save button
                self.savetimer -= 1
                self.image = g.images['inventory'][0].subsurface((0, 0, 0, 0))
                return
            self.orginalimg = g.images['inventory'][0].subsurface(((3+frameno) * 32, 0, 32, 32))
            self.image = self.orginalimg
        elif self.name == 'health': # health is animated
            frameno = (self.timer / 4 % 2)
            self.orginalimg = g.images['inventory'][0].subsurface(((frameno) * 32, 2*32, 32, 32))
            self.image = self.orginalimg
        elif self.name == 'shot2':
            self.orginalimg = g.images['inventory'][0].subsurface((2 * 32, 2*32, 32, 32))
            self.image = self.orginalimg
            self.extraimg.rect.x = self.rect.x
            self.extraimg.rect.y = self.rect.y - 6
        elif self.name == 'shot4':
            self.orginalimg = g.images['inventory'][0].subsurface((2 * 32, 2*32, 32, 32))
            self.image = self.orginalimg
            self.extraimg.rect.x = self.rect.x - 3
            self.extraimg.rect.y = self.rect.y - 4
        elif self.name == 'shot7':
            self.orginalimg = g.images['inventory'][0].subsurface((2*32, 2*32, 32, 32))
            self.image = self.orginalimg
            self.extraimg.rect.x = self.rect.x
            self.extraimg.rect.y = self.rect.y - 1
        elif self.name.find('healthincrease', 0) == 0:
            if self.open == 0:
                self.image = g.images['inventory'][0].subsurface((1*32, 3*32, 32, 32))
            else:
                self.image = g.images['inventory'][0].subsurface((2*32, 3*32, 32, 32))
            if self.displaymsg == 1:
                str = "\nMax health increased by 2!"
                g.level.info_box(str)
                if g.player.pos != myPos:
                    self.displaymsg = 0
        elif self.name == 'switch':
            if self.open == 0:
                self.image = g.images['inventory'][0].subsurface((3*32, 3*32, 32, 32))
            else:
                self.image = g.images['inventory'][0].subsurface((4*32, 3*32, 32, 32))
            if self.displaymsg == 1:
                if g.player.pos != myPos:
                    self.displaymsg = 0
                else:
                    str = "\nSwitch pulled"
                    g.level.info_box(str)
        elif self.name == 'spike':
            tmer = (self.timer / 2)  % self.timerloop
            if tmer == (self.timerloop-4):
                self.image = g.images['inventory'][0].subsurface((2*32, 9*32, 32, 32))
            elif tmer == (self.timerloop-3):
                self.image = g.images['inventory'][0].subsurface((3*32, 9*32, 32, 32))
            elif tmer == (self.timerloop-2):
                self.image = g.images['inventory'][0].subsurface((4*32, 9*32, 32, 32))
            elif tmer == (self.timerloop-1):
                self.image = g.images['inventory'][0].subsurface((5*32, 9*32, 32, 32))
            else:
                self.image = self.orginalimg
        elif self.name == 'aspike':
            self.orginalimg = g.images['inventory'][0].subsurface((4*32, 10*32, 32, 32))
            self.image = self.orginalimg
        elif self.name == 'clonevat':
            k = self.timer % 8
            if k == 0:
                po = self.rect.x + 30 + random.randint(0, 50), self.rect.y + 100
                Effect(self.g, 'bubble', po)
            elif k == 4:
                po = self.rect.x + 160 + random.randint(0, 50), self.rect.y + 100
                Effect(self.g, 'bubble', po)
            self.timer += 1
            return
        elif self.name == 'plane':
            self.image = self.orginalimg
            return
        elif self.name == 'fish0':
            return
        elif self.name == 'fish1':
            return
        elif self.name == 'arms':
            self.image = g.images['inventory'][0].subsurface((2*32, 4*32, 32, 32))
        elif self.name == 'sprinkler':
            self.image = g.images['inventory'][0].subsurface((3*32, 4*32, 32, 32))
            if self.on:
                self.timer += 1
                if self.timer % 2 == 0:
                    Effect(self.g, 'water', (self.rect.x, self.rect.y + 3))
            return
        elif self.name == 'flutterswitch':
            return
        elif self.name == 'skyberry':
            self.image = pygame.transform.rotate(self.orginalimg, self.rotate_timer)
            if self.rotate_amount > 0:
                self.rotate_timer += int(self.rotate_amount)
                self.rotate_amount -= 0.2
            if self.gravity != None:
                self.rect.y -= self.gravity
                self.gravity -= .5
                self.rect.x -= self.xvel
                self.xvel /= 2
            plpos = (g.player.rect.x+g.player.rect.width/2, g.player.rect.y+g.player.rect.height)
            dx,dy = plpos[0] - self.rect.x, plpos[1] - self.rect.y
            if dx < 8 and dx > 0 and dy < 12 and dy > 4 and self.canget:
                self.destroy()
                self.g.player.get_skyberry()
            if not self.canget:
                self.timer += 1
                if self.timer > 30:
                    self.removeself()
            return
        elif self.name == 'drawingwater':
            self.image = pygame.Surface((384, 200), SRCALPHA)
            self.timer += 1
            ypos = 202 - self.timer / 10
            self.image.fill((30,108, 137,165), pygame.Rect(0,ypos,384, 200))
            for i in xrange(14):
                self.image.blit(self.orginalimg, (math.sin(self.timer/10.0) * 16 + i*32 - 32, ypos-17))
            return
        elif self.name == 'waterfall':
            self.timer += 1
            self.image = pygame.Surface((32, 160), SRCALPHA)
            self.image.fill((30,108, 137,165), pygame.Rect(13,20, 16,130 + 13 - self.timer / 10))
            if self.timer / 2 % 2 == 0:
                self.image.blit(self.orginalimg1, (0,0))
            else:
                self.image.blit(self.orginalimg2, (0,0))
            return



        # if you're interacting with the switch
        if g.player.pos == myPos:
            # items you get by simply walking over
            if self.name == 'health':
                g.player.addHealth(1)
                self.destroy()
            elif self.name == 'spike':
                g.player.touch(self)
            elif self.name == 'aspike':
                g.player.touch(self)
            elif self.name == 'switch':
                if self.displaymsg == 0 and g.event:
                    self.displaymsg = 1
                    self.pull_switch()
                    self.pulled.play()
            elif self.name == 'shot2':
                self.destroy()
                if g.saveData['shot2'] < self.max_bullet:
                    g.saveData['weapon'] = 2
                    g.saveData['shot2'] += 1
            elif self.name == 'shot4':
                self.destroy()
                if g.saveData['shot4'] < self.max_bullet:
                    g.saveData['weapon'] = 4
                    g.saveData['shot4'] += 1
            elif self.name == 'shot7':
                self.destroy()
                if g.saveData['shot7'] < self.max_bullet:
                    g.saveData['weapon'] = 7
                    g.saveData['shot7'] += 1
            # items you have to manually gather
            elif g.player.looking:
                if self.name == 'save':
                    g.save(g)
                    self.savetimer = 100 # 100 ticks disabled
                    Effect(self.g, 'explosion', (self.rect.x, self.rect.y))
                    Effect(self.g, 'msg', (self.rect.x, self.rect.y), 'Saved!')
                    self.savesound.play()
                elif self.name.find('healthincrease', 0) == 0:
                    if self.open == 0:
                        self.open = 1
                        self.displaymsg = 1
                        g.saveData['i_' + self.name] = 1
                        g.player.healthmax += 2
                        g.player.health += 2
                        g.saveData['healthmax'] = g.player.healthmax
                else:
                    g.saveData['i_' + self.name] = 1
                    self.destroy()
                    if self.name == 'newspaper':
                        self.gotten = 1
        self.timer += 1

        if self.timer/4 % 20 == 0:
            if self.name.find('healthincrease', 0) == 0 and self.open:
                return
            if self.name == 'spike' or self.name == 'switch' or self.name == 'sprinkler' or self.name == 'flutterswitch':
                return
            if self.name == 'skyberry' or self.name == 'aspike':
                return
            if self.flash:
                self.image = g.make_image_white(self.orginalimg)

    # put the character on the tile
    def pos(self, p):
        f = self.g.tile_to_screen((p[0], p[1]))
        self.rect.x = f[0] - self.g.view.x
        self.rect.y = f[1] - self.g.view.y
        self._rect.x = f[0] - self.g.view.x
        self._rect.y = f[1] - self.g.view.y
        self.walktopos = (self.rect.x, self.rect.y)

    def destroy(self):
        self.g.pickup.play()
        self.g.sprites.remove(self)
        self.g.removeOnLeave.remove(self)
        if self.extraimg in self.g.sprites:
            self.g.sprites.remove(self.extraimg)

    def removeself(self):
        self.g.sprites.remove(self)
        self.g.removeOnLeave.remove(self)
        if self.extraimg in self.g.sprites:
            self.g.sprites.remove(self.extraimg)

    def get_damage(self):
        if self.name == 'aspike':
            return 15
        return 127