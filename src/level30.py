""" Satalite, get imas backup tape """
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
        self.title = 'Office Complex Top'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles6.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level30.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        self.initBack('bg1.png', 230)

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))


    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 31:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((105,70,70), (0, 30, 255))
        self.g.screen.blit(test, (0,0))

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos
        if g.player.pos[0] == 1:
            g.currentLevel = 10
        if g.player.pos[0] == 39:
            g.currentLevel = 31



    # level events
    def level_loop(self):
        g = self.g

        

        