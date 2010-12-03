""" Level base class """
import pygame
from pygame.locals import *
from pygame.rect import Rect
import os
import sys; sys.path.insert(0, "..")
from pgu.vid import Sprite
from shot import Shot
from effect import Effect
#from enemies.enemy import Enemy
from enemies.nurse import Nurse
from enemies.monster2 import Monster2
import random
import math

class Character(Sprite):
    """ Character object used to animate and control behavour of NPCs

    """
    walking = 0
    direction = 0
    framecount = 0
    walktopos = 0,0
    walkspeed = 6
    faceup = 0
    hidden = 0
    feeling = 'normal'# angry, depressed etc. used in the avatar
    oldRect = None
    type = None
    attacking = 0
    jumping = 0
    following = None

    def __init__(self, file, avatar, g, type = None):
        #load the image
        tileTexture = os.path.join("textures",  file)
        self.orginalImage = pygame.image.load(tileTexture)
        self.orginalImage = self.orginalImage.convert_alpha()

        # texture for the avatar
        tileTexture = os.path.join("textures",  avatar)
        self.orginalAvatar = pygame.image.load(tileTexture)
        # fox = 96 x 64
        # set the sprite image
        if type == 'fox':
            self.image = self.orginalImage.subsurface((0, 0, 96, 64))
            self.attacking = 0
            self.timer = 0
            self.jumping = 0    # ai bull shit
            self.health = 15
            self.jumpvec = 0
            self.healthmax = 15
            tileTexture = os.path.join("effects",  "shoot1.wav")
            self.hitme = pygame.mixer.Sound(tileTexture)
            self.teleport = pygame.mixer.Sound(os.path.join("effects",  "teleport1.wav"))
            self.lastframehidden = -1
        elif type == 'mushroom':
            self.secondImage = pygame.image.load(os.path.join("textures",  "mushroomhit.png"))
            self.image = self.orginalImage.subsurface((0, 0, 256, 256))
            self.attacking = 0
            self.timer = 0
            self.jumping = 0    # ai bull shit
            self.health = 60
            self.healthmax = 60
            self.dead = 0
            tileTexture = os.path.join("effects",  "critter5.wav")
            self.hitme = pygame.mixer.Sound(tileTexture)
            self.exp2 = pygame.mixer.Sound(os.path.join("effects",  "exp2.wav"))
            self.squirt = pygame.mixer.Sound(os.path.join("effects",  "squirt.wav"))
            self.squirt2 = pygame.mixer.Sound(os.path.join("effects",  "squirt2.wav"))
        elif type == 'doctor':
            self.squirt = pygame.mixer.Sound(os.path.join("effects",  "squirt3.wav"))
            self.hitme = pygame.mixer.Sound(os.path.join("effects",  "cry.wav"))
            self.attack = pygame.mixer.Sound(os.path.join("effects",  "doctor.wav"))

            self.imagea = pygame.image.load(os.path.join("textures",  "monster3a.png"))
            self.imageb = pygame.image.load(os.path.join("textures",  "monster3b.png"))
            self.imagec = pygame.image.load(os.path.join("textures",  "monster3c.png"))
            self.imaged = pygame.image.load(os.path.join("textures",  "monster3d.png"))
            self.imagee = pygame.image.load(os.path.join("textures",  "monster3e.png"))
            self.imagef = pygame.image.load(os.path.join("textures",  "monster3f.png"))
            self.imageg = pygame.image.load(os.path.join("textures",  "monster3g.png"))
            self.imageh = pygame.image.load(os.path.join("textures",  "monster3h.png"))
            self.imagei = pygame.image.load(os.path.join("textures",  "monster3i.png"))
            self.imagej = pygame.image.load(os.path.join("textures",  "monster3j.png"))
            self.imagek = pygame.image.load(os.path.join("textures",  "monster3k.png"))
            self.imagel = pygame.image.load(os.path.join("textures",  "monster3l.png"))
            self.image = self.orginalImage.subsurface((0, 0, 256, 256))
            self.attacking = 0
            self.timer = 0
            self.jumping = 0    # ai bull shit
            self.health = 130   # ha oh man that's a nasty fight lol
            self.healthmax = 130
            self.dead = 0
            self.dx = 0.0
            self.attackright = 0
            self.attackleft = 0
            self.spawnedspecialnurse = 0
        elif type == 'robot':
            self.timer = 0
            self.image = self.orginalImage.subsurface((0, 0, 32, 32))
            self.health = 100
            self.healthmax = 100
        elif type == 'backup':
            self.walktimer = 0
            self.dy = 0.0
            self.timer = 0
            self.image = self.orginalImage.subsurface((0, 0, 32, 32))
            self.health = 100
            self.healthmax = 100
            self.dead = 0
        elif type == 'boat':
            self.image = self.orginalImage.subsurface((0, 0, 64, 32))
        else:
            self.image = self.orginalImage.subsurface((0, 0, 32, 32))
        Sprite.__init__(self, self.image, Rect(0,0,32,32))
        self.type = type
        if type == 'fox':
            self.rect.width = 96
            self.rect.height = 64
        elif type == 'doctor':
            self.rect.width = 256
            self.rect.height = 256
        elif type == 'boat':
            self.rect.width = 32
            self.rect.height = 64
        self.dontwalk = 0
        g.sprites.append(self)
        g.removeOnLeave.append(self)
        self.groups = g.string2groups('character')
        self.g = g
        self.direction = 1

    # get the current image avatar.
    def getAvatar(self):
        if self.type == 'robot':
            if self.feeling == 'arms':
                return self.orginalAvatar.subsurface((64, 0, 64, 64))
            return self.orginalAvatar.subsurface((0, 0, 64, 64))
        elif self.type == 'nurse':
            if self.feeling == 'dead':
                return self.orginalAvatar.subsurface((64, 0, 64, 64))
            return self.orginalAvatar.subsurface((0, 0, 64, 64))
        elif self.type == 'backup':
            return self.orginalAvatar.subsurface((0, 0, 64, 64))

        if self.feeling == 'normal' or self.type == 'director':
            return self.orginalAvatar.subsurface((0, 0, 64, 64))
        elif self.feeling == 'sad':
            return self.orginalAvatar.subsurface((64, 0, 64, 64))
        elif self.feeling == 'happy':
            return self.orginalAvatar.subsurface((128, 0, 64, 64))
        elif self.feeling == 'coma':
            return self.orginalAvatar.subsurface((128, 0, 64, 64))
        return self.orginalAvatar.subsurface((192, 0, 64, 64))

    # upon each loop
    def loop(self, g, r):
        enableflip = 1
        # reseting the frame count if not walking
        if self.walking == 0:
            self.framecount = 0
            
        # animation
        if self.type == None: # assistant ima
            self.image = self.orginalImage.subsurface((32 * ((self.framecount/2) % 4), 0, 32, 32))
            # hack! to get ima the only holding hand character
            if g.connected == 1 and self.direction == 0 and self.orginalImage.get_size() == (256, 128):
                self.image = self.orginalImage.subsurface((32 * ((self.framecount/2) % 4), 64, 32, 32))
            if self.faceup == 1:
                self.image = self.orginalImage.subsurface((32 * 4, 0, 32, 32))
            elif self.feeling == 'worried':
                self.image = self.orginalImage.subsurface((32 * 5, 0, 32, 32))
            elif self.feeling == 'pulled':
                self.image = self.orginalImage.subsurface((32 * 6, 0, 32, 32))
            elif self.feeling == 'coma':
                self.image = self.orginalImage.subsurface((32 * 7, 0, 32, 32))
        elif self.type == 'director':# director victora
            self.image = self.orginalImage.subsurface((32 * ((self.framecount/2) % 5), 0, 32, 32))
            if self.feeling == 'sit':
                self.image = self.orginalImage.subsurface((32 * 5, 0, 32, 32))
            elif self.feeling == 'sitangry':
                self.image = self.orginalImage.subsurface((32 * 6, 0, 32, 32))
            elif self.feeling == 'sitawake':
                self.image = self.orginalImage.subsurface((32 * 7, 0, 32, 32))
        elif self.type == 'robot':# robot 0
            self.image = self.orginalImage.subsurface((0, 0, 32, 32))
            if self.feeling == 'blink':
                self.image = self.orginalImage.subsurface((32, 0, 32, 32))
            elif self.feeling == 'happy':
                self.image = self.orginalImage.subsurface((64, 0, 32, 32))
            elif self.feeling == 'arms':
                self.image = self.orginalImage.subsurface((96, 0, 32, 32))
            elif self.feeling == 'attack':
                self.image = self.orginalImage.subsurface((96, 0, 32, 32))
            elif self.feeling == 'dead':
                self.image = self.orginalImage.subsurface((96, 32, 32, 32))
        elif self.type == 'mushroom':# mushroom king
            if self.dead:
                self.image = pygame.Surface((1, 1), SRCALPHA)
                return
            enableflip = 0
            self.timer += 1
            self.image = self.orginalImage.subsurface((256, 256, 256, 256))
            if self.feeling == 'walking':
                m = (self.timer / 3) % 3
                if m == 0:
                    self.image = self.orginalImage.subsurface((0, 0, 256, 256))
                elif m == 1:
                    self.image = self.orginalImage.subsurface((256, 0, 256, 256))
                elif m == 2:
                    self.image = self.orginalImage.subsurface((0, 256, 256, 256))
        elif self.type == 'doctor':# doctor robot
            if self.dead:
                self.image = pygame.Surface((1, 1), SRCALPHA)
                return
            self.image = pygame.Surface((256, 256), SRCALPHA)
            enableflip = 0
            self.timer += 1

            leftarmlength = self.attackleft
            rightarmlength = self.attackright
            rightarmspnning = 0
            if rightarmlength == 10:
                rightarmspnning = ((self.timer % 1000) - 600) / 40 + 1
            dead = 0
            if self.health <= 0:
                leftarmlength = 0
                rightarmlength = 0
                self.feeling = 'dead'
                self.image.blit(self.imagel, (0,0))
                dead = 1
            else:
                self.image.blit(self.imageh, (0,0))
            if self.feeling == 'walking':
                m = (self.timer / 2) % 2 == 0
                if m == 1:
                    self.image.blit(self.imagee, (0,0)) # wonky tracks 2
                else:
                    self.image.blit(self.imagef, (0,0)) # wonky tracks 1
            else:
                self.image.blit(self.imageg, (0,0)) # normal tracks

            # getting hit by a bullet
            s = Rect(self.rect)
            s.x += 50
            s.y += 40
            s.width -= 120
            s.height -= 140
            for b in g.bullets:
                if b.owner == 'player':
                    drect = (b.rect.x , b.rect.y )
                    if s.collidepoint(drect) and not dead and rightarmspnning == 0:
                        dmg = b.get_damage()
                        self.health -= dmg
                        e = Effect(self.g, 'health', (self.rect.x + 128, self.rect.y + 60))
                        e.healthchange = -dmg
                        self.hitme.play()
                        self.image.blit(self.imagek, (0,0)) # white flash hit
                        b.destroy()
                        if self.health <= 0:
                            self.timer = 0

            # blit the right arm
            if rightarmspnning == 0:
                if rightarmlength == 4 or leftarmlength == 4:
                    self.attack.play()
                if rightarmlength == 0 or rightarmlength == 2:
                    self.image.blit(self.imagec, (0,0))
                elif rightarmlength == 1 or rightarmlength == 3:
                    self.image.blit(self.imagei, (0,0))
                else:
                    self.image.blit(self.imagec, (0,(rightarmlength - 4) * 20))
                if rightarmlength >= 0 and rightarmlength <= 3:
                    rpos = (0,0)
                    armr = self.imagea
                elif rightarmlength == 4:
                    rpos = (-50,-65)
                    armr = pygame.transform.rotate(self.imagea, -27)
                elif rightarmlength == 5: # there's no way to rotate around a point in pygame.
                    rpos = (-55,-90)
                    armr = pygame.transform.rotate(self.imagea, -45)
                else: # there's no way to rotate around a point in pygame.
                    rpos = (-55,-90)
                    armr = pygame.transform.rotate(self.imagea, -50)
                self.image.blit(armr, rpos)
            else:
                # covering the cross from player fire
                if rightarmspnning == 1 or rightarmspnning >= 9:
                    armrd = pygame.transform.rotate(self.imagea, -10)
                    armrc = pygame.transform.rotate(self.imagec, -25)
                    self.image.blit(armrd, (-30, -25))
                    self.image.blit(armrc, (-60,-75))
                else:
                    armrd = pygame.transform.rotate(self.imagea, -20)
                    armrc = pygame.transform.rotate(self.imagec, -50)
                    self.image.blit(armrd, (-40, -50))
                    self.image.blit(armrc, (-80,-130))

            # blit the left arm
            if leftarmlength == 0 or leftarmlength == 2:
                self.image.blit(self.imaged, (0,0))
            elif leftarmlength == 1 or leftarmlength == 3:
                self.image.blit(self.imagej, (0,0))
            else:
                self.image.blit(self.imaged, (0,(leftarmlength - 4) * 18))
            if leftarmlength >= 0 and leftarmlength <= 3:
                rpos = (0,0)
                arml = self.imageb
            elif leftarmlength == 4:
                rpos = (-35,-60)
                arml = pygame.transform.rotate(self.imageb, 27)
            elif leftarmlength == 5:
                rpos = (-40,-80)
                arml = pygame.transform.rotate(self.imageb, 45)
            else:
                rpos = (-40,-80)
                arml = pygame.transform.rotate(self.imageb, 50)
            self.image.blit(arml, rpos)
            if self.attackright > 0:
                self.attackright += 1
                if self.attackright > 7:
                    self.attackright = 0
            if self.attackleft > 0:
                self.attackleft += 1
                if self.attackleft > 7:
                    self.attackleft = 0
        elif self.type == 'nurse': # the devil child of the doctor. special nurse
            if self.feeling == 'dead':
                self.image = self.orginalImage.subsurface((5 * 32, 0, 32, 32))
            else:
                self.image = self.orginalImage.subsurface((0, 0, 32, 32))
        elif self.type == 'fox':
            if self.lastframehidden != self.hidden and self.lastframehidden != -1:
                print 'out of frame animation effect'
                Effect(g, 'foxentrance', (self.rect.x + 32, self.rect.y + 8))
                self.teleport.play()
            self.lastframehidden = self.hidden
            if self.jumping:
                self.image = self.orginalImage.subsurface((96, 0, 96, 64))
            elif self.walking:
                self.image = self.orginalImage.subsurface((96 * ((self.framecount/3) % 2), 64, 96, 64))
            else:
                self.image = self.orginalImage.subsurface((0, 0, 96, 64))
                if self.feeling == 'sad':
                    self.image = self.orginalImage.subsurface((0, 128, 96, 64))
                elif self.feeling == 'shooting':
                    self.image = self.orginalImage.subsurface((96, 128, 96, 64))
                elif self.feeling == 'dead':
                    self.image = self.orginalImage.subsurface((96, 192, 96, 64))
                    
            if self.faceup == 1:
                self.image = self.orginalImage.subsurface((0, 192, 96, 64))
        elif self.type == 'backup':
            self.image = self.orginalImage.subsurface((0, 0, 32, 32))
            if self.dead:
                self.image = self.orginalImage.subsurface((196, 0, 32, 32))
        elif self.type == 'boat':
            return

        # if you look the way you are facing
        if enableflip:
            self.image = pygame.transform.flip(self.image, self.direction, 0)


        # AI Mode has been activated
        if self.attacking != 0:
            if self.type == 'mushroom':# robot 0
                self.mushroom_attack_loop()
            elif self.type == 'doctor':
                self.doctor_attack_loop()
            elif self.type == 'robot':
                self.robot_attack_loop()
            elif self.type == 'backup':
                self.backup_attack_loop()
            else:
                self.fox_attack_loop()
            return

        if self.dontwalk:
            return



        
        # if you're walking to a position
        p = (self.rect.x, self.rect.y)
        self.walking = 0
        if p != self.walktopos and self.walktopos != None:
            self.walking = 1
            self.framecount += 1
            if p[0] > self.walktopos[0] + self.walkspeed:
                self.rect.x -= self.walkspeed
            elif p[0] < self.walktopos[0] - self.walkspeed:
                self.rect.x += self.walkspeed
            else:
                self.rect.x = self.walktopos[0]
            if p[1] > self.walktopos[1] + self.walkspeed:
                self.rect.y -= self.walkspeed
            elif p[1] < self.walktopos[1] - self.walkspeed:
                self.rect.y += self.walkspeed
            else:
                self.rect.y = self.walktopos[1]

        if self.hidden == 1:
            self.image = self.orginalImage.subsurface((0, 0, 0, 0))

    def rotPoint(self, point, axis, ang):
        """ Orbit. calcs the new loc for a point that rotates a given num of degrees around an axis point,
            +clockwise, -anticlockwise -> tuple x,y
        """
        x, y = point[0] - axis[0], point[1] - axis[1]
        radius = math.sqrt(x*x + y*y) # get the distance between points

        RAng = math.radians(ang)       # convert ang to radians.

        h = axis[0] + ( radius * math.cos(RAng) )
        v = axis[1] + ( radius * math.sin(RAng) )

        return h, v



    # put the character on the tile
    def pos(self, p):
        g = self.g
        pos = g.tile_to_screen((p[0], p[1]))
        w,h = g.size
        if p[0] <= w and p[1] <= h:
            self.walktopos = (pos[0] + g.view.x, pos[1] + g.view.y)
            self.rect.x,self.rect.y = self.walktopos
            self._rect.x,self._rect.y = self.walktopos
        else:
            print 'position set out of bounds',pos

    # will walk the character to a position
    def walkto(self, p):
        if p == None:
            self.walktopos = None
            return
        self.following = None
        g = self.g
        pos = g.tile_to_screen((p[0], p[1]))
        self.walktopos = (pos[0] + g.view.x, pos[1] + g.view.y)

    # gets the current characters position
    def get_pos(self):
        curpos = (self.rect.x + self.rect.width / 2 -  self.g.view.x, \
                self.rect.y +  self.rect.height / 2 -  self.g.view.y)
        return self.g.screen_to_tile(curpos)

    # where the character is
    def hasWalkedTo(self, p = (0,0)):
        w,h = self.g.screen_to_tile((self.rect.x - self.g.view.x, self.rect.y - self.g.view.y))
        if p == (w,h) or p == (0,0):
            return not self.walking
        return 0

    # walk to a rect pos
    def walktorect(self, r):
        self.walktopos = (r[0], r[1])

    def rebound(self, n):
        if self.type == 'fox':
            if self.jumpvec > 8:
                self.jumping = 0
            # change direction
            if self.attacking == 1:
                if n == 2 or n == 3:
                    print 'rebound n = ', n
                    self.direction = 1
                    if self.rect.x < self.g.player.rect.x:
                        self.direction = 0
                
        elif self.type == 'mushroom':
            if n == 2 or n == 3:
                self.direction = not self.direction
        elif self.type == 'doctor':
            self.dx = -self.dx
        elif self.type == 'robot':
            self.attacking = 1
            self.face_the_player()
        elif self.type == 'backup':
            if n == 2 or n == 3:
                self.face_the_player()


    def backup_attack_loop(self):
        g = self.g
        self.image = self.orginalImage.subsurface((160, 0, 32, 32))

        speed = self.walktimer
        self.walktimer += 1
        if self.walktimer > 6:
            self.walktimer = 6


        self.timer += 1
        timergate = self.timer % 100
        if timergate >= 80:
            if timergate == 80:
                self.face_the_player()
            if timergate == 85:
                Shot(g, self.direction, (self.rect.x + 16, self.rect.y + 8), 'shot8', 'enemy')
            self.walking = 0
        else:
            self.walking = 1
        if timergate % 100 == 0:
            self.face_the_player()

        dx = self.rect.x - g.player.rect.x
        if dx <40 and dx > -40:
            if self.dy == 10.0:
                self.dy = -10.0

        if self.walking:
            self.rect.x += (1 - (self.direction * 2)) * speed
            framen = self.timer / 2  % 3
            self.image = self.orginalImage.subsurface((32 + framen * 32, 0, 32, 32))
        else:
            self.walktimer = 0

        self.dy += .5
        if self.dy > 10.0:
            self.dy = 10.0
        self.rect.y += self.dy

        if self.rect.x < 416:
            self.direction = 0

        
        self.image = pygame.transform.flip(self.image, self.direction, 0)
        # hitting the bullets and player
        s = Rect(self.rect)
        if s.colliderect (g.player.rect):
            g.player.touch(self)
        for b in g.bullets:
            if b.owner == 'player':
                drect = (b.rect.x + 30, b.rect.y )
                if s.collidepoint(drect):
                    b.destroy()
                    self.health -= b.get_damage()
                    e = Effect(self.g, 'health', (self.rect.x, self.rect.y))
                    e.healthchange = -b.get_damage()
                    self.image = g.make_image_white(self.image)




    # loop function for the fox attack. walks back and forth,
    # and fires at the player when it reaches the end
    def fox_attack_loop(self):
        g = self.g

        if self.health <= 0:
            self.feeling = 'sad'
            self.health = 0
            if self.attacking == 3:
                self.feeling = 'dead'
                self.rect.y += 3
            else:
                self.attacking = 0
            self.walking = 0
            self.jumping = 0
            self.walktopos = (self.rect.x, self.rect.y)
            return
        
        self.timer += 1

        if self.jumping == 1:
            self.rect.y += self.jumpvec
            self.jumpvec += 1

        # if timer is in the minus, you're firing for a while
        if self.timer < 0:
            self.walking = 0
            if self.timer < -10:
                self.feeling = 'shooting'
                if self.attacking == 1:# first battle
                    if self.timer % 2 == 0:
                        s = Shot(g, self.direction, (self.rect.x + 44, self.rect.y + 35), 'shot3', 'enemy')
                elif self.attacking == 2: # second battle
                    if self.timer % 4 == 0:
                        s = Shot(g, self.direction, (self.rect.x + 44, self.rect.y + 35), 'shot3', 'enemy')
                        s.keep_alive = 6
                elif self.attacking == 3: # last
                    if self.timer % 10 == 0:
                        s = Shot(g, self.direction, (self.rect.x + 44, self.rect.y + 35), 'shot8', 'enemy')
        else:
            self.feeling = 'normal'
            speed = 4
            if self.attacking == 2:
                speed = 5
            self.rect.x += (1 - (self.direction * 2)) * speed
            self.rect.y += 2 # gravity
            if self.walktopos == (self.rect.x, self.rect.y) : # walking into something
                self.jumping = 1
                self.jumpvec = -10
            if self.attacking == 1: # first battle with fox
                if self.timer == 2:
                    self.jumping = 1
                    self.jumpvec = -10
                # shooting every random interval
                if random.randint(0, 70) == 0 and self.framecount > 10:
                    self.timer = -30
            if self.attacking == 2 or self.attacking == 3: # second battle with Fox
                dv = self.rect.x - self.g.player.rect.x
                if dv > 200:
                    self.direction = 1
                if dv < -200:
                    self.direction = 0
                if self.jumping == 0:
                    # jumping every 30 frames
                    if self.framecount % 40 == 0 and self.jumping == 0:
                        self.jumping = 1
                        self.jumpvec = -10
                        if self.attacking == 3:
                            self.jumpvec = -15
                    # shooting every random interval
                    elif random.randint(0, 15) == 0 and self.framecount > 10:
                        self.timer = -30
            self.framecount += 1
            self.walking = 1
            self.walktopos = (self.rect.x, self.rect.y)
        
        # hitting the bullets and player
        s = Rect(self.rect)
        if s.colliderect (g.player.rect):
            g.player.touch(self)
        for b in g.bullets:
            if b.owner == 'player':
                drect = (b.rect.x + 30, b.rect.y )
                if s.collidepoint(drect):
                    b.destroy()
                    self.health -= b.get_damage()
                    e = Effect(self.g, 'health', (self.rect.x, self.rect.y))
                    e.healthchange = -b.get_damage()
                    if self.feeling != 'sad':
                        self.hitme.play()
                    self.feeling = 'sad'
                    self.image = g.make_image_white(self.image, (96, 64))

    # creates a slime monster at this location
    def create_slime_monster(self, r):
        #Enemy(self.g, (r[0], r[1] - r[1] % 32 + 16), 'monster2')
        Monster2(self.g, (r[0], r[1] - r[1] % 32 + 16))
        self.squirt.play()

    # creates a nurse monster
    def create_nurse_monster(self, r):
        #Enemy(self.g, (r[0] - 16, r[1] - r[1] % 32), 'nurse')
        Nurse(self.g, (r[0] - 16, r[1] - r[1] % 32))

    # will make the direction of the object face the player
    def face_the_player(self):
        self.direction = 1
        if self.rect.x < self.g.player.rect.x:
            self.direction = 0

    # attacking the player
    def robot_attack_loop(self):
        g = self.g
        self.timer += 1
        speed = 9
        attackphase = self.timer % 70
        self.image = self.orginalImage.subsurface((0, 32, 32, 32))
        if attackphase == 1: # lunge at the player
            self.face_the_player()
            self.attacking = 2 # 2 = lunging
        elif attackphase == 50: # fire a ball of death at the player
            Shot(self.g, self.direction, (self.rect.x + 16, self.rect.y + 20), 'shot8', 'enemy')
        if attackphase >= 50 and attackphase <= 65: # fire a ball of death at the player
            self.image = self.orginalImage.subsurface((64, 32, 32, 32))

        # lunging
        if self.attacking == 2:
            self.image = self.orginalImage.subsurface((32, 32, 32, 32))
            if self.rect.colliderect (self.g.player.rect):
                self.g.player.touch(self)
            self.rect.x += speed
            if self.direction:
                self.rect.x -= speed*2

        # loop through bullets and see if I die
        for b in g.bullets:
            if b.owner == 'player':
                drect = (b.rect.x + 30, b.rect.y )
                if self.rect.collidepoint(drect):
                    b.destroy()
                    self.health -= b.get_damage()
                    e = Effect(self.g, 'health', (self.rect.x, self.rect.y))
                    e.healthchange = -b.get_damage()
                    self.image = g.make_image_white(self.image, (32, 32))
        self.image = pygame.transform.flip(self.image, not self.direction, 0)

        if self.health <= 0:
            self.feeling = 'dead'
            self.attacking = 0
            self.dontwalk = 1



    # creates a nurse character
    def create_nurse_character(self, r):
        c = Character("monster4.png", "facenurse.png", self.g, 'nurse')
        c.feeling = 'dead' # lol feeling dead?
        mpos = self.g.screen_to_tile((r[0] - self.g.view.x, r[1] - self.g.view.y - 8))
        c.pos(mpos)
        self.g.level.nurse = c
        print 'create character nurse', mpos

    # boss doctor fight
    def doctor_attack_loop(self):
        speed = 6
        self.feeling = 'walking'
        g = self.g

        if self.health <= 0:
            #destoryed walking too 813
            targntx = self.rect.x
            if targntx > 813 + speed * 2: # walked too far left left
                self.dx -= .5
                if self.dx < -speed:
                    self.dx = -speed
                self.rect.x += int(self.dx)
                self.timer = self.timer % 10
            elif targntx < 813 - speed * 2:# walked too far right
                self.dx += .5
                if self.dx > speed:
                    self.dx = speed
                self.rect.x += int(self.dx)
                self.timer = self.timer % 10
            else:
                if self.spawnedspecialnurse == 0:
                    print 'spawn special nurse'
                    self.spawnedspecialnurse = 1
                    s = Shot(self.g, self.direction, (self.rect.x + 128, self.rect.y + 80 ), 'shot6', 'enemy')
                    s.callback = self.create_nurse_character
                    s.xvel = 0
            if self.timer < 70:
                if self.timer % 3 == 0:
                    # flash on and off
                    self.image = pygame.Surface((1, 1), SRCALPHA)
                else:
                    x = random.randint(0, 256)
                    y = random.randint(0, 256)
                    Effect(self.g, 'explosion', (self.rect.x + x, self.rect.y + y))
            return
        #self.timer += 1
        dx = (self.rect.x + self.rect.width/2) - g.player.rect.x
        dy = (self.rect.y + self.rect.height) - g.player.rect.y
        pdrect = 100
        if self.timer % 1000 > 400:
            pdrect = 400
            if self.dx < 0 and self.dx > -speed:
                self.dx += -.5
            if self.dx > 0 and self.dx < speed:
                self.dx += .5
        if dx > pdrect: # walked too far left left
            self.dx -= .5
            if self.dx < -speed:
                self.dx = -speed
        elif dx < -pdrect:# walked too far right
            self.dx += .5
            if self.dx > speed:
                self.dx = speed

        # attck with arms
        if dx > 70 and dx < 140:
            if dy <50 and dy > 0:
                if self.attackleft == 0:
                    self.attackleft = 1
                if self.attackleft == 5:
                    g.player.touch(self)
        # attack with the right arm
        if dx < -70 and dx > -140:
            if dy <50 and dy > 0:
                if self.attackright == 0:
                    self.attackright = 1
                if self.attackright == 5:
                    g.player.touch(self)
        # scratching self to stop continius shooting
        if self.timer % 1000 > 600:
            self.attackright = 10
        # tracks hittin the player
        #if dx > -40 and dx < 40:
        #    if dy < 40 and dy > 0:
        #        g.player.touch(self)
        # like the monotane, it shits out little babies
        if self.timer % 20 == 1:
            if self.timer % 400 < 200:
                c = random.randint(0, 20)
                s = Shot(self.g, self.direction, (self.rect.x + 128, self.rect.y + 80 + c), 'shot6', 'enemy')
                s.callback = self.create_nurse_monster
                self.squirt.play()


        self.rect.x += int(self.dx)
        self.draw_health_meter()



    # boss fight
    def mushroom_attack_loop(self):
        g = self.g
        if self.health <= 0:
            if self.feeling != 'dead':
                self.feeling = 'dead'
                self.timer = 0
                
        if self.feeling == 'dead':
            if self.timer > 70:
                self.image = pygame.Surface((1, 1), SRCALPHA)
                self.dead = 1
                return
            if self.timer % 10 == 0:
                self.exp2.play()
            if self.timer % 3 == 0:
                # flash on and off
                self.image = pygame.Surface((1, 1), SRCALPHA)
            else:
                x = random.randint(0, 256)
                y = random.randint(0, 256)
                e = Effect(self.g, 'explosion', (self.rect.x + x, self.rect.y + y))
            return


        if self.timer % 20 == 1:
            if self.timer % 200 < 100:
                c = random.randint(0, 20)
                s = Shot(self.g, self.direction, (self.rect.x + 128, self.rect.y + 128 + c), 'shot5', 'enemy')
                s.callback = self.create_slime_monster
                self.squirt2.play()

        s = Rect(self.rect)
        s.x += 80
        s.width -= 100
        s.y += 100
        s.height -= 180
        if s.colliderect (g.player.rect):
            g.player.touch(self)

        for b in g.bullets:
            if b.owner == 'player':
                drect = (b.rect.x + 30, b.rect.y )
                if s.collidepoint(drect):
                    b.destroy()
                    self.health -= b.get_damage()
                    e = Effect(self.g, 'health', (self.rect.x, self.rect.y))
                    e.healthchange = -b.get_damage()
                    tmp = pygame.Surface((256, 256), SRCALPHA)
                    tmp.blit(self.image, (0,0))
                    tmp.blit(self.secondImage, (0,0))
                    self.image = tmp
                    self.hitme.play()
                    
        speed = 2
        self.rect.x += (1 - (self.direction * 2)) * speed
        self.draw_health_meter()




    # if this character is an enemy
    def get_damage(self):
        return 1

    # draws a meter of the character. used during boss battles 
    def draw_health_meter(self):
        self.g.drawhealth = self.health
        self.g.healthmax = self.healthmax

    # fox jumps out of the picture
    def jump_out(self):
        self.walktopos = (self.rect.x, self.rect.y - 1000)
        self.jumping = 1


        