""" Jail 1 """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from character import Character
from inventory import Inventory


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    btimer = 0
    fillingwithwater = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Jail'

        # current level
        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles5.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        currentLevel = os.path.join("levels",  "level14.tga")
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.robot = Character("robot0.png","facerobot.tga", g,'robot')
        self.robot.pos((13, 20))
        self.robot.direction = 0
        
        #(2, 3) 'i_arms' in g.saveData
        self.arms = Inventory(g, 'arms')
        self.arms.pos((2,3))

        # if you've given her arms
        if 'scene7' in g.saveData:
            self.dialog = 6
            self.robot.feeling = 'arms'

        # if you read the newspaper, she fights you to get to the top
        self.newspaper = 0
        if 'scene17' in g.saveData:
            self.newspaper = Inventory(g, "newspaper")
            self.newspaper.pos((6, 20))

        if 'scene19' in g.saveData:
            self.robot.feeling = 'dead'
            self.robot.hidden = 1

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 15:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos[0] == 38:
            g.currentLevel = 15

    # level events
    def level_loop(self):
        g = self.g

        if 'scene7' in g.saveData:
            self.g.clayer[4][18] = 0
            self.g.tlayer[4][18] = 1
        else:
            self.g.clayer[4][18] = 1
            self.g.tlayer[4][18] = 25

        # player position
        if g.player.pos == (13, 20) and not 'scene18' in g.saveData:
            if g.event:
                self.pdialog = 1
                if 'i_arms' in g.saveData:
                    self.pdialog = 2
            if self.pdialog == 0:
                if not 'scene7' in g.saveData:
                    self.robot.feeling = 'blink'
            if self.pdialog == 1:
                self.dialog = 0
                self.robot.feeling = ''
                str = "Hello! Welcome to the Octagon Correctional Facility."
                str += "\nYou must be a visitor, as you weren't tagged when you arrived."
                str += "\nI'd love to help you, but I've misplaced my arms."
                self.info_box(str, self.robot)
            elif self.pdialog == 2:
                if g.keyup and self.timer > 30:
                    self.dialog += 1
                    self.timer = 0
                    self.contains_msg_box_counter = 0
                if 'scene7' in g.saveData and self.dialog == 1:
                    self.dialog = 6 # if you already got the item
                if self.dialog == 1:
                    self.robot.feeling = 'happy'
                    str = "Ah! you found some arms!"
                    g.intermission = 1
                    g.player.staylooking = 1
                    self.info_box(str, self.robot)
                elif self.dialog == 2:
                    self.robot.feeling = 'arms'
                    str = "Thank you"
                    g.saveData['i_arms'] = 0
                    g.player.staylooking = 1
                    self.info_box(str, self.robot)
                elif self.dialog == 3:
                    self.robot.feeling = 'arms'
                    str = "Ima? Yes a girl was automatically transferred to a holding cell "
                    str += "\nacross to the jail. She's been stored in a cell across the complex. "
                    self.info_box(str, self.robot)
                    g.player.staylooking = 1
                elif self.dialog == 4:
                    str = "I'll open the door for you so you can get out."
                    self.info_box(str, self.robot)
                    g.player.staylooking = 1
                elif self.dialog == 5:
                    g.saveData['scene7'] = 1
                    g.player.staylooking = 0
                    g.intermission = 0
                    self.dialog = 7
                elif self.dialog == 6:
                    self.robot.feeling = 'arms'
                    str = "Your friend was automatically transferred to a holding cell."
                    self.info_box(str, self.robot)

        if 'scene17' in g.saveData:
            if not 'scene18' in g.saveData:
                if self.newspaper and self.newspaper.gotten:
                    if g.intermission == 0:
                        self.timer = 0
                    str = "What are you doing? Don't touch that!"
                    self.info_box(str, self.robot)
                    g.intermission = 1
                    g.player.direction = 0
                    if g.keyup and self.timer > 30:
                        g.saveData['scene18'] = 1
                        g.intermission = 0
                        self.robot.attacking = 1

        if self.robot.attacking != 0 and self.robot.feeling != 'dead':
            self.robot.draw_health_meter()
            self.g.clayer[17][18] = 1
            self.g.tlayer[17][18] = 11
        else:
            self.g.clayer[17][18] = 0
            self.g.tlayer[17][18] = 10

        if self.robot.feeling == 'dead':
            if not 'scene19' in g.saveData:
                Inventory(self.g, 'drawingwater', (192, 536 - 64))
                Inventory(self.g, 'waterfall', (15 * 32, 16 * 32))
                g.shake_screen()
                g.player.maxspeed = 3
                g.player.jump_gravity = 7
                self.fillingwithwater = 1
            g.saveData['scene19'] = 1

        # filling the level with water
        if (self.fillingwithwater != 0):
            self.fillingwithwater += 1
            self.g.clayer[17][18] = 1
            self.g.tlayer[17][18] = 11
            

            if self.fillingwithwater > 450 and self.fillingwithwater < 550:
                self.info_box("\nYou can't hold your breath for much longer.")

            if self.fillingwithwater > 750 and self.fillingwithwater < 850:
                self.info_box("\nYou are feeling lightheaded")


            # fade to black when dead
            fadouttime = 1000
            if self.fillingwithwater > fadouttime and self.fillingwithwater < fadouttime+64:
                g.intermission = 1
                self.g.player.animation = 1
                self.g.player.dieanimation = 1
                alpha = 255 - (self.fillingwithwater - fadouttime) * 4
                self.g.screen.fill((alpha,alpha,alpha), None, BLEND_MULT)
            if self.fillingwithwater >= fadouttime+64:
                self.g.screen.fill((0,0,0))
                self.g.player.animation = 0
                self.g.player.dieanimation = 0
            if self.fillingwithwater > 1100:
                g.currentLevel = 13




        #(15, 16) test


        # if you're moving
        if self.oldPos != g.player.pos:
            self.pdialog = 0
            self.dialog = 0
        self.oldPos = g.player.pos
        self.timer += 1

        