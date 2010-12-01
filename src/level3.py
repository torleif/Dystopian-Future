""" leith """
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
    dialog = 1
    pdialog = 0
    timer = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Water of Leith'

        # current level
        currentLevel = os.path.join("levels",  "level3.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles0.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((3, 10))
        self.assistant.direction = 0
        g.intermission = 1
        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

        # already done the cut scene
        if 'scene2' in g.saveData:
            self.dialog = 5
        if 'scene4' in g.saveData:
            self.g.sprites.remove(self.assistant)
        self.initBack('bg0.png', 180)

        

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 4:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            #g.view.y = r.rect.y # meh...
            self.assistant.pos((54, 10))

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if not g.event or a.__class__.__name__ != 'Player':
            return

        #back to castle st
        if self.g.player.pos == (1, 10):
            self.g.currentLevel = 2
        if self.g.player.pos == (56, 10):
            self.g.currentLevel = 4



    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (255, 255, 255))
        self.g.screen.blit(test, (0,0))

        # sparkling water
        if self.timer % 7 == 0:
            w,h = self.g.dimentions[0], self.g.dimentions[1]
            for y in range(0,h):
                for x in range(0,w):
                    if self.g.tlayer[y][x] == 26:
                        self.g.tlayer[y][x] = 34
                    elif self.g.tlayer[y][x] == 34:
                        self.g.tlayer[y][x] = 26

    # level events
    def level_loop(self):
        g = self.g

        # if the key is up
        if g.keyup and self.timer > 40 and self.dialog < 4:
            self.dialog += 1
            self.timer = 0
            self.contains_msg_box_counter = 0

        if self.dialog == 1:
            self.assistant.walkto((7, 10))
            if self.assistant.hasWalkedTo((7, 10)):
                self.assistant.faceup = 1
                str = "Ima:"
                str += "\nYou can see old shopping trolleys in the Leith."
                self.info_box(str, self.assistant)
        elif self.dialog == 2:
            self.assistant.faceup = 0
            self.assistant.direction = 1
            str = "Ima:"
            str += "\nIf they weren't rusted I'd ride down hills in them"
            self.info_box(str, self.assistant)
        elif self.dialog == 3:
            str = "Ima:"
            str += "\nLet's get to the tower. "
            self.info_box(str, self.assistant)
        elif self.dialog == 4:
            self.assistant.walkto((3, 10))
            if self.assistant.hasWalkedTo((3,10)):
                self.dialog = 5
        elif self.dialog == 5:
            g.intermission = 0
            # Ima follows the player
            #if g.player.direction == 0:
            #    self.assistant.walkto((g.player.pos[0]-1,g.player.pos[1]))
            #    self.assistant.direction = 0
            #else:
            #    self.assistant.walkto((g.player.pos[0]+1,g.player.pos[1]))
            #    self.assistant.direction = 1
            g.following = self.assistant
            g.saveData['scene2'] = 1
            if g.player.pos == (52, 10):
                if g.event:
                    self.pdialog = 1
                if self.pdialog == 1:
                    str = "Clock Tower"
                    str += "\nGracefully reconstructed by News Corporation"
                    self.info_box(str)

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        