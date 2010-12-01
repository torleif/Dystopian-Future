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
        self.title = 'Octagon'

        # current level
        currentLevel = os.path.join("levels",  "level10.tga")
        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles4.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        
        self.initBack('bg1.png', 180)
        
        if 'scene15' in g.saveData:
            self.switches[0].open = 1
            self.switches[1].open = 1

    # adds a monster. in this level they're rats, and one bird
    def add_monster (self,g,r,a):
        Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 11:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y
        if self.prevlevel == 30:
            g.player.rect.x,g.player.rect.y = 38*32,1*32
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos
        if g.player.pos[0] == 1:
            if not 'scene19' in g.saveData:
                g.currentLevel = 9
            else:
                g.currentLevel = 32
        if g.player.pos == (31, 28):
            g.currentLevel = 11
        if g.player.pos[0] == 39:
            g.currentLevel = 30

    # adds a health increase tile
    def add_health_increase (self,g,r,a):
        Inventory(g, 'healthincrease1', (r.rect.x, r.rect.y))

    # draw back of level
    def draw_back(self):
        if 'scene18' in self.g.saveData:
            test = self.draw_gradent((105,70,70), (0, 30, 255))
            self.g.screen.blit(test, (0,0))
        else:
            test = self.draw_gradent((18,217,255), (6, 4, 179))
            self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g
        
        # Some hints as to the past
        if g.player.pos == (16, 20):
            if g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "A note reads:"
                str += "\nRemind Director Victoria that Entertainment Units "
                str += "\nhave been shipped "
                self.info_box(str)
        if g.player.pos == (15, 11):
            if g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "Memo: All third party access requests to the"
                str += "\nEntertainment Fiber Network are to be discarded. Renewed "
                str += "\ncontracts will have their rates increased by their maximum rate."
                self.info_box(str)
        if g.player.pos == (36, 28):
            if g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "A note reads:"
                str += "\nRecent terrorist attacks require accounting, billing, customer service,"
                str += "\nPR and web development teams move to the underground offices. "
                self.info_box(str)

        # switch 1
        if self.switches[0].open:
            self.g.clayer[26][37] = 0
            self.g.tlayer[26][37] = 7
        else:
            self.g.clayer[26][37] = 1
            self.g.tlayer[26][37] = 9
        # switch 2
        if self.switches[1].open:
           self.g.clayer[20][12] = 0
           self.g.tlayer[20][12] = 7
           self.g.saveData['scene15'] = 1
        else:
           self.g.clayer[20][12] = 1
           self.g.tlayer[20][12] = 9

        # 36, 16
        if not self.switches[0].open and self.switches[1].open:
           self.g.clayer[17][36] = 0
           self.g.tlayer[17][36] = 7
        else:
           self.g.clayer[17][36] = 1
           self.g.tlayer[17][36] = 1

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        