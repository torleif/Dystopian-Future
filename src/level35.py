""" jail - battle a few more monsters, battle end guy, save ima. """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from effect import Effect
from enemies.ghost import Ghost
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
    movie = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Jail - Airport Shortcut'
        # current level
        TW,TH = 32,32
        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level35.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))


    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        Ghost(self.g, (r.rect.x, r.rect.y))

    # upon moving
    def playerMove(self, g,r,a):
        print 'player move'

    # draw back of level
    def draw_back(self):
        pass

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos
        if g.player.pos[1] == 38:
            g.currentLevel = 36
        if g.player.pos[0] == 0:
            g.currentLevel = 34

    # level events
    def level_loop(self):
        g = self.g

        if g.player.pos == (35, 8) and g.event and g.intermission == 0:
            self.g.player.hidden = 1
            self.movie = 1
            g.intermission = 1
            pos = g.tile_to_screen((35, 8))
            pos = (pos[0] + g.view.x, pos[1] + g.view.y)
            self.lift = Effect(self.g, 'lift', pos)
        if self.movie:
            self.g.tlayer[8][35] = 10
            self.pan_camera(self.lift)
            if self.lift.rect.y < 20:
                g.currentLevel = 25
                g.sprites.remove(self.lift)
                self.pan_camera(None)
                g.intermission = 0

        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos

        self.timer += 1
        