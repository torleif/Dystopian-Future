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
        self.title = 'Elevator'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level21.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        #see two dead fish. Symbolisim
        self.vats = Inventory(g, 'fish0')
        self.vats.pos((19, 19))
        self.vats = Inventory(g, 'fish1')
        self.vats.pos((28, 19))

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg2.png', 680)
        self.g.player.hidden = 0

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 22:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # draw back of level 242422
    def draw_back(self):
        test = self.draw_gradent((0,0,0), (24, 24, 22))
        self.g.screen.blit(test, (0,0))

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos
        if g.player.pos[0] == 38:
            g.currentLevel = 22

    # level events
    def level_loop(self):
        g = self.g
        if g.player.pos == (6, 27):
            if g.event:
                g.currentLevel = 20


        #message at (33, 27)
        if g.player.pos == (33, 27):
            if g.event:
                self.pdialog = 2
            if self.pdialog == 2:
                str = "Casting two fish,"
                str = "\nA man you shall meet you bearing a pitcher of water."
                self.info_box(str)

        self.timer += 1
        if self.oldPos != g.player.pos:
            self.pdialog = 0
            self.oldPos = g.player.pos

        