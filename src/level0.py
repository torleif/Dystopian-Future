""" Gardies Cloning faclities """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
from inventory import Inventory

class Level(LevelBase):
    prevlevel = 0
    timer = 0

    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new,dimentions)
        self.prevlevel = p

        self.title = 'Gardies Cloning faclities'
        # current level
        currentLevel = os.path.join("levels",  "level0.tga")

        TW,TH = 32,32

        # an ambient sound plays
        ambientSound = os.path.join("ambient",  "amb1.ogg")
        pygame.mixer.music.load(ambientSound)

        # load tile set
        tileTexture = os.path.join("textures",  "tiles0.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        g.code_events(self.edata)

        # fade in and display a quick waking up animation
        if 'scene_start' in g.saveData:
            self.timer = 255
        else:
            g.saveData['scene_start'] = 1
            g.intermission = 1
        
        
    # leaving this level
    def leave(self):
        LevelBase.leave(self)
        
    # if the player comes back from a prev level
    def playerMove(self, g,r,a):
        if self.prevlevel == 1:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
        else:
            pygame.mixer.music.play() # play the start 'theme'

    # if the player hits a change level tile
    def change_level(self, g,r,a):
        if not g.event or a.__class__.__name__ != 'Player':
            return

        if g.player.pos == (11, 10):
            self.g.currentLevel = 1

    # level events
    def level_loop(self):
        g = self.g
        LevelBase.level_loop(self)
        
        # when the player investigates something
        if g.player.pos == (3,10) or g.player.pos == (4,10):
            if g.event:
                self.dialog = 1
            if self.dialog == 1:
                str = "\"Stem Scaffolding Construction Device\""
                str += "\nGARD01"
                self.info_box(str)
        if g.player.pos == (5,10):
            if g.event:
                self.dialog = 2
            if self.dialog == 2:
                str = "$> patch --binary template.bsf subject24.bsf > /dev/tty2"
                str += "\nis written on console"
                self.info_box(str)

        if self.oldPos != g.player.pos:
            # clear dialog box
            self.dialog = 0
            
        # remmber last pos so I can remove old dialoge boxes
        self.oldPos = g.player.pos

        self.timer += 1
        # fade out of black
        if self.timer < 255:
            if self.timer < 64:
                alpha = self.timer * 4
                self.g.screen.fill((alpha,alpha,alpha), None, BLEND_MULT)
            if self.timer < 50:
                self.g.player.animation = 1
            elif self.timer < 118:
                self.g.player.animation = 2
            elif self.timer < 135:
                self.g.player.animation = 1
            elif self.timer < 140:
                self.g.player.animation = 2
            elif self.timer < 145:
                self.g.player.animation = 3
            elif self.timer < 156:
                self.g.player.animation = 0
                g.intermission = 0
