""" Get to the airport death? """
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
        g.tga_load_tiles(os.path.join("textures",  "tiles6.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level29.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.g.player.hidden = 0
        self.pan_camera(None)
        self.initBack('bg4.png', 190, 512)
        #pygame.mixer.music.load(os.path.join("ambient",  "amb15.ogg"))
        #pygame.mixer.music.play(40000)


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
        if g.player.pos[0] == 64:
            g.currentLevel = 29
        if g.player.pos[0] == 1:
            g.currentLevel = 27
        print g.player.pos

    # level events
    def level_loop(self):
        g = self.g

        if self.g.player.pos[0] > 24:
            if not 'scene16' in g.saveData:
                g.intermission = 1
                self.pan_camera(self.fox)
                if self.dialog == 0:
                    self.dialog = 1

                if self.dialog != 0:
                    if g.keyup:
                        self.dialog += 1
                        self.contains_msg_box_counter = 0
                if self.dialog == 2:
                    g.intermission = 1
                    str = "The plane is ready. "
                    self.info_box(str,self.director)
                if self.dialog == 3:
                    str = "Him, again?"
                    self.fox.direction = 1
                    self.fox.feeling = 'sad'
                    self.info_box(str,self.director)
                if self.dialog == 4:
                    str = "You still havn't killed him?"
                    self.info_box(str,self.director)
                    self.fox.direction = 0
                if self.dialog == 5:
                    str = "This is your last chance. Finish him!"
                    self.info_box(str,self.director)
                    self.director.walkto((35, 16))
                if self.dialog == 6:
                    g.intermission = 0
                    g.saveData['scene16'] = 1
                    self.dialog = 0
                    self.fox.attacking = 3

        if self.director.hasWalkedTo((35,16)):
            self.director.hidden = 1
        if self.fox.attacking != 0 and self.fox.feeling != 'dead':
            self.fox.draw_health_meter()
            self.g.clayer[16][6] = 1
            self.g.tlayer[16][6] = 30
        else:
            if self.fox.health <= 0:
                self.fox.rect.y += 2 # gravity
            self.g.clayer[16][6] = 0
            self.g.tlayer[16][6] = 0

        if self.fox.feeling == 'dead':
            g.saveData['scene17'] = 1


           
        if self.oldPos != g.player.pos:
            self.dialog = 0
            self.oldPos = g.player.pos
            self.timer = 0
        