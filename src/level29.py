""" blank level """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from effect import Effect
from gameEffect import GameEffect




class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    btimer = 0
    lockedatmessage = 0
    inbattle = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Airport'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level29.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.g.player.hidden = 0
        self.pan_camera(None)

        self.doctor = Character("monster3a.png", "monster3a.png", self.g, 'doctor')
        self.doctor.pos((25, 20)) # 25, 20
        self.doctor.health = 0
        self.doctor.dead = 1
        
        self.movie = 0
        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((33, 27))
        self.assistant.feeling  = 'coma'
        self.nurse = Character("monster4.png", "facenurse.png", self.g, 'nurse')
        self.nurse.pos((29, 27))
        self.nurse.direction = 0
        if not 'scene14' in g.saveData:
            self.nurse.feeling = 'dead'
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))


    # upon moving
    def playerMove(self, g,r,a):
        print 'player move'

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((105,70,70), (0, 30, 255))
        self.g.screen.blit(test, (0,0))

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        
        print g.player.pos

    # level events
    def level_loop(self):
        g = self.g

        if g.player.pos == (29, 27):
            if self.dialog == 0:
                if g.event:
                    g.intermission = 1
                    self.dialog = 1
            else:
                if self.dialog <= 4:
                    g.player.staylooking = 1
                if g.keyup:
                    if self.dialog != 4: # walking
                        self.dialog += 1
                        self.contains_msg_box_counter = 0

        if self.dialog == 2:
            g.player.direction = 1
            str = "I've set up the computer ready for the tape. All I need now"
            str += "\nis her tape."
            str += "\n"
            self.info_box(str,self.nurse)
        elif self.dialog == 3:
            str = "You have it? That's great!"
            str += "\n Give it here and I'll set it up"
            str += "\n"
            self.info_box(str,self.nurse)
        elif self.dialog == 4:
            self.nurse.walkto((31,27))
            if self.nurse.hasWalkedTo((31,27)):
                self.dialog = 5
                g.player.staylooking = 0
                g.player.direction = 0
        elif self.dialog == 5:
            str = "Lemmie start up the transfer"
            str += "\n"
            self.info_box(str,self.nurse)
        elif self.dialog == 6:
            if (self.timer / 4) % 2 == 0 :
                self.nurse.feeling = 'look0'
            else:
                self.nurse.feeling = 'look1'
        elif self.dialog == 7:
            self.nurse.feeling = ''
            str = "Hmmm...."
            str += "\n"
            self.info_box(str,self.nurse)
        elif self.dialog == 8:
            str = "arrg..."
            str += "\n"
            self.assistant.feeling = 'coma2'
            self.info_box(str,self.assistant)
        elif self.dialog == 9:
            str = "She's awake!"
            str += "\n"
            self.info_box(str,self.nurse)
        elif self.dialog == 10:
            g.shake_screen()
            g.exp2.play()
            self.dialog = 11
        elif self.dialog == 11:
            str = "???"
            str += "\n"
            self.info_box(str,self.nurse)
        elif self.dialog == 12:
            g.intermission = 0


                    
        self.timer += 1
        if self.oldPos != g.player.pos:
            self.dialog = 0
            self.oldPos = g.player.pos
            self.timer = 0
        