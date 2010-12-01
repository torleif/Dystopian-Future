""" Castle st level """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from pgu import tilevid, timer


class Level(LevelBase):
    prevlevel = 0
    oldPos =(0, 0)

    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new,dimentions)
        self.prevlevel = p
        self.title = 'Castle st'

        # current level
        currentLevel = os.path.join("levels",  "level1.tga")


        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles0.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        g.code_events(self.edata)
        self.initBack('bg0.png', 128)


    # if the player comes back from a prev level
    def playerMove(self, g,r,a):
        if self.prevlevel == 2:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y
            #g.player.set_position((r.rect.x,r.rect.y))

    # user hits a change level block
    def change_level(self, g,r,a):
        if not g.event or a.__class__.__name__ != 'Player':
            return
        # back to the cloning lab
        if g.player.pos == (3, 9):
            self.g.currentLevel = 0
        # to the professors lab
        if g.player.pos == (38, 9):
            self.g.currentLevel = 2


    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (255, 255, 255))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g
        LevelBase.level_loop(self)

        # when the player investigates something
        if g.player.pos == (6, 9):
            if g.event:
                self.dialog = 1
            if self.dialog == 1:
                str = "Gardies Research Facility"
                self.info_box(str)
        if g.player.pos == (34, 9):
            if g.event:
                self.dialog = 1
            if self.dialog == 1:
                str = "Centre For Innovation"
                self.info_box(str)

        if self.oldPos != g.player.pos:
            # clear dialog box
            self.dialog = 0

        # remmber last pos so I can remove old dialoge boxes
        self.oldPos = g.player.pos

