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
        currentLevel = os.path.join("levels",  "level6.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles2.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((4, 16))
        self.assistant.direction = 0
        if 'scene5' in g.saveData:
            self.assistant.hidden = 1
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg0.png', 290)

    # adds a monster. in this level they're rats, and one bird
    def add_monster (self,g,r,a):
        if r.rect == Rect(672, 416, 32, 32):
            Enemy(self.g, (r.rect.x, r.rect.y), 'bird')
        else:
            Enemy(self.g, (r.rect.x, r.rect.y), 'rat')

    # upon moving
    def playerMove(self, g,r,a):
        # imas house. Y pos does not get set right, so we minus a bit from the y
        if self.prevlevel == 7 and r.rect == Rect(1056, 320, 32, 32): 
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y - 16
            g.view.x = r.rect.x
            #g.view.y = r.rect.y - 400
        elif self.prevlevel == 8 and r.rect == Rect(1184, 512, 32, 32):
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y 
            g.view.x = r.rect.x
            #g.view.y = r.rect.y
        else:
            g.view.y = 200

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return

        # going to level 6 - before imas house
        if g.player.pos[0] == 1:
            g.currentLevel = 5

        # going to the octogon
        if g.player.pos[0] == 38 and 'scene6' in g.saveData:
            g.currentLevel = 8

        # going back to the tree house
        if g.event:
            if g.player.pos == (32, 10) or g.player.pos == (33, 10):
                g.currentLevel = 7
        

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,217,255), (6, 4, 179))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g

        if 'scene5' not in g.saveData:
            #self.assistant.walktorect((g.player.rect.x - 32, g.player.rect.y))
            #if g.player.direction == 1:
            #    self.assistant.walktorect((g.player.rect.x + 8, g.player.rect.y))
            #self.assistant.direction = g.player.direction
            g.following = self.assistant
            

        if 'scene6' not in g.saveData:
            if g.player.pos == (37, 16):
                if g.event:
                    self.pdialog = 1
                if self.pdialog:
                    str = "\nOctagon this way"
                    self.info_box(str)
            if g.player.pos == (39, 16):
                str = "\nI don't need to go to the Octagon now"
                self.info_box(str)
                

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        