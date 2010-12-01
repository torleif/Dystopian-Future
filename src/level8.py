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
        self.title = 'Path to Octagon'

        # current level
        currentLevel = os.path.join("levels",  "level8.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles3.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg0.png', 510)

    # adds a monster. in this level they're rats, and one bird
    def add_monster (self,g,r,a):
        if r.rect == Rect(448, 448, 32, 32) or r.rect == Rect(768, 544, 32, 32):
            Enemy(self.g, (r.rect.x, r.rect.y), 'bird')
        else:
            Enemy(self.g, (r.rect.x, r.rect.y), 'rat')
            

    # upon moving
    def playerMove(self, g,r,a):
        print 'player move'
        if self.prevlevel == 9:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return

        # going back to the train tracks
        if g.player.pos[0] == 1:
            g.currentLevel = 6
        if g.player.pos[0] == 39:
            g.currentLevel = 9

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((60,90,200), (50, 40, 179))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g


        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        