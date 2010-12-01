""" Clock tower """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from pgu import tilevid, timer
from character import Character
from inventory import Inventory


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Clock Tower'

        # current level
        currentLevel = os.path.join("levels",  "level4.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles1.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((3, 24))
        self.assistant.direction = 0

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        if 'scene3' in g.saveData:
            self.dialog = 4
            self.g.sprites.remove(self.assistant)

    # upon moving
    def playerMove(self, g,r,a):
        print g, r, a
        pass

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if not g.event or a.__class__.__name__ != 'Player':
            return

        if r == Rect(128, 768, 32, 32):
            self.g.currentLevel = 3
        

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (255, 255, 255))
        test = test.subsurface((0, 0, 480, test.get_rect().height))
        self.g.screen.blit(test, (80,0))

    # level events
    def level_loop(self):
        g = self.g

        # if you have the microwave and get to the top
        if self.dialog == 0 and 'i_microwave' in g.saveData:
            #self.assistant.walkto((g.player.pos[0],g.player.pos[1]))
            #self.assistant.direction = g.player.direction
            g.following = self.assistant
            if g.player.pos == (6, 4) or g.player.pos == (5, 4):
                self.dialog = 1
                self.timer = 0
        elif self.dialog == 1:
            self.assistant.walkto((4, 4))
            str = "Ima:"
            str += "\nThis is where we transmit a things."
            str += "\nIt's our job to make sure it keeps working."
            self.info_box(str, self.assistant)
            g.intermission = 1
            if g.keyup and self.timer > 40:
                self.dialog += 1
        elif self.dialog == 2:
            self.assistant.walkto((3, 4))
            g.intermission = 0
            if g.player.pos == (1, 4):
                if g.event:
                    self.timer = 0
                    self.dialog = 3
                    g.saveData['i_' + 'microwave'] = 0
        elif self.dialog == 3:
            str = "\nPlaced the transmitter in the slot!"
            self.assistant.following = g.player
            g.intermission = 1
            g.player.staylooking = 1
            self.info_box(str)
            if g.keyup and self.timer > 40:
                self.dialog += 1
                self.timer = 0
        elif self.dialog == 4:
            g.player.staylooking = 0
            self.assistant.walkto((2, 4))
            if self.assistant.hasWalkedTo((2, 4)):
                if g.keyup and self.timer > 40:
                    self.dialog += 1
                g.player.direction = 0
                self.assistant.direction = 1
                str = "Ima:"
                str += "\nThe building where you woke up"
                str += "\nI woke up there too."
                self.info_box(str, self.assistant)
                g.saveData['scene3'] = 1
        elif self.dialog == 5:
            g.intermission = 0
            if self.assistant in g.sprites:
                g.following = self.assistant
        
        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        