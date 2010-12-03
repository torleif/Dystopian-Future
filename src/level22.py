""" elevator to under airport """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from effect import Effect
#from enemies.enemy import Enemy
from enemies.monster0 import Monster0


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
        self.title = 'Underground'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level22.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.g.player.hidden = 0
        
        # so you can get back
        if self.prevlevel == 23:
            self.switches[0].pull_switch()

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        #e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')
        Monster0(self.g, (r.rect.x, r.rect.y))

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 23:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos[0] == 38:
            g.currentLevel = 23
        if g.player.pos[0] == 1:
            g.currentLevel = 21

    # level events
    def level_loop(self):
        g = self.g

        if self.switches[0].open: # (8, 5)
           self.g.clayer[5][8] = 0
           self.g.tlayer[5][8] = 10
        else:
           self.g.clayer[5][8] = 1
           self.g.tlayer[5][8] = 25

        self.timer += 1
        if self.oldPos != g.player.pos:
            self.pdialog = 0
            self.oldPos = g.player.pos

        