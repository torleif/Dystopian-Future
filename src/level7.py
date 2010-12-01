""" Imas house. boss battle """
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
    dialog = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = "Tree House"

        # current level
        currentLevel = os.path.join("levels",  "level7.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles2.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.fox = Character("fox.png","facefox.tga", g, 'fox')
        self.fox.pos((3, 9))
        self.fox.direction = 0
        self.fox.hidden = 1

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((9, 10))
        self.assistant.direction = 0
        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.g.player.direction = 1
        g.intermission = 1
        if 'scene5' in g.saveData:
            self.assistant.hidden = 1
            self.fox.hidden = 1
            self.dialog = 10

    # adds a monster. in this level they're rats, and one bird
    def add_monster (self,g,r,a):
        if r.rect == Rect(640, 416, 32, 32):
            Enemy(self.g, (r.rect.x, r.rect.y), 'bird')
        else:
            Enemy(self.g, (r.rect.x, r.rect.y), 'rat')

    # upon moving
    def playerMove(self, g,r,a):
        print g, r, a
        pass

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return

        # going back to the train tracks
        if g.event:
            if g.player.pos == (11, 10) and self.dialog == 10:
                g.currentLevel = 6
        

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((60,40,30), (0, 0, 0))
        self.g.screen.blit(test, (0,0))

    # level events
    def level_loop(self):
        g = self.g

        if g.keyup and self.timer > 30:
            if self.dialog < 6:
                self.dialog += 1
                self.contains_msg_box_counter = 0
            if self.dialog == 6 and g.intermission == 1:
                self.dialog += 1
                self.contains_msg_box_counter = 0
            if self.dialog == 9 or self.dialog == 7:
                self.dialog += 1
                self.contains_msg_box_counter = 0

            self.timer = 0

        if self.dialog == 0:
            str = "Ima:"
            str += "\nWelcome to my home"
            self.info_box(str, self.assistant)
        elif self.dialog == 1:
            self.g.player.direction = 1
            self.assistant.direction = 1
            self.fox.hidden = 0
            str = "\nhello!"
            self.info_box(str, self.fox)
        elif self.dialog == 2:
            self.fox.feeling = 'sad'
            str = "I came here to inform you that you Ima broke your "
            str += "\ncontractual obligations. This means I have to take you away."
            self.info_box(str, self.fox)
        elif self.dialog == 3:
            self.fox.feeling = 'normal'
            str = "Who are you?"
            self.info_box(str, self.fox)
        elif self.dialog == 4:
            str = "You must be why I'm here!"
            str += "\nThat means I can squash you!"
            self.info_box(str, self.fox)
        elif self.dialog == 5:
            self.fox.attacking = 1
            self.timer = 0
            self.dialog = 6
            g.intermission = 0
        elif self.dialog == 6:
            if self.fox.attacking != 0: # finishing the battle. Ima gets kidnapped
                self.fox.draw_health_meter()
            else:
                g.intermission = 1
                self.dialog = 7
                self.timer = 0
        elif self.dialog == 7:
            str = "Ah! my face!"
            str += "\nI'm getting out of here."
            self.fox.feeling = 'angry'
            self.info_box(str, self.fox)

        elif self.dialog == 8:
            self.fox.walktorect((self.assistant.rect.x, self.assistant.rect.y))
            self.fox.direction = 0
            if self.fox.rect == Rect(320, 288, 96, 64) or self.fox.rect == Rect(288, 288, 96, 64):
                self.fox.direction = 1
                self.fox.walkto((10, 2))
                self.assistant.walkto((10, 2))
                self.dialog = 9
                self.timer = 0
        elif self.dialog == 9:
            str = "Ima:"
            str += "\nEeeeek!"
            self.assistant.feeling = 'scared'
            self.info_box(str, self.assistant)
            if self.timer > 25:
                self.fox.hidden = 1
                self.assistant.hidden = 1
        elif self.dialog == 10:
            self.dialog = 10
            g.intermission = 0
            g.saveData['scene5'] = 1


        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        