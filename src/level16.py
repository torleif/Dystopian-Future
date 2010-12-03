""" Jail3  """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from enemies.monster1 import Monster1


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
        tileTexture = os.path.join("textures",  "tiles5.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        currentLevel = os.path.join("levels",  "level16.tga")
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        #e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster1')
        e = Monster1(self.g, (r.rect.x, r.rect.y))

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 17:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos[1] < 15:
            g.currentLevel = 15
        else:
            g.currentLevel = 17

    # level events
    def level_loop(self):
        g = self.g

        