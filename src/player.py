""" Player class """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
from pgu import tilevid
from inventory import Inventory

from shot import Shot,Shot2,Shot4
from effect import Effect


SW,SH = 640,480
SPEED = 1
GRAVITY = 1
SPEED_MAX = 7

class Player(Sprite):
    """ Player object. 

    """
    pos = (0,0)
    health = 4
    healthmax = 4

    gravity = 0
    canjump = 0
    framecount = 0
    direction = 0
    looking = 0
    staylooking = 0
    animation = 0
    shotwait = 0
    shotcounter = 0
    imortal = 0 # after being hit by a enimy, this will be a timer down
    dx = 0
    snowwalk = 0
    hidden = 0
    jumpshoot = 0 # jumping while shooting
    maxspeed = SPEED_MAX
    jump_gravity = 15
    dieanimation = 0# a special hack when you're drowing in after defeating robot
    
    def __init__(self, g, t):
        g.clayer[t.ty][t.tx] = 0
        self.rect = Rect(t.rect.x + 16 - g.view.x, t.rect.y - g.view.y, 32, 32)
        Sprite.__init__(self, g.images['player'], self.rect)
        self.renderoffset = (-13,0) # must be called after sprite init

        g.sprites.append(self)
        g.removeOnLeave.append(self)
        self.groups = g.string2groups('player')
        g.player = self
        g.infobox = 0
        self.orginalImage = self.image

        hitSoundFile = os.path.join("effects",  "hit.wav")
        self.hitSound = pygame.mixer.Sound(hitSoundFile)
        hitSoundFile = os.path.join("effects",  "ground.wav")
        self.hitground = pygame.mixer.Sound(hitSoundFile)
        hitSoundFile = os.path.join("effects",  "jump.wav")
        self.jumpsound = pygame.mixer.Sound(hitSoundFile)

        if g.loadPosition != None:
            pop = g.tile_to_screen(g.loadPosition)
            self.rect.x = pop[0] + g.view.x
            self.rect.y = pop[1] + g.view.y
            g.loadPosition = None
        self.g = g
        self.health = g.saveData['health']
        self.healthmax = g.saveData['healthmax']
        self._rect.x,self._rect.y = self.rect.x,self.rect.y
        self.jumping = 0
        self.rect.width = 8
        #place the camera on the player
        if not g.intermission:
            if self.rect.x > g.view.width:
                g.view.x = self.rect.x - g.view.width/2
            if self.rect.y > g.view.height:
                g.view.y = self.rect.y - g.view.height/2

    # you get a skyberry
    def get_skyberry(self):
        # add to the weapon
        if 'weapon' in self.g.saveData:
            if self.g.saveData['weapon'] >= 1:
                wpnstr = 'shot'+str(self.g.saveData['weapon'])+'_lvl'
                if self.g.saveData[wpnstr] == 10:
                    Effect(self.g, 'msg', (self.rect.x,self.rect.y), 'Level Up!')
                if self.g.saveData[wpnstr] == 20:
                    Effect(self.g, 'msg', (self.rect.x,self.rect.y), 'Level Up!')
                if self.g.saveData[wpnstr] >= 30: # limit = 30
                    return
                self.g.saveData[wpnstr] += 1

            
    # touching an enemy
    def touch(self, e):
        if self.imortal == 0:
            self.g.hurt.play()
            self.imortal = 10
            self.health -= e.get_damage()
            ef = Effect(self.g, 'health', (self.rect.x, self.rect.y))
            ef.healthchange = -e.get_damage()
            # drop some skyberries
            if 'weapon' in self.g.saveData:
                if self.g.saveData['weapon'] >= 1:
                    wpnstr = 'shot'+str(self.g.saveData['weapon'])+'_lvl'
                    if self.g.saveData[wpnstr] > 1:
                        self.g.saveData[wpnstr] -= 1
                        if self.g.saveData[wpnstr] == 9:
                            Effect(self.g, 'msg', (self.rect.x,self.rect.y), 'Level Down')
                        if self.g.saveData[wpnstr] == 19:
                            Effect(self.g, 'msg', (self.rect.x,self.rect.y), 'Level Down')
                        sb = Inventory(self.g, 'skyberry', (self.rect.x,self.rect.y))
                        sb.canget = 0
                        sb = Inventory(self.g, 'skyberry', (self.rect.x,self.rect.y))
                        sb.canget = 0
                        sb = Inventory(self.g, 'skyberry', (self.rect.x,self.rect.y))
                        sb.canget = 0

            self.g.player.gravity = 15
            self.g.player.jumping = 1
            if self.g.saveData['weapon'] != 0:
                shotType = 'shot' + str(self.g.saveData['weapon'])
                self.g.saveData[shotType] -= 1
            self.g.saveData['health'] = self.health
            
    # upon each loop
    def loop(self, g, r):
        if g.dead == 1:
            self.image = self.orginalImage.subsurface((0, 0, 0, 0))
            return

        keys = pygame.key.get_pressed()
        dy = 0
        self.pos = g.screen_to_tile((g.player.rect.x - g.view.x + 8, g.player.rect.y - g.view.y + 16))
        faced = 0
        aimup,aimdown = 0,0
        shooting = 0

        # move the player
        if g.intermission == 0:
            jumpkeydown = 0
            if keys[K_DOWN]:
                faced = 1
                if g.infobox:
                    self.staylooking = 1
                if self.jumpshoot:
                    aimdown = 1
            if keys[K_UP]:
                faced = 2
                # jump
                aimup = 1
            if keys[K_LEFT]:
                faced = 0
                self.staylooking = 0
                self.dx -= SPEED
                self.direction = 1
                if g.player.canjump:
                    self.framecount += 1
            if keys[K_RIGHT]:
                faced = 0
                self.staylooking = 0
                self.dx += SPEED
                self.direction = 0
                if g.player.canjump:
                    self.framecount += 1
            if keys[K_LEFT] and keys[K_RIGHT]:
                self.framecount = 0
            if keys[K_z]:
                if g.player.canjump == 1 and g.player.gravity == 0 and g.disable_fire == 0:
                    g.player.canjump = 0
                    g.player.gravity += self.jump_gravity
                    g.player.jumping = 1
                    self.jumpsound.play()
            if keys[K_x]:
                # firing code
                shooting = 1
                if g.level.weapon_gui == 0 and g.level.inventory_gui == 0:
                    if 'weapon' in g.saveData and g.disable_fire == 0:
                        if self.shotcounter <= 0 and g.saveData['weapon'] > 0:
                            xoffset = (not self.direction) * 2
                            shottype = 'shot' + str(g.saveData['weapon'])
                            sdirection = self.direction
                            if aimup:
                                sdirection = 2
                            if aimdown:
                                sdirection = 3
                            s = None
                            if shottype == 'shot2':
                                s = Shot2(g, sdirection, (self.rect.x - xoffset, self.rect.y + 20))
                            elif shottype == 'shot4':
                                s = Shot4(g, sdirection, (self.rect.x - xoffset, self.rect.y + 20))
                            else:
                                s = Shot(g, sdirection, (self.rect.x - xoffset, self.rect.y + 20), shottype)
                            s.invisible_timer = 1
                            self.shotcounter += s.get_reload_time()
            self.jumpshoot = 0
            if jumpkeydown == 0 and self.canjump == 0:
                self.jumpshoot = 1
            # the gui disables firing
            #if not keys[K_x]:
            #    g.disable_fire = 0
            if not keys[K_z]:
                g.disable_fire = 0
        # not walking
        if not keys[K_LEFT] and not keys[K_RIGHT]:
            self.framecount = 0

        # not going anywhere
        if keys[K_LEFT] and keys[K_RIGHT]:
            if self.dx > 0:
                self.dx -= SPEED
            if self.dx < 0:
                self.dx += SPEED
        if g.intermission:
            self.dx = 0

        if not keys[K_RIGHT] and self.dx > 0:
            self.dx -= SPEED
        if not keys[K_LEFT] and self.dx < 0:
            self.dx += SPEED

        if self.dx > self.maxspeed:
            self.dx = self.maxspeed
        if self.dx < -self.maxspeed:
            self.dx = -self.maxspeed
            
        # move camera with player
        if not g.intermission:
            if g.player.rect.x - g.view.x > SW - 200 and self.dx > 0:
                g.view.x += self.dx
            if g.player.rect.x - g.view.x < 200 and self.dx < 0:
                g.view.x += self.dx
            if g.player.rect.y - g.view.y > SH - 180:
                g.view.y += self.maxspeed
            if g.player.rect.y - g.view.y < 100:
                g.view.y -= self.maxspeed

        weaponvisible = 0
        if 'weapon' in g.saveData:
            if g.saveData['weapon'] != 0:
                weaponvisible = 1

        # animation
        iw,ih = g.player.image.get_width(), g.player.image.get_height()
        if weaponvisible == 0 or self.dieanimation == 1:
            g.player.image = g.player.orginalImage.subsurface((iw * ((self.framecount/3) % 5), 0, 32, 32))

            if g.following:
                # draw hand
                if g.connected == 1 and self.direction == 1:
                    g.player.image = pygame.Surface((32, 32), SRCALPHA)
                    g.player.image.blit(g.player.orginalImage.subsurface((iw * ((self.framecount/3) % 5), 6 * 32, 32, 32)), (0,0))
                    g.player.image.blit(g.player.orginalImage.subsurface((2 * 32, 4 * 32, 32, 32)), (7,0))
                    g.player.image = pygame.transform.flip(g.player.image, self.direction, 0)

            # looking forward
            if faced == 1 or self.staylooking:
                g.player.image = g.player.orginalImage.subsurface((5 * 32, 0, 32, 32))
            if faced == 2:
                g.player.image = g.player.orginalImage.subsurface((1 * 32, 32, 32, 32))
            # animations...
            if self.animation == 1:
                g.player.image = g.player.orginalImage.subsurface((6 * 32, 0, 32, 32))
            elif self.animation == 2:
                g.player.image = g.player.orginalImage.subsurface((7 * 32, 0, 32, 32))
            elif self.animation == 3:
                g.player.image = g.player.orginalImage.subsurface((0 * 32, 32, 32, 32))
            g.player.image = pygame.transform.flip(g.player.image, self.direction, 0)
        else:
            if self.direction == 0:
                g.player.image = g.player.orginalImage.subsurface((iw * ((self.framecount/3) % 5), 2 * 32, 32, 32))
            else:
                if g.following:
                    g.player.image = pygame.Surface((32, 32), SRCALPHA)
                    g.player.image.blit(g.player.orginalImage.subsurface((iw * ((self.framecount/3) % 5), 5 * 32, 32, 32)), (0,0))

                    # draw hand
                    if g.connected == 1 and self.direction == 1:
                        g.player.image.blit(g.player.orginalImage.subsurface((2 * 32, 4 * 32, 32, 32)), (7,0))
                else:
                    g.player.image = g.player.orginalImage.subsurface((iw * ((self.framecount/3) % 5), 3 * 32, 32, 32))
            # looking forward
            if (faced == 1 or self.staylooking) and not shooting and not self.jumping:
                if self.direction == 0:
                    g.player.image = g.player.orginalImage.subsurface((5 * 32, 2 * 32, 32, 32))
                else:
                    g.player.image = g.player.orginalImage.subsurface((5 * 32, 3 * 32, 32, 32))
            if faced == 2:
                if self.direction == 0:
                    g.player.image = g.player.orginalImage.subsurface((4 * 32, 1 * 32, 32, 32))
                else:
                    g.player.image = g.player.orginalImage.subsurface((5 * 32, 1 * 32, 32, 32))
            if self.jumping == 1:
                if self.direction == 0:
                    g.player.image = g.player.orginalImage.subsurface((6 * 32, 2 * 32, 32, 32))
                else:
                    g.player.image = g.player.orginalImage.subsurface((6 * 32, 3 * 32, 32, 32))
            if aimup :
                if self.direction:
                    self.image = g.player.orginalImage.subsurface((5 * 32, 1 * 32, 32, 32))
                else:
                    self.image = g.player.orginalImage.subsurface((4 * 32, 1 * 32, 32, 32))
            if aimdown:
                if self.direction:
                    self.image = g.player.orginalImage.subsurface((7 * 32, 1 * 32, 32, 32))
                else:
                    self.image = g.player.orginalImage.subsurface((6 * 32, 1 * 32, 32, 32))
        if g.player.gravity == 0:
            self.jumping = 0
        self.looking = faced
        g.infobox = 0

        if self.hidden == 1:
            self.image = self.orginalImage.subsurface((0, 0, 0, 0))



        # getting shot
        for b in g.bullets:
            if b.owner == 'enemy':
                drect = (b.rect.x, b.rect.y)
                if self.rect.collidepoint(drect):
                    self.touch(b)

        # edge
        g.player.gravity -= GRAVITY
        self.rect.x += self.dx
        self.rect.y += dy - g.player.gravity
        #self.rect.clamp_ip(g.view)
            
        # dead ...
        if self.health <= 0 and not g.dead:
            g.dead = 1
            g.exp2.play()
        if self.imortal > 0:
            if self.imortal/5 % 2 == 0:
                g.player.image = g.make_image_white(g.player.image)
            self.imortal -= 1

        # getting demoted 
        if self.g.saveData['weapon'] > 1:
            shottype = 'shot' + str(self.g.saveData['weapon'])
            if self.g.saveData[shottype] == 0:
                if self.g.saveData['weapon'] == 2:
                    self.g.saveData['weapon'] = 1
                elif self.g.saveData['weapon'] == 4:
                    self.g.saveData['weapon'] = 2
                elif self.g.saveData['weapon'] == 7:
                    self.g.saveData['weapon'] = 4
                else:
                    print 'weapon not down graded'

        # reloading the gun
        if self.shotcounter > 0:
            self.shotcounter -= 1


    # hitting the ground 
    def hit_ground(self):
        if self.gravity <= -14:
            self.hitground.play()
        if self.gravity <= -2:
            if self.snowwalk == 1:
                self.snowwalk = 0
                Effect(self.g, 'snow', (self.rect.x - 8, self.rect.y + 8))
                Effect(self.g, 'snow', (self.rect.x - 8, self.rect.y + 8))

    # adds some health to the player
    def addHealth(self, n):
        self.health += n
        ef = Effect(self.g, 'health', (self.rect.x, self.rect.y - 10))
        ef.healthchange = n
        if self.health > self.healthmax:
            self.health = self.healthmax
        self.g.saveData['health'] = self.health
