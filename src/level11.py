""" Path to octogon """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from enemies.monster0 import Monster0


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    pullswitch = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Office'

        # current level
        currentLevel = os.path.join("levels",  "level11.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles4.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        if self.pullswitch == 1:
            self.switches[0].open = 1


    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        Monster0(self.g, (r.rect.x, r.rect.y))

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 12:
            print 'r.rect = ', r.rect
            self.pullswitch = 1
            g.view.x = r.rect.x
            g.view.y = r.rect.y
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos == (39, 1):
            g.currentLevel = 12
        if g.player.pos == (7, 1) or g.player.pos == (8, 1):
            g.currentLevel = 10

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (6, 4, 179))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g

        # switch 1 (6, 14)
        if not self.switches[0].open:
            self.g.clayer[14][6] = 1
            self.g.tlayer[14][6] = 9
        else:
            self.g.clayer[14][6] = 0
            self.g.tlayer[14][6] = 7

        if g.player.pos == (22, 22):
            if g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "It's a stack of papers."
                str += "\n\"Today's list of job applications: 1503.\""
                self.info_box(str)

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        