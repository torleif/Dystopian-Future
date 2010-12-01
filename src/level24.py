""" Battle with a monster. Medical monster. meet ima?! """
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


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 0
    oldPos = (0, 0)
    dialog = 0
    btimer = 0
    lockedatmessage = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new, dimentions)
        self.prevlevel = p
        self.title = 'Underground'
        # current level
        TW,TH = 32,32

        # load tile set
        g.tga_load_tiles(os.path.join("textures",  "tiles5.png"), (TW,TH), self.tdata)
        g.tga_load_level(os.path.join("levels",  "level24.tga"), 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.doctor = Character("monster3a.png", "monster3a.png", self.g, 'doctor')
        self.doctor.pos((25, 20)) # 25, 20

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((33, 27))
        self.assistant.direction = 1
        self.assistant.feeling  = 'coma'

        self.nurse = None # will get set by character.py later on

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))
        self.g.player.hidden = 0
        self.movie = 0
        
        # battled and destoryed the doctor
        if  'scene13' in g.saveData:
            self.doctor.health = 0
            self.nurse = Character("monster4.png", "facenurse.png", self.g, 'nurse')
            self.nurse.pos((29, 27))
            if not 'scene14' in g.saveData:
                self.nurse.feeling = 'dead'



    # ugly, ugly monsters
    def add_monster (self,g,r,a):
        print 'add_monster ',r.rect
        e = Enemy(self.g, (r.rect.x, r.rect.y), 'monster0')

    # upon moving
    def playerMove(self, g,r,a):
        print 'player move'
        if self.prevlevel == 25:
            g.player.rect.x,g.player.rect.y = r.rect.x,r.rect.y - 2
            g.view.x = r.rect.x
            g.view.y = r.rect.y

    # adds a health increase tile
    def add_health_increase (self,g,r,a):
        Inventory(g, 'healthincrease3', (r.rect.x, r.rect.y))
        
    # when you're over a change level tile
    def change_level(self, g,r,a):
        if a.__class__.__name__ != 'Player':
            return
        if g.player.pos[0] == 1:
            g.currentLevel = 23

    # level events
    def level_loop(self):
        g = self.g

        # deciding if the doctor should attack. if it is, lock the player in
        self.g.clayer[27][7] = 1
        self.g.tlayer[27][7] = 25
        if not 'scene13' in g.saveData:
            self.g.clayer[27][7] = 0
            self.g.tlayer[27][7] = 10
            if g.player.pos[0] >= 22:
                self.pan_camera(self.doctor)
                g.intermission = 1
                self.timer += 1
                if self.timer >= 50:
                    g.intermission = 0
                    g.saveData['scene13'] = 1
                    self.doctor.attacking = 1
        # can walk through if you healed the nurse
        if 'scene14' in g.saveData:
            self.g.clayer[27][7] = 0
            self.g.tlayer[27][7] = 10


        if g.player.pos == (33, 27):
            if g.event:
                self.dialog = 1
            if self.dialog == 1:
                str = "..."
                self.info_box(str, self.assistant)


        if g.player.pos == (22, 14) and g.event and g.intermission == 0:
            self.g.player.hidden = 1
            self.movie = 1
            g.intermission = 1
            pos = g.tile_to_screen((22, 14))
            pos = (pos[0] + g.view.x, pos[1] + g.view.y)
            self.lift = Effect(self.g, 'lift', pos)
        if self.movie:
            self.g.tlayer[14][22] = 10
            self.pan_camera(self.lift)
            if self.lift.rect.y < 80:
                g.currentLevel = 25
                g.sprites.remove(self.lift)
                self.pan_camera(None)
                g.intermission = 0

        # the nurse the doctor spat out
        if self.nurse != None:
            if 'scene14' in g.saveData:
                self.nurse.feeling = 'normal'
            if self.nurse.get_pos() == g.player.pos:
                if g.event:
                    if not 'scene14' in g.saveData:
                        self.dialog = 1
                if g.keyup:
                    if 'scene14' in g.saveData:
                        self.dialog += 1
                        self.contains_msg_box_counter = 0

                if self.dialog == 1:
                    if not 'i_medicine' in g.saveData:
                        str = "\nShe looks unconscious"
                        self.info_box(str, self.nurse)
                    else:
                        # give her the spray medicine?
                        if not 'scene14' in g.saveData:
                            if g.level.option_gui == 0:
                                g.level.option_gui = 1
                                g.intermission = 1
                                self.contains_msg_box_counter = 0
                                self.pan_camera(None)
                            if g.level.option_gui != 0: # dialog open
                                str = "Give her the spray medicine?"
                                self.info_box(str)
                            if g.level.option_gui == 3: #selected yes
                                g.saveData['scene14'] = 1
                                self.nurse.feeling = 'normal'
                                g.level.option_gui = 0
                                self.dialog = 1
                                self.contains_msg_box_counter = 0
                            if g.level.option_gui == 4: #selected no
                                g.intermission = 0
                                g.level.option_gui = 0
                                self.dialog = 0
                elif self.dialog == 2:
                    str = "Arg... My head..."
                    self.info_box(str, self.nurse)
                    g.intermission = 1
                elif self.dialog == 3:
                    str = "Where am I?"
                    self.info_box(str,self.nurse)
                elif self.dialog == 4:
                    str = "Gee, your friend looks bad..."
                    self.info_box(str,self.nurse)
                elif self.dialog == 5:
                    str = "It says on her chart she was rejected because her brain had "
                    str += "\nchronic malformation in the limbic system. I guess the doctor had"
                    str += "\n a wee dig around in there. Not good."
                    self.info_box(str,self.nurse)
                elif self.dialog == 6:
                    str = "To restore her you'll need a copy of her brain... If she has one. "
                    str += "\nAnyone will do, but if you don't find her one her memories"
                    str += "\nwill be lost. "
                    self.info_box(str,self.nurse)
                elif self.dialog == 7:
                    g.intermission = 0
                            
            if g.player.pos == (7, 14):
                if g.event:
                    self.dialog = 1
                if self.dialog == 1:
                    str = "The generic nurse unit can acquire access testosterone due to"
                    str += "\nexternal influences. Access aggression can be controlled with a"
                    str += "\nshot of oestrogen, via Diverticula Delivery System (tm) "
                    self.info_box(str)
                    self.lockedatmessage = 1

            # grabbing the medicine from the cabinet
            if g.player.pos == (5, 14):
                if g.event:
                    self.dialog = 1
                if self.dialog == 2:
                    if 'i_medicine' in g.saveData:
                        str = "You take the Diverticula Delivery System (tm) "
                        self.info_box(str)
                if self.dialog == 1:
                    if self.lockedatmessage == 1:
                        #prompt the user to take the medicine
                        if not 'i_medicine' in g.saveData:
                            if g.level.option_gui == 0:
                                g.level.option_gui = 1
                                g.intermission = 1
                                self.contains_msg_box_counter = 0
                                self.pan_camera(None)
                            if g.level.option_gui != 0: # dialog open
                                str = "Take the Diverticula Delivery System (tm)?"
                                self.info_box(str)
                            if g.level.option_gui == 3: #selected yes
                                g.saveData['i_medicine'] = 1
                                g.level.option_gui = 0
                                g.intermission = 0
                                self.dialog = 2
                                self.contains_msg_box_counter = 0
                            if g.level.option_gui == 4: #selected no
                                g.intermission = 0
                                g.level.option_gui = 0
                                self.dialog = 0
                        else:
                            str = "You have taken the Diverticula Delivery System (tm) "
                            self.info_box(str)
                    else:
                        str = "Medicines and gadgets fill the cabinet"
                        self.info_box(str)

        # bug fix
        if g.player.pos != (5, 14) and self.nurse and self.nurse.get_pos() != g.player.pos:
            g.level.option_gui = 0
            g.intermission = 0


        # if you killed the doctor
        if self.doctor.health <= 0:
            #(37, 26)
            self.g.clayer[26][37] = 1
            self.g.tlayer[26][37] = 11
            self.g.clayer[23][37] = 1
            self.g.tlayer[23][37] = 11
            self.g.clayer[20][37] = 1
            self.g.tlayer[20][37] = 11
        else:
            self.g.clayer[26][37] = 0
            self.g.tlayer[26][37] = 10
            self.g.clayer[23][37] = 0
            self.g.tlayer[23][37] = 10
            self.g.clayer[20][37] = 0
            self.g.tlayer[20][37] = 10
            
        if self.oldPos != g.player.pos:
            self.dialog = 0
            self.oldPos = g.player.pos
            self.timer = 0
        