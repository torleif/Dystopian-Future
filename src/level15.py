""" Jail2 - monster battle """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from enemies.monster1 import Monster1


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    btimer = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        self.monsters = []
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Jail'
        # current level
        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles5.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        currentLevel = os.path.join("levels",  "level15.tga")
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.mushroom = Character("mushroom.png","faceassistant.png", g, 'mushroom')
        self.mushroom.pos((5, 20))

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

        if 'scene9' in g.saveData:
            self.mushroom.dead = 1


    # adds a health increase tile
    def add_health_increase (self,g,r,a):
        Inventory(g, 'healthincrease2', (r.rect.x, r.rect.y))
        
    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        #e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster1')
        e = Monster1(self.g, (r.rect.x, r.rect.y))
        e.waketype = 'water'
        self.monsters.append(e)

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 16:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos == (1, 27):
            g.currentLevel = 16
            return

        if g.player.pos[0] == 1:
            g.currentLevel = 14

    # level events
    def level_loop(self):
        g = self.g

        #first door
        if self.switches[0].open:
           self.g.clayer[7][14] = 0
           self.g.tlayer[7][14] = 2
           self.sprinklers[0].on = 1
           self.sprinklers[1].on = 1
           self.monsters[0].wet = 1
           self.monsters[1].wet = 1
        else:
           self.g.clayer[7][14] = 1
           self.g.tlayer[7][14] = 25
           self.sprinklers[0].on = 0
           self.sprinklers[1].on = 0

        # Second swtich (17, 10)
        if self.switches[1].open:
           self.g.clayer[24][24] = 0
           self.g.tlayer[24][24] = 2
           self.g.clayer[10][17] = 0
           self.g.tlayer[10][17] = 2
           self.sprinklers[2].on = 1
           self.monsters[2].wet = 1
        else:
           self.g.clayer[24][24] = 1
           self.g.tlayer[24][24] = 25
           self.g.clayer[10][17] = 1
           self.g.tlayer[10][17] = 25
           self.sprinklers[2].on = 0


        # (1, 27)
        if 'scene9' in g.saveData:
           self.g.clayer[27][1] = 0
           self.g.tlayer[27][1] = 2
           self.g.clayer[24][24] = 0
           self.g.tlayer[24][24] = 2
           self.g.clayer[7][14] = 0
           self.g.tlayer[7][14] = 2
        else:
           self.g.clayer[27][1] = 1
           self.g.tlayer[27][1] = 25


        if self.g.player.pos == (20, 19):
            if g.event:
                self.dialog = 1
            if self.dialog == 1:
                str = "\nBeware! the Monotane lies"
                self.info_box(str)

        d = self.g.player.pos
        if d[0] < 15 and d[1] > 20:
            # a little movie
            if 'scene8' not in g.saveData:
                g.intermission = 1
                g.view.x -= 5
                if g.view.x <= 30:
                    g.intermission = 0
                    g.saveData['scene8'] = 1
                    self.mushroom.attacking = 1
                    self.mushroom.feeling = 'walking'
            if self.mushroom.dead:
                g.saveData['scene9'] = 1

        

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
            self.dialog = 0
            self.contains_msg_box_counter = 0
        self.oldPos = g.player.pos
        self.timer += 1

        