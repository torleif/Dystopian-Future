""" train tracks. conatains monsters. """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from pgu import tilevid, timer
from character import Character
from inventory import Inventory
from enemy import Enemy


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = "Tracks"

        # current level
        currentLevel = os.path.join("levels",  "level5.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles1.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((5, 10))
        self.assistant.direction = 0
        if 'scene5' in g.saveData:
            self.assistant.hidden = 1
        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg0.png', 170)

    # adds a monster. in this level they're birds.
    def add_monster (self,g,r,a):
        Enemy(self.g, (r.rect.x, r.rect.y), 'bird')

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 6:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            self.assistant.rect.x,self.assistant.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return

        # going to level 6 - before imas house
        if g.player.pos[0] == 49:
            g.currentLevel = 6

        # going back to the lab
        if g.event:
            if g.player.pos == (1,10):
                g.currentLevel = 2

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (6, 4, 179))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g
        if 'scene5' not in g.saveData:
            g.following = self.assistant
        
        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        