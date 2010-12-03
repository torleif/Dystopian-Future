""" boat ride """
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
        self.title = 'Styx'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles6.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level32.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.stygian = Character('stygian.png', 'facestygian.png', g)
        self.stygian.pos((17, 9))
        self.stygian.direction = 0
        self.boat = Character('boat.png', 'facestygian.png', g, 'boat')
        self.boat.pos((15, 12))
        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg0.png', 160)


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
        print g.player.pos
        if g.player.pos[0] == 22:
            g.currentLevel = 10

    # level events
    def level_loop(self):
        g = self.g

        # the ferryman only taks you if you have the coins
        if g.player.pos == self.stygian.get_pos():
            if g.event and self.pdialog == 0:
                self.pdialog = 1

        if self.pdialog == 1:
            if not 'i_coin' in g.saveData:
                str = "hue!\nSomeone flooded this street"
                self.info_box(str, self.stygian)
            else:
                g.currentLevel = 33

        # fall in water
        if g.player.rect.y > 356:
            g.player.health = 0
                
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos


        