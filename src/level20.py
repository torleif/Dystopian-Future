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
        self.title = 'Elevator'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level20.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.movie = 0

    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        print 'add_monster ',r.rect
        #e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')
        Monster0(self.g, (r.rect.x, r.rect.y))


    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 21:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos == (0, 37):
            g.currentLevel = 19

    # level events
    def level_loop(self):
        g = self.g

        if 'scene12' in g.saveData: # (16, 37)
           self.g.clayer[37][16] = 0
           self.g.tlayer[37][16] = 10
        else:
           self.g.clayer[37][16] = 1
           self.g.tlayer[37][16] = 11

        # grabbing the eleivator out of here
        if self.switches[0].open or 'scene12' in g.saveData: #(8, 37)
            self.g.tlayer[37][8] = 53
            if g.player.pos == (8, 37) and g.event and g.intermission == 0:
                self.g.player.hidden = 1
                self.movie = 1
                g.intermission = 1
                pos = g.tile_to_screen((8, 37))
                pos = (pos[0] + g.view.x, pos[1] + g.view.y)
                self.lift = Effect(self.g, 'lift', pos)
            if self.movie:
                self.g.tlayer[37][8] = 10
                self.pan_camera(self.lift)
                if self.lift.rect.y < 80:
                    g.currentLevel = 21
                    g.sprites.remove(self.lift)
                    self.pan_camera(None)
                    g.intermission = 0
        else:
           self.g.tlayer[37][8] = 52


        
        # Say to the player, you're a fucking nigger goddamn
        if g.player.pos == (13, 37) and not 'scene12' in g.saveData:
            if g.event and g.level.option_gui == 0:
                g.level.option_gui = 1
                g.intermission = 1
                self.contains_msg_box_counter = 0
        if g.level.option_gui != 0: # dialog open
            str = "\nThere's a switch on the mushroom. Press it?"
            self.info_box(str)
        if g.level.option_gui == 3: #selected yes
            g.saveData['scene12'] = 1
            g.level.option_gui = 0
            g.intermission = 0
        if g.level.option_gui == 4: #selected no
            g.intermission = 0
            g.level.option_gui = 0



        self.timer += 1
        if self.oldPos != g.player.pos:
            self.pdialog = 0
            self.oldPos = g.player.pos

        