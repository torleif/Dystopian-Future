""" after boat ride """
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
        self.title = 'Flooded Lab'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles6.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level33.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.stygian = Character('stygian.png', 'facestygian.png', g)
        self.stygian.pos((8, 9))
        self.stygian.direction = 1
        self.boat = Character('boat.png', 'facestygian.png', g, 'boat')
        self.boat.pos((9, 11))
        
        self.professor = Character("professor.png","faceprofessor.tga", g)
        self.professor.pos((5, 9))
        self.professor.direction = 0
        
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.initBack('bg0.png', 140)


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
        if g.player.pos[0] == 8:
            g.currentLevel = 32

    # level events
    def level_loop(self):
        g = self.g


        # professor will talk to you and give you a key to go underground
        if g.player.pos == self.professor.get_pos():
            if g.event and self.pdialog == 0:
                self.pdialog = 2
                self.timer = 0
                g.intermission = 1
                self.contains_msg_box_counter = 0
                self.professor.walkto((4, 9))

        if g.keyup and self.timer > 30:
            if self.pdialog >= 2:
                self.pdialog += 1
                self.contains_msg_box_counter = 0
                self.timer = 0

        if self.pdialog == 2:
            str = "My workshop was flooded...\nI don't suppose you know do did that?"
            self.info_box(str, self.professor)
            self.g.player.direction = 1
        elif self.pdialog == 3:
            str = "You met the doctor?"
            self.info_box(str, self.professor)
        elif self.pdialog == 4:
            str = "I'm surprised you lived through that. Not many people do."
            self.info_box(str, self.professor)
        elif self.pdialog == 5:
            str = "Here, take this key. It's a shortcut to see the doctor."
            self.info_box(str, self.professor)
        elif self.pdialog == 6:
            str = "\nGot jail key!"
            self.info_box(str)
            g.saveData['i_jailkey'] = 1
        elif self.pdialog == 7:
            g.intermission = 0
                
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos

        self.timer += 1
        