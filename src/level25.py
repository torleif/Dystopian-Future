""" Get to the airport, and an intermission """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from effect import Effect
from enemies.monster5 import Monster5
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
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Airport'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles6.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level25.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.g.player.hidden = 0
        self.pan_camera(None)
        self.initBack('bg3.png', 190, 512)
        self.effect = GameEffect(g,'wind')
        pygame.mixer.music.load(os.path.join("ambient",  "amb15.ogg"))
        pygame.mixer.music.play(40000)

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        Monster5(self.g, (r.rect.x, r.rect.y))

    # upon moving
    def playerMove(self, g,r,a):
        print 'player move'
        if self.prevlevel == 26:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y - 2
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # adds a health increase tile
    def add_health_increase (self,g,r,a):
        Inventory(g, 'healthincrease4', (r.rect.x, r.rect.y))

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((105,70,70), (0, 30, 255))
        self.g.screen.blit(test, (0,0))

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos[0] == 64:
            g.currentLevel = 26
            if 'i_tape' in g.saveData:
                g.currentLevel = 28 # change the level a bit.

    # level events
    def level_loop(self):
        g = self.g
        if g.player.pos == (7, 17):
            if g.event:
                g.currentLevel = 24

        if self.oldPos != g.player.pos:
            self.dialog = 0
            self.oldPos = g.player.pos
            self.timer = 0
        