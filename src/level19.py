""" Jail6 - meet terrorist """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from enemy import Enemy


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    btimer = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Jail'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level19.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        # and an odd object called flutter box. flutter shutter (37, 13) 
        self.terrorist = Character("terrorist.png","faceterrorist.tga", g)
        self.terrorist.pos((3, 20))
        self.terrorist.direction = 0
        self.terrorist.faceup = 1

        self.flutterbox = Inventory(g, 'flutterbox')
        self.flutterbox.pos((37, 13))
        self.flutterswitch = Inventory(g, 'flutterswitch')
        self.flutterswitch.pos((37, 20))

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        print 'add_monster ',r.rect
        e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster1')

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 20:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos[1] == 1:
            g.currentLevel = 18

        if g.player.pos == (39, 27) or g.player.pos == (39, 28):
            g.currentLevel = 20

    # level events
    def level_loop(self):
        g = self.g



        # 16, 13
        if self.switches[0].open:
           self.g.clayer[13][16] = 0
           self.g.tlayer[13][16] = 2
        else:
           self.g.clayer[13][16] = 1
           self.g.tlayer[13][16] = 25

        #(26, 13)
        if self.switches[1].open:
           self.g.clayer[13][26] = 0
           self.g.tlayer[13][26] = 2
        else:
           self.g.clayer[13][26] = 1
           self.g.tlayer[13][26] = 25

        # opened up the flutter box (13, 20)
        if 'scene10' in g.saveData:
           self.g.clayer[20][11] = 0
           self.g.tlayer[20][11] = 2
        else:
           self.g.clayer[20][11] = 1
           self.g.tlayer[20][11] = 25

        # door to leave (38, 27)
        if 'scene11' in g.saveData:
           self.g.clayer[27][38] = 0
           self.g.tlayer[27][38] = 2
        else:
           self.g.clayer[27][38] = 1
           self.g.tlayer[27][38] = 25
        

        if g.player.pos == (37, 20):
            if 'i_flutterbox' in g.saveData:
                if g.event:
                    self.pdialog = 1
                    g.saveData['scene10'] = 1
                if self.pdialog == 1:
                    str = "\nPlaced the flutter box inside the holder"
                    self.info_box(str)
                    
        # talking to the terrorist
        if g.player.pos == (3, 20):
            if g.keyup and self.timer > 30:
                if self.pdialog > 0:
                    self.pdialog += 1
                    self.timer = 0
                    self.contains_msg_box_counter = 0
            if g.event and self.pdialog < 2:
                self.pdialog = 1
            if self.pdialog == 2:
                g.intermission = 1
                str = "Ah?"
                str += "\nYou interrupted me!"
                self.info_box(str, self.terrorist)
                self.terrorist.walkto((4, 20))
                self.terrorist.direction = 1
                self.terrorist.faceup = 0
                g.player.direction = 0
            elif self.pdialog == 3:
                str = "Haha! You're bald! "
                self.info_box(str, self.terrorist)
            elif self.pdialog == 4:
                str = "You must be the one who was sent down here. I guess the robot "
                str += "\ndidn't think you'd live past the Monotane. "
                str += "\nShe didn't think much of me either. "
                self.info_box(str, self.terrorist)
            elif self.pdialog == 5:
                str = "Most people don't think much of my group."
                self.info_box(str, self.terrorist)
            elif self.pdialog == 6:
                str = "They called us terrorists, after they ruined the economy. They "
                str += "\nlobbied our leaders against the people, and when the people turned "
                str += "\nto crime to put food on their table they put them in prison."
                self.info_box(str, self.terrorist)
            elif self.pdialog == 7:
                str = "We found salvation. A company called News Corp financed us "
                str += "\nso we could fight back. "
                self.info_box(str, self.terrorist)
            elif self.pdialog == 8:
                str = "The government stepped in and sold the people  "
                str += "\nEntertainment Devices that protected them completely.  "
                str += "\nThose blue things behind me, there are people in them.  "
                self.info_box(str, self.terrorist)
            elif self.pdialog == 9:
                str = "I've hacked the Entertainment network. The girl you're looking for "
                str += "\nwas inserted into the system, but got rejected due to an  "
                str += "\nincompatible brain. She's going to be flown out of the city soon. "
                self.info_box(str, self.terrorist)
            elif self.pdialog == 10:
                str = "Take my card with my location. The airport is down to the right; "
                str += "\nif you ever want to  continue the fight against the power,"
                str += "\nyou know where to find me.  "
                self.info_box(str, self.terrorist)
            elif self.pdialog == 11:
                str = "\nReceived the location card!"
                self.info_box(str)
                g.saveData['i_locationcard'] = 1
            elif self.pdialog == 12:
                g.intermission = 0
                g.saveData['scene11'] = 1



        self.timer += 1
        if self.oldPos != g.player.pos:
            self.pdialog = 0
            self.oldPos = g.player.pos

        