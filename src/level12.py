""" Path to octogon """
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
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Office'

        # current level
        currentLevel = os.path.join("levels",  "level12.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles4.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 13:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos == (3, 28) or g.player.pos ==(2, 29) or g.player.pos == (2, 28):
            g.currentLevel = 11
        if g.player.pos[1] == 1:
            g.currentLevel = 13


    # level events
    def level_loop(self):
        g = self.g


        # switch 1 (37, 15)
        if self.switches[0].open:
            self.g.clayer[15][36] = 0
            self.g.tlayer[15][36] = 7
        else:
            self.g.clayer[15][36] = 1
            self.g.tlayer[15][36] = 9

        if g.player.pos == (23, 18):
            if g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "Written on a console:"
                str += "\nSCF 10: Cell scaffold complete. Injecting stem cells complete. EMF "
                str += "\nresonance complete. Ejecting specimen. "
                self.info_box(str)

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        