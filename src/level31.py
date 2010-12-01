""" Satalite, get imas backup tape """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from effect import Effect
from enemy import Enemy
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
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Office Complex Top'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles6.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level31.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        self.initBack('bg1.png', 730)

        self.backuptape = Inventory(g, 'tape', (37, 22))
        self.backuptape.pos((37, 22))
        self.backup = Character('backup.png', 'facebackup.png', g, 'backup')
        self.backup.pos((28, 25))
        self.backup.direction = 0
        if 'scene21' in g.saveData:
            self.backup.hidden = 1
        # coming back and saying high to the guy.
        if 'scene20' in g.saveData and not 'scene21' in g.saveData:
            del g.saveData['scene20']

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.coins = 0


    # upon moving
    def playerMove(self, g,r,a):
        print 'player move'

    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((105,70,70), (0, 30, 255))
        self.g.screen.blit(test, (0,0))

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos
        if g.player.pos[0] == 1:
            g.currentLevel = 30

    # level events
    def level_loop(self):
        g = self.g



        # Some hints as to the past
        if g.player.pos == (28, 25) and not 'scene20' in g.saveData:
            if self.pdialog != 0:
                if g.keyup:
                    self.contains_msg_box_counter = 0
                    self.pdialog += 1
            if g.event and self.pdialog == 0:
                self.backup.face_the_player()
                g.intermission = 1
                self.pdialog = 1
                self.backup.walkto((29, 25))
                self.backup.direction = 1
                g.player.direction = 0

            if self.pdialog == 2:
                str = "Hello"
                self.info_box(str, self.backup)
            elif self.pdialog == 3:
                str = "You don't know me..."
                str += "\nbut I know you, ha. Haha!"
                self.info_box(str, self.backup)
            elif self.pdialog == 4:
                str = "Who knows if I'm myself, when I am who what's on a tape? "
                str += "\nSeveral times I've been built because of a timer."
                str += "\nWhat happened in between these gaps is anyone's guess."
                self.info_box(str, self.backup)
            elif self.pdialog == 5:
                str = "You came to tell me what you're doing."
                str += "\nBut I already know!"
                self.info_box(str, self.backup)
            elif self.pdialog == 6:
                str = "See, you can't have her tape."
                str += "\nI need it. For the future, you see."
                self.info_box(str, self.backup)
            elif self.pdialog == 7:
                str = "The insult 'tool' never really fits to most situations."
                str += "\nBut now it's apt!"
                self.info_box(str, self.backup)
            elif self.pdialog == 8:
                str = "...sudo apt!"
                self.info_box(str, self.backup)
            elif self.pdialog == 9:
                str = "..."
                self.info_box(str, self.backup)
            elif self.pdialog == 10:
                str = "Now you die!"
                self.info_box(str, self.backup)
            elif self.pdialog == 11:
                g.saveData['scene20'] = 1
                self.backup.attacking = 1
                self.backup.dy = -10.0
                self.pdialog = 20
                self.backup.walkto(None)
        else:
            g.intermission = 0

        if 'scene20' in g.saveData:
            if not 'scene21' in g.saveData:
                self.backup.draw_health_meter()

        if self.backup.health <= 0:
            if not 'scene21' in g.saveData:
                g.saveData['scene21'] = 1
                self.backup.attacking = 0
                self.backup.dead = 1
                self.coins = Inventory(g, 'coin', (self.backup.rect.x, self.backup.rect.y) )

        if self.coins:
            self.coins.rect.y += 5
            self.backup.rect.y += 5


        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos


        