""" battle fox #2 """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory
from enemies.enemy import Enemy
from effect import Effect
from enemies.monster0 import Monster0


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    btimer = 0
    fadein = 0
    watertimer = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Office'

        # current level
        currentLevel = os.path.join("levels",  "level13.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles4.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)
        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

        # intermission!
        self.fox = Character("fox.png","facefox.tga", g, 'fox')
        self.fox.pos((27, 13))
        self.fox.direction = 0
        self.fox.hidden = 1

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((28, 9))
        self.assistant.direction = 0
        self.assistant.feeling = 'pulled'
        self.assistant.hidden = 1

        self.director = Character("director.png","facedirector.png", g, 'director')
        self.director.pos((32, 14))
        self.director.direction = 1
        self.director.feeling = 'sit'

        if 'scene18' in g.saveData:
            self.director.hidden = 1
            self.dialog = 15
            g.intermission = 0
            self.switches[0].open = 1

        
    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        print 'add_monster ',r.rect
        #Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')
        Monster0(self.g, (r.rect.x, r.rect.y))

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 14:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

            # you also wake up here if you've just killed robot
            if 'scene18' in g.saveData:
                self.fadein = 1


    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        print g.player.pos
        if g.player.pos[1] == 23:
            g.currentLevel = 12

    # level events
    def level_loop(self):
        g = self.g

        if g.keyup and self.timer > 30:
            if self.dialog > 0 and self.dialog != 10 and self.dialog != 9 and self.dialog != 11 and self.dialog != 15:
                self.dialog += 1
                self.contains_msg_box_counter = 0

        if g.player.pos == (24, 11) or g.player.pos == (24, 12) or g.player.pos == (24, 13) or g.player.pos == (24, 14):
            if self.dialog == 0:
                self.dialog = 1
                g.intermission = 1
                self.pan_camera(self.fox)
                self.fox.pos((27, 8))
                self.timer = 0
        if self.dialog == 1:
            str = "Fox:"
            str += "\nI got her"
            self.info_box(str, self.fox)
            self.fox.walkto((28, 13))
            self.assistant.walkto((29, 14))
            self.fox.hidden = 0
            self.assistant.hidden = 0
            if self.switches[0].open:
                self.switches[0].pull_switch()
        elif self.dialog == 2:
            self.assistant.feeling = 'worried'
            str = "..."
            str += "\nGood. "
            self.director.feeling = 'sitawake'
            self.info_box(str, self.director)
        elif self.dialog == 3:
            str = "Take her to the prison."
            self.info_box(str, self.director)
        elif self.dialog == 4:
            str = "What is this?"
            self.info_box(str, self.director)
            self.fox.feeling = 'sad'
        elif self.dialog == 5:
            str = "Fox:"
            str += "\nAh..."
            self.info_box(str, self.fox)
            self.fox.direction = 1
        elif self.dialog == 6:
            str = "Fox:"
            str += "\nIt's her clone she made, Director Victoria"
            self.info_box(str, self.fox)
            self.fox.direction = 1
        elif self.dialog == 7:
            str = "Director Victoria:"
            str += "\nI can see that! You failed to get rid of her illegal friend? Useless!"
            self.info_box(str, self.director)
            self.director.feeling = 'sitangry'
            self.fox.direction = 0
        elif self.dialog == 8:
            str = "Director Victoria:"
            str += "\nThis time get rid of him. Put her in the incarceration hole."
            self.info_box(str, self.director)
            self.fox.feeling = 'normal'
            self.director.feeling = 'normal'
        elif self.dialog == 9:
            self.fox.faceup = 1
            self.assistant.hidden = 1
            self.btimer += 1
            if self.btimer > 40:
                self.director.walkto((36, 14))
                self.fox.faceup = 0
                self.dialog = 10
                self.director.direction = 0
                self.pan_camera(g.player)
        elif self.dialog == 10:
            self.btimer += 1
            if self.btimer > 40:
                # start another boss battle
                self.fox.attacking = 2
                self.fox.health = 50
                self.fox.healthmax = 50
                self.dialog = 11
                g.intermission = 0
        elif self.dialog == 11:
            if self.fox.attacking != 0: # kill the fox!
                self.fox.draw_health_meter()
            else:
                self.dialog = 12
                self.timer = 0
        elif self.dialog == 12:
            str = "Fox:"
            str += "\nNot again!"
            self.info_box(str, self.fox)
            self.pan_camera(self.fox)
            g.intermission = 1
        elif self.dialog == 13:
            str = "Fox:"
            str += "\nWhatever. I'm out of here"
            self.info_box(str, self.fox)
        elif self.dialog == 14:
            g.intermission = 0
            self.fox.jump_out()
            self.dialog = 15
            self.btimer = 0
        elif self.dialog == 15:
            self.btimer += 1
            if self.btimer >= 30:
                self.fox.hidden = 1




        # give a wee message that director locked the door behind her. bitch.
        if g.player.pos == (36, 14):
            if g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                if 'i_jailkey' in g.saveData:
                    g.currentLevel = 34
                else:
                    str = "\nThe door is locked."
                    self.info_box(str)

        
        # the tunnel to the jail pit (prompt player for option)
        if not 'scene18' in g.saveData:
            # director fucks off
            if self.director.hasWalkedTo((36, 14)):
                self.director.hidden = 1
                self.g.tlayer[14][36] = 42
            if g.player.pos == (29, 14) and self.fox.hidden == 1:
                if g.event and g.level.option_gui == 0:
                    g.level.option_gui = 1
                    g.intermission = 1
                    self.contains_msg_box_counter = 0
                    self.pan_camera(None)
            if g.level.option_gui != 0: # dialog open
                str = "\nJump in the pipe?"
                self.info_box(str)
            if g.level.option_gui == 3: #selected yes
                g.level.option_gui = 0
                self.g.currentLevel = 14
                g.intermission = 0
            if g.level.option_gui == 4: #selected no
                g.level.option_gui = 0
                g.intermission = 0
        else:
            self.g.tlayer[14][36] = 42
            self.watertimer += 1
            if self.watertimer % 2 == 0:
                Effect(self.g, 'water', (29 * 32, 14* 32 + 3))

            
        #(7, 14)
        if self.switches[0].open:
           self.g.clayer[14][7] = 0
           self.g.tlayer[14][7] = 7
        else:
           self.g.clayer[14][7] = 1
           self.g.tlayer[14][7] = 9

        # fade in 
        if self.fadein!=0:
            self.fadein += 1
            if self.fadein < 64:
                self.g.player.animation = 1
                self.g.player.dieanimation = 1
                g.intermission = 1
                alpha = self.fadein * 4
                self.g.screen.fill((alpha,alpha,alpha), None, BLEND_MULT)
            else:
                self.g.player.animation = 0
                self.g.player.dieanimation = 0
                g.intermission = 0
                self.fadein = 0

        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        