""" Level base class """
import random
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from character import Character
from inventory import Inventory
#from enemies.enemy import Enemy
from enemies.bugs import Bugs
from enemies.drip import Drip
import sys; sys.path.insert(0, "..")
from pgu import vid



class LevelBase:
    cdata = {}
    edata = {}
    tdata = {}
    switches = []
    dimentions = 0,0
    oldPos = 0,0
    dialog = 0
    moveCamera = None
    contains_msg_box = 0
    contains_msg_box_counter = 0
    info_box_str = None
    info_box_character = None
    bgimage = None
    inventory_gui = 0
    weapon_gui = 0
    select_gui = 0
    option_gui = 0
    effect = None

    # effects
    effect_wind = 0

    def __init__(self, g, player_new, dimentions):
        self.g = g
        self.dimentions = dimentions

        # text sounds
        textblip = os.path.join("effects",  "text.wav")
        self.text_blip = pygame.mixer.Sound(textblip)
        g.tmpPlayerPos = None
        self.switches = []
        self.sprinklers = []
        
        # collision data
        self.edata = {
            0x01:('player', self.hittest_level),
            0x03:('player', self.change_level),
            0x07:('player', self.hittest_level_half),
            0x0B:('player', self.walk_snow)
            }

        # texture data
        self.tdata = { }

        # init code data
        self.cdata = {
            0x02:(player_new, None),
            0x04:(self.playerMove, None),
            0x05:(self.add_monster, None),
            0x06:(self.add_save_inventory, None),
            0x08:(self.add_health_increase, None),
            0x09:(self.add_spike, None),
            0x0A:(self.add_switch, None),
            0x0C:(self.add_health, None),
            0x0D:(self.add_water, None),
            0x0E:(self.add_shot3, None), # lol
            0x0F:(self.add_bugs, None),
            0x10:(self.add_drip, None),
            0x12:(self.add_special_spike, None)
            }

        g.connected = 0
        g.following = None
        self.draw_timer_gui = 0
        self.title = 'Unknown'

    # load the tiling image for the background
    def initBack(self, bgimage, backheight, width = 256):
        self.bgimage = bgimage
        self.backheight = backheight
        self.backwidth = width
        if bgimage != None:
            g = self.g
            img = pygame.image.load(os.path.join("textures",  bgimage)).convert_alpha()
            bks = g.bounds.width / width
            for m in range(bks + 1):
                g.backsprites.append(vid.Sprite(img, Rect(m * width,0,32,32)))
            LevelBase.draw_back(self)

            
    # creates a monster at a position
    def add_monster(self, g,r,a):
        pass

    # Changes the level to a new level
    def change_level(self, g,r,a):
        pass

    # add some bugs that fly around
    def add_bugs(self, g, r, a):
        mbugs = random.randint(0, 3)
        for i in range(mbugs):
            #Enemy(self.g,(r.rect.x, r.rect.y), 'bugs')
            Bugs(self.g,(r.rect.x, r.rect.y))

    # add a drip that makes a dripping.. sound? i don't know.
    def add_drip(self, g, r, a):
        #Enemy(self.g,(r.rect.x, r.rect.y), 'drip')
        Drip(self.g,(r.rect.x, r.rect.y))

    # a spike that takes 21 off health
    def add_special_spike(self, g, r, a):
        spike = Inventory(self.g, 'aspike')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        spike.pos(pos)
        
    # add a water sprinkler
    def add_water(self, g,r,a):
        sprinkler = Inventory(self.g, 'sprinkler')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        sprinkler.pos(pos)
        self.sprinklers.append(sprinkler)

    def add_health(self, g,r,a):
        save = Inventory(self.g, 'health')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        save.pos(pos)

    def add_shot3(self, g,r,a):
        shot4 = Inventory(self.g, 'shot4')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        shot4.pos(pos)

    # walking on a snow area
    def walk_snow(self, g,r,a):
        g.player.snowwalk = 1

    # Creates a save icon
    def add_save_inventory (self,g,r,a):
        save = Inventory(self.g, 'save')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        save.pos(pos)

    def hittest_level(self,g,r,a):
        """ called when hitting a wall

        """
        h = 0
        if (a._rect.bottom <= r.top and a.rect.bottom > r.top):
            a.rect.bottom = r.top
            h = 1
            if a.__class__.__name__ == 'Player':
                g.player.hit_ground()
                g.player.gravity = 0
                g.player.canjump = 1
        if (a._rect.right <= r.left and a.rect.right > r.left):
            a.rect.right = r.left
            h = 2
        if (a._rect.left >= r.right and a.rect.left < r.right):
            a.rect.left = r.right
            h = 3
        if (a._rect.top >= r.bottom and a.rect.top < r.bottom):
            a.rect.top = r.bottom
            h = 4
            if a.__class__.__name__ == 'Player':
                if g.player.gravity != 0:
                    g.player.hitSound.play()
                g.player.gravity = 0
        if h:
            a.rebound(h)

    def hittest_level_half(self,g,r,a):
        """ half block 16 pixels lower
        """

        inside = 0
        s = 0
        h = 0
        if a.rect.bottom - 16 > r.top and a.rect.top - 16 < r.bottom:
            inside = 1
        if (a._rect.bottom - 16 <= r.top and a.rect.bottom - 16 > r.top):
            a.rect.bottom = r.top + 16
            s = 1
            h = 1
            if a.__class__.__name__ == 'Player':
                g.player.hit_ground()
                g.player.gravity = 0
                g.player.canjump = 1

        if (a._rect.top - 16 >= r.bottom and a.rect.top - 16 < r.bottom):
            a.rect.top = r.bottom + 16
            s = 1
            h = 2
            if a.__class__.__name__ == 'Player':
                if g.player.gravity != 0:
                    g.player.hitSound.play()
                g.player.gravity = 0
        if (a._rect.right <= r.left and a.rect.right > r.left and inside):
            a.rect.right = r.left
            s = 1
            h = 3
        if (a._rect.left >= r.right and a.rect.left < r.right and inside):
            a.rect.left = r.right
            s = 1
            h = 4
        if h:
            a.rebound(h)
        # if it's a weapon shot
        if a.__class__.__name__ == 'Shot' and s:
            a.destroy()

    # tile block
    def tile_block(self,g,t,a):
        """ When the user hits a tile

        """
        pass

    # when the player leaves this level
    def leave(self):
        """ upon leaving this level

        """
        for b in self.g.removeOnLeave:
            if b in self.g.sprites:
                self.g.sprites.remove(b)
        self.g.removeOnLeave = []
        for n in self.g.backsprites:
            self.g.backsprites.remove(n)
            del self.g.backsprites[:]
        pygame.mixer.music.stop()

    # display an information block to the user
    def info_box(self, str, character = 0):
        """ Draws a box that contains a string for the user to read

        """
        self.info_box_str = str
        self.info_box_character = character

    def draw_gui(self):
        """ Will draw all the over layed objects on screen
        """
        g = self.g


        # GUI text box. May contain a avatar of the character talking
        if self.info_box_str != None:
            mstr = self.info_box_str
            character = self.info_box_character
            n = self.contains_msg_box_counter * 4
            if n < len(mstr):
                mstr = mstr[:n]
                self.text_blip.set_volume(.2)
                self.text_blip.play(2)
            txtx = 25
            SW,SH = self.dimentions
            # draw bg
            self.g.screen.fill((0,0,0,100), (20, SH-90, SW-40, 75))
            if isinstance(character, Character):
                img = character.getAvatar()
                self.g.screen.blit(img,(25,SH-85))
                txtx = 100
            self.g.infobox = 1

            n = mstr.split("\n")
            v = 0
            pygame.draw.rect(self.g.screen, (55,55,55), (20, SH-90, SW-40, 75), 3)
            for s in n:
                img = self.g.font.render(s,0,(255,255,255))
                self.g.screen.blit(img,(txtx,SH-85 + v))
                v += 20
            self.contains_msg_box = 1

        # player GUI
        if g.saveData['displayhealth'] == 1:
            # health meter
            healthamount = g.player.health
            if healthamount < 0:
                healthamount = 0
            g.screen.blit(g.images['inventory'][0].subsurface((2 * 32, 0, 32, 32)), (15, 10))
            pygame.draw.rect(g.screen, (255,255,255), Rect(55,15,90,18))
            pygame.draw.rect(g.screen, (60,1,1), Rect(57,17,86,14))
            pygame.draw.rect(g.screen, (180,1,1), Rect(57,17,86.0* float(healthamount) / float(g.player.healthmax),14))
            # shadow the real text
            img = g.font.render(str(g.player.health)+ ' / ' + str(g.player.healthmax),0,(0,0,0))
            g.screen.blit(img,(152, 9))
            img = g.font.render(str(g.player.health)+ ' / ' + str(g.player.healthmax),0,(255,255,255))
            g.screen.blit(img,(150, 7))

            # depending on the weapon selected, draw the icon
            if g.saveData['weapon'] != 0:
                if g.saveData['weapon'] == 1:
                    g.screen.blit(g.images['inventory'][0].subsurface((0, 4 *32, 32, 32)), (15, 35 - 6))
                elif g.saveData['weapon'] == 2:
                    g.screen.blit(g.images['inventory'][0].subsurface((3 * 32, 2 *32, 32, 32)), (15, 35 - 6))
                elif g.saveData['weapon'] == 3:
                    g.screen.blit(g.images['inventory'][0].subsurface((3 * 32, 5 *32, 32, 32)), (15, 35 - 6))
                elif g.saveData['weapon'] == 4:
                    g.screen.blit(g.images['inventory'][0].subsurface((5 * 32, 3 *32, 32, 32)), (12, 35 - 4))
                g.screen.blit(g.images['inventory'][0].subsurface((2 * 32, 2 *32, 32, 32)), (15, 35))
                if g.saveData['weapon'] > 1:
                    wpnstr = 'shot'+str(g.saveData['weapon'])+'_lvl'
                    g.screen.blit(g.images['inventory'][0].subsurface((2 * 32, 0, 32, 32)), (15, 10))
                    pygame.draw.rect(g.screen, (255,255,255), Rect(55,41,90,18))
                    pygame.draw.rect(g.screen, (60,1,1), Rect(57,43,86,14))
                    # level 1
                    skyberries = g.saveData[wpnstr]
                    lvl1,lvl2,lvl2 = skyberries,skyberries,skyberries
                    if skyberries > 10:
                        lvl1 = 10
                    pygame.draw.rect(g.screen, (68,78,30), Rect(57,43,86.0* float(lvl1) / 10.0,14))
                    # level 2
                    if skyberries > 10:
                        lvl2 = skyberries - 10
                        if lvl2 > 10: lvl2 = 10
                        pygame.draw.rect(g.screen, (129,147,56), Rect(57,43,86.0* float(lvl2) / 10.0,14))
                    # level 3 - max
                    if skyberries > 20:
                        lvl3 = skyberries - 20
                        if lvl3 > 10: lvl3 = 10
                        skyberries = g.saveData[wpnstr]
                        pygame.draw.rect(g.screen, (223,255,97), Rect(57,43,86.0* float(lvl3) / 10.0,14))

        # draw the boss GUI health bar
        if g.drawhealth != 0:
            SW,SH = g.view.w,g.view.h
            g.screen.blit(g.images['inventory'][0].subsurface((2 * 32, 0, 32, 32)), (30, SW - 20))
            pygame.draw.rect(g.screen, (255,255,255), Rect(55,SH - 22,SW - 100,18))
            pygame.draw.rect(g.screen, (60,1,1), Rect(57,SH - 20,SW - 104 ,14))
            pygame.draw.rect(g.screen, (180,1,1), Rect(57,SH - 20,(SW - 104)* float(g.drawhealth) / float(g.healthmax),14))
            img = g.font.render(str(g.drawhealth),0,(255,255,255))
            g.screen.blit(img,(25, SH - 30))
            g.drawhealth = 0

        # draw the inventory list
        if self.inventory_gui != 0:
            g.disable_fire = 1
            self.weapon_gui = 0
            w,h = 350, 100
            SW,SH = g.view.w,g.view.h
            pygame.draw.rect(g.screen, (255,255,255), Rect(SW/2-w/2,SH/2-h/2,w+4,h+4))
            pygame.draw.rect(g.screen, (60,1,1), Rect(SW/2+2-w/2,SH/2+2-h/2,w,h))
            
            inventorylist = []
            if 'displayhealth' in g.saveData:
                if g.saveData['displayhealth'] == 1:
                    a = ('An advanced weapon with four spirs', \
                        g.images['inventory'][0].subsurface((1 * 32, 0, 32, 32)))
                    inventorylist.append(a)
            if 'i_microwave' in g.saveData:
                if g.saveData['i_microwave'] == 1:
                    a = ('A transmitting device', \
                        g.images['inventory'][0].subsurface((0, 0, 32, 32)))
                    inventorylist.append(a)
            if 'i_arms' in g.saveData:
                if g.saveData['i_arms'] == 1:
                    a = ('A pair of robot arms', \
                        g.images['inventory'][0].subsurface((2 * 32, 4 * 32, 32, 32)))
                    inventorylist.append(a)
            if 'i_flutterbox' in g.saveData:
                if g.saveData['i_flutterbox'] == 1:
                    a = ('A flutterbox', \
                        g.images['inventory'][0].subsurface((7 * 32, 4 * 32, 32, 32)))
                    inventorylist.append(a)
            if 'i_locationcard' in g.saveData:
                if g.saveData['i_locationcard'] == 1:
                    a = ('A card that connects to a elevator', \
                        g.images['inventory'][0].subsurface((1 * 32, 5 * 32, 32, 32)))
                    inventorylist.append(a)
            if 'i_medicine' in g.saveData:
                if g.saveData['i_medicine'] == 1:
                    a = ('A spray type medicine for nurses', \
                        g.images['inventory'][0].subsurface((7 * 32, 6 * 32, 32, 32)))
                    inventorylist.append(a)
            if 'i_newspaper' in g.saveData:
                if g.saveData['i_newspaper'] == 1:
                    a = ('A newspaper from the past', \
                        g.images['inventory'][0].subsurface((0, 10*32, 32, 32)))
                    inventorylist.append(a)
            if 'i_coin' in g.saveData:
                if g.saveData['i_coin'] == 1:
                    a = ('Two gold coins', \
                        g.images['inventory'][0].subsurface((6*32, 10*32, 32, 32)))
                    inventorylist.append(a)
            if 'i_jailkey' in g.saveData:
                if g.saveData['i_jailkey'] == 1:
                    a = ('Key to the jail', \
                        g.images['inventory'][0].subsurface((5*32, 10*32, 32, 32)))
                    inventorylist.append(a)
            if 'i_tape' in g.saveData:
                if g.saveData['i_tape'] == 1:
                    a = ('Ima\'s backup tape', \
                        g.images['inventory'][0].subsurface((7*32, 10*32, 32, 32)))
                    inventorylist.append(a)

            selectedno = 0
            for i in inventorylist:
                selectedno += 1
                xpos = selectedno * 38
                pygame.draw.rect(g.screen, (0,0,0), Rect(120+xpos,200,32,32))
                if selectedno == self.inventory_gui:
                    pygame.draw.rect(g.screen, (255,255,255), Rect(120 + xpos, 200,36,36))
                    pygame.draw.rect(g.screen, (30,30,30), Rect(122 + xpos ,202,32,32))
                    img = g.font.render(i[0],0,(255,255,255))
                    g.screen.blit(img,(155, 250))
                img = i[1]
                g.screen.blit(img, (120 + xpos, 200))

            if self.inventory_gui > selectedno:
                self.inventory_gui = 0
            if self.inventory_gui < 0:
                self.inventory_gui = 1

            if self.select_gui != 0:
                self.inventory_gui = 0
                self.select_gui = 0



        # draw the weapon list
        if self.weapon_gui != 0 and g.saveData['weapon'] != 0:
            g.disable_fire = 1
            self.inventory_gui = 0
            w,h = 350, 100
            SW,SH = g.view.w,g.view.h
            pygame.draw.rect(g.screen, (255,255,255), Rect(SW/2-w/2,SH/2-h/2,w+4,h+4))
            pygame.draw.rect(g.screen, (60,1,1), Rect(SW/2+2-w/2,SH/2+2-h/2,w,h))

            inventorylist = []
            if 'weapon' in g.saveData:
                a = ('A basic shot', \
                    g.images['inventory'][0].subsurface((0, 4 *32, 32, 32)), \
                    1)
                inventorylist.append(a)
            if 'shot2' in g.saveData:
                if g.saveData['shot2'] >= 1:
                    a = ('A generic anti-bio shot. ' + str(g.saveData['shot2']) + ' remain.', \
                        g.images['inventory'][0].subsurface((3 * 32, 2 *32, 32, 32)), \
                        2)
                    inventorylist.append(a)
            if 'shot4' in g.saveData:
                if g.saveData['shot4'] >= 1:
                    a = ('A dark type shot. ' + str(g.saveData['shot4'])  + ' remain.', \
                        g.images['inventory'][0].subsurface((5 * 32, 3 *32, 32, 32)), \
                        4)
                    inventorylist.append(a)
            if 'shot7' in g.saveData:
                if g.saveData['shot7'] >= 1:
                    a = ('A electrical type shot. ' + str(g.saveData['shot7'])  + ' remain.', \
                        g.images['inventory'][0].subsurface((0, 7 *32, 32, 32)), \
                        7)
                    inventorylist.append(a)

            selectedno = 0
            selectedweaponnumber = 0
            for i in inventorylist:
                selectedno += 1
                xpos = selectedno * 38
                pygame.draw.rect(g.screen, (0,0,0), Rect(120+xpos,200,32,32))
                if selectedno == self.weapon_gui:
                    pygame.draw.rect(g.screen, (255,255,255), Rect(120 + xpos, 200,36,36))
                    pygame.draw.rect(g.screen, (30,30,30), Rect(122 + xpos ,202,32,32))
                    img = g.font.render(i[0],0,(255,255,255))
                    g.screen.blit(img,(155, 250))
                    selectedweaponnumber = i[2]
                img = i[1]
                g.screen.blit(img, (120 + xpos, 200))

            # closing the window
            if self.weapon_gui > selectedno:
                self.weapon_gui = 0
            if self.weapon_gui < 0:
                self.weapon_gui = 1

            # selecting a different weapon
            if self.select_gui != 0:
                print 'self.select_gui=',self.select_gui, g.saveData['weapon'],selectedweaponnumber
                g.saveData['weapon'] = selectedweaponnumber
                self.weapon_gui = 0
                self.select_gui = 0

        # yes / no screen
        if self.option_gui != 0:
            g.disable_fire = 1
            w,h = 90, 100
            SW,SH = g.view.w,g.view.h
            pygame.draw.rect(g.screen, (255,255,255), Rect(SW/2-w/2-20,SH/2-h/2+30,w+4,h+4))
            pygame.draw.rect(g.screen, (60,1,1), Rect(SW/2+2-w/2-20,SH/2+2-h/2+30,w,h))
            g.screen.blit(g.font.render('Yes',0,(255,255,255)), (SW / 2-30,SH/2))
            g.screen.blit(g.font.render('No',0,(255,255,255)), (SW / 2-30,SH/2+30))
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                self.option_gui = 1
            if keys[K_DOWN]:
                self.option_gui = 2
            if self.option_gui == 1:
                img = g.font.render('>',0,(255,255,255))
                g.screen.blit(img, (SW / 2-45,SH/2))
                if keys[K_SPACE] or keys[K_RETURN] or keys[K_z]:
                    self.option_gui = 3
            if self.option_gui == 2:
                img = g.font.render('>',0,(255,255,255))
                g.screen.blit(img, (SW / 2-45,SH/2+30))
                if keys[K_SPACE] or keys[K_RETURN] or keys[K_z]:
                    self.option_gui = 4

        # Draws the circle, and the name of the level
        if not g.intermission:
            if self.draw_timer_gui < 40:
                img = pygame.Surface((g.view.width, g.view.height), SRCALPHA, 32)
                img.fill((0,0,0))
                posm = (g.player.rect.x - g.view.x,g.player.rect.y - g.view.y)
                pygame.draw.circle(img, (0,0,0,0), posm, self.draw_timer_gui * 30)
                g.screen.blit(img, (0,0))
            if self.draw_timer_gui < 60:
                img = g.font.render(self.title,0,(0,0,0))
                posm = (g.view.width /2 - img.get_rect().width/2, g.view.height /2 - img.get_rect().height/2)
                g.screen.blit(img, posm)
                posm = (posm[0] + 2, posm[1] + 2)
                img = g.font.render(self.title,0,(255,255,255))
                g.screen.blit(img,posm)
            if self.draw_timer_gui == 0:
                g.enterLevelSound.play()
        self.draw_timer_gui += 1

        #if self.effect != None:
        #    self.effect.loop(g)



        self.info_box_str = None
        self.info_box_character = None

        if self.moveCamera != None and g.intermission:
            g.view.x += (self.moveCamera[0] - g.view.x) / 10
            g.view.y += (self.moveCamera[1] - g.view.y) / 10

    # n = 0 to 256
    def reversenumber(self, n, r = 128):
        return (-(n - r)) + r - 1




    # draws a gradent from one color to another
    def draw_gradent(self, background_color, background_gradient):
        """ draws a square filled with a gradent

        """
        drawing_area = Rect(0,0, 800, 600)
        image = pygame.Surface((drawing_area[2], drawing_area[3]))

        x1 = drawing_area[0]
        x2 = x1 + drawing_area[2]
        a, b = background_color, background_gradient
        y1 = drawing_area[1]
        y2 = y1 + drawing_area[3]
        h = y2-y1
        rate = (float((b[0]-a[0])/h),
                 (float(b[1]-a[1])/h),
                 (float(b[2]-a[2])/h)
                 )
        for line in range(y1,y2):
             color = (min(max(a[0]+(rate[0]*line),0),255),
                      min(max(a[1]+(rate[1]*line),0),255),
                      min(max(a[2]+(rate[2]*line),0),255)
                      )
             pygame.draw.line(image,color,(x1,line),(x2,line))
        return image

    # called after the msg_box has been called.
    def tick_msg_box(self):
        if self.contains_msg_box == 1:
            self.contains_msg_box_counter += 1
        else:
            self.contains_msg_box_counter = 0
        self.contains_msg_box = 0
    
    # draws the background
    def draw_back(self):
        if self.bgimage != None:
            i = 0
            for m in self.g.backsprites:
                x = self.backwidth * (i)
                m.rect.x = x 
                m.rect.y = self.backheight
                i += 1

                
    # level events
    def level_loop(self):
        pass

    # upon moving
    def playerMove(self, g,r,a):
        pass
    
    # adds a health increase tile
    def add_health_increase (self,g,r,a):
        print 'add_health_increase no method supplied'

    # adds a pike to a position
    def add_spike(self,g,r,a):
        spike = Inventory(self.g, 'spike')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        spike.pos(pos)

    # adds a switch to a position
    def add_switch(self,g,r,a):
        switch = Inventory(self.g, 'switch')
        pos = g.screen_to_tile((r.rect.x + g.view.x, r.rect.y + g.view.y))
        switch.pos(pos)
        self.switches.append(switch)

    # move the camera to a sprites position
    def pan_camera(self, s):
        if s == None:
            self.moveCamera = None
            return
        self.moveCamera = (s.rect.x - self.g.view.width/2 + s.rect.width / 2, s.rect.y - self.g.view.height/2 + s.rect.height / 2)
        
    def loop_render(self):
        g = self.g
        if g.following != None and g.following != 0:
            nx = g.player.rect.x - 13 + 11 * (g.player.direction * 2 - 1)
            if not g.connected:
                speed = g.player.maxspeed
                #dx = g.following.rect.x - g.player.rect.x
                dy = g.following.rect.y - g.player.rect.y
                dx = g.following.rect.x - nx
                if dx < -5 or dx > 5:
                    g.following.rect.x += speed * (int(dx < 0) * 2 - 1)
                    g.following.walking = 1
                if dy < -1 or dy > 1:
                    g.following.rect.y += speed * (int(dy < 0) * 2 - 1)
                    g.following.walking = 1
                g.following.direction = dx > 0
                g.following.walktopos = None
                g.following = None
                if dx >= -5 and dx <= 5 and dy >= -1 and dy <= 1:
                    g.connected = 1
                    print 'hold hands?'
            else:
                dx = g.following.rect.x - g.player.rect.x
                g.following.direction = g.player.direction
                #nx = g.player.rect.x - 13 + 11 * (g.player.direction * 2 - 1)
                ny = g.player.rect.y + g.player.gravity
                if nx != g.following.rect.x:
                    g.following.walking = 1
                    g.following.framecount = g.player.framecount
                g.following.rect.x, g.following.rect.y = nx, ny
                # depending on direction, spaw player and ima.
                if not g.following in g.sprites:
                    return
                a, b = g.sprites.index(g.player), g.sprites.index(g.following)
                fd = g.player.direction
                if (a < b and not fd) or (a > b and fd):
                    g.sprites[b], g.sprites[a] = g.sprites[a], g.sprites[b]
                g.following = None
        else:
            g.connected = 0