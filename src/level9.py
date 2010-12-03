""" Path to octogon """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from enemies.bird import Bird
from enemies.rat import Rat


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
        self.title = 'Path to Octagon'

        # current level
        currentLevel = os.path.join("levels",  "level9.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles3.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg0.png', 680)

    # adds a monster. in this level they're rats, and one bird
    def add_monster (self,g,r,a):
        if r.rect == Rect(1024, 704, 32, 32):
            Bird(self.g, (r.rect.x, r.rect.y))
        else:
            Rat(self.g, (r.rect.x, r.rect.y))

    # adds a health increase tile
    def add_health_increase (self,g,r,a):
        pass
        Inventory(g, 'healthincrease0', (r.rect.x, r.rect.y))
        
    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 10 :
            g.view.x = r.rect.x
            g.view.y = r.rect.y 
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y - 54

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos[0]
        if g.player.pos[0] == 1:
            g.currentLevel = 8
        if g.player.pos[0] == 39:
            g.currentLevel = 10

        print g.player.pos


    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (6, 4, 179))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g


        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        