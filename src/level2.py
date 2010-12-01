""" Engineers Lab """
import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from level import LevelBase
import sys; sys.path.insert(0, "..")
from pgu import tilevid, timer
from character import Character
from inventory import Inventory


class Level(LevelBase):
    prevlevel = 0
    dialog = 0
    pdialog = 0
    timer = 10
    ticker = 0
    
    def __init__(self, g, player_new, dimentions, p = 0):
        LevelBase.__init__(self, g, player_new,dimentions)
        self.prevlevel = p
        self.title = 'Engineers Lab'

        # current level
        currentLevel = os.path.join("levels",  "level2.tga")

        TW,TH = 32,32

        # load tile set
        tileTexture = os.path.join("textures",  "tiles0.png")
        g.tga_load_tiles(tileTexture, (TW,TH), self.tdata)
        g.tga_load_level(currentLevel, 1)
        g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
        g.code_events(self.edata)

        self.microwave = Inventory(g, 'microwave')
        self.microwave.pos((6, 9))

        self.professor = Character("professor.png","faceprofessor.tga", g)
        self.professor.pos((6, 9))
        self.professor.direction = 0

        self.assistant = Character("assistant.png","faceassistant.png", g)
        self.assistant.pos((12, 9))
        self.assistant.direction = 1
        
        g.intermission = 1

        # already done the cut scene
        if 'scene1' in g.saveData:
            g.intermission = 0
            self.professor.pos((11, 9))
            self.dialog = 9
            self.g.sprites.remove(self.assistant)

        # if you've put the transmitter in
        if 'scene3' in g.saveData:
            self.assistant = Character("assistant.png","faceassistant.png", g)
            self.assistant.pos((13, 9))
            self.professor.pos((8, 9))
            self.assistant.direction = 1
            self.dialog = 10
            g.intermission = 1
        
        # already had the talk after putting in the transmitter
        if 'scene4' in g.saveData:
            self.dialog = 19
            g.intermission = 0
            self.g.sprites.remove(self.assistant)

        if 'scene5' in g.saveData:
            self.dialog = 20
            self.professor.pos((11,9))
            self.professor.faceup = 1

        g.run_codes(self.cdata,(0,0,g.dimentions[0],g.dimentions[1]))

    # upon moving
    def playerMove(self, g,r,a):
        if self.prevlevel == 3:
            g.player.rect.x = r.rect.x
            g.player.rect.y = r.rect.y
        if self.prevlevel == 5:
            # why do you eat so much chicken?
            pop = g.tile_to_screen((6,9))
            g.player.rect.x = pop[0]
            g.player.rect.y = pop[1]

    # when you're over a change level tile
    def change_level(self, g,r,a):
        if not g.event or a.__class__.__name__ != 'Player':
            return

        #back to castle st
        if g.player.pos == (1, 9):
            self.g.currentLevel = 1
        if g.player.pos == (13, 9):
            self.g.currentLevel = 3

        # The door is open
        if 'scene4' in g.saveData:
            if g.player.pos == (7, 9):
                g.currentLevel = 5


    # draw back of level
    def draw_back(self):
        test = self.draw_gradent((18,20,34), (0, 0, 0))
        self.g.screen.blit(test, (0,0))

        # blinking machines
        if self.ticker % 7 == 0:
            w,h = self.g.dimentions[0], self.g.dimentions[1]
            for y in range(0,h):
                for x in range(0,w):
                    if self.g.tlayer[y][x] == 47:
                        self.g.tlayer[y][x] = 63
                    elif self.g.tlayer[y][x] == 63:
                        self.g.tlayer[y][x] = 47


        # open the door
        if 'scene4' in self.g.saveData:
            w,h = self.g.dimentions[0], self.g.dimentions[1]
            for y in range(0,h):
                for x in range(0,w):
                    if self.g.tlayer[y][x] == 1:
                        self.g.tlayer[y][x] = 55



    # level events
    def level_loop(self):
        g = self.g
        # if the key is up
        if g.keyup and self.timer > 30 and self.dialog != 9 and self.dialog != 19 and self.dialog != 20:
            self.dialog += 1
            self.timer = 0
            self.contains_msg_box_counter = 0

        # dialog bs
        if self.dialog == 0:
            self.professor.faceup = 1
        elif self.dialog == 1:
            self.professor.faceup = 0
            str = "I've completed the testing of the microwave transmitter."
            str += "\nI'll put the cover on it and it will be fixed."
            self.info_box(str, self.professor)
        elif self.dialog == 2 :
            self.professor.walkto((11, 9))
            if self.professor.hasWalkedTo((11, 9)):
                self.professor.faceup = 1
                str = "I don't know how I'll manage to fix it again; "
                str += "\nThe solder is rusted and the components have decayed. If"
                str += "\nthey want us to do it again they'll need to supply us correctly."
                self.info_box(str, self.professor)
        elif self.dialog == 3:
            self.professor.faceup = 0
            str = "Hehe!"
            str += "\nThere's a visitor in the door"
            self.info_box(str, self.assistant)
        elif self.dialog == 4:
            str = "A visitor?"
            self.professor.direction = 1
            self.info_box(str, self.professor)
        elif self.dialog == 5:
            self.professor.walkto((3, 9))
            self.assistant.walkto((4, 9))
            if self.professor.hasWalkedTo((3, 9)):
                str = "You're a face I haven't seen before..."
                self.info_box(str, self.professor)
        elif self.dialog == 6:
            str = "The ID sown to your speed suit is GARD01 2454"
            self.info_box(str, self.professor)
        elif self.dialog == 7:
            self.professor.direction = 0
            str = "You wouldn't happen to know where this man came from,"
            str += "\ndo you, Ima?"
            str += "\n"
            self.info_box(str, self.professor)
        elif self.dialog == 8:
            self.professor.direction = 1
            str = "Well I'm sure you wouldn't helping her take the microwave "
            str += "\ntransmitter to the clock tower and install it. It shouldn't"
            str += "\ntake long."
            self.info_box(str, self.professor)
        elif self.dialog == 9:
            # enable walking
            g.intermission = 0

            # professor goes back to working
            self.professor.direction = 0
            self.professor.walkto((11, 9))

            if self.professor.hasWalkedTo((11, 9)):
                self.professor.faceup = 1

            if self.assistant in self.g.sprites:
                g.following = self.assistant
            g.saveData['scene1'] = 1
            
            # asking the professor what to do
            if g.player.pos == (11,9) and g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "You can get to the tower using the door to my right."
                str += "\nMake sure to take the transmitter!"
                self.info_box(str, self.professor)
        elif self.dialog == 10:
            self.assistant.walkto((11, 9))
            self.professor.walkto((10, 9))
            g.player.direction = 1
            if self.assistant.hasWalkedTo((11, 9)):
                self.professor.faceup = 0
                str = "Back already?"
                self.info_box(str, self.professor)
        elif self.dialog == 11:
            str = "Good work. This means we can go home for the day."
            self.info_box(str, self.professor)
        elif self.dialog == 12:
            self.assistant.walkto((10, 9))
            self.professor.walkto((11, 9))
            if self.professor.hasWalkedTo((11, 9)):
                self.assistant.direction = 0
                str = "What about you?"
                self.info_box(str, self.professor)
        elif self.dialog == 13:
            str = "The last thing you remember is getting paid for a medical trail?"
            str += "\nAh yes. To be an undergraduate again..."
            str += "\nWonderful times!"
            self.info_box(str, self.professor)
        elif self.dialog == 14:
            str = "Ima:"
            str += "\nEngineer?"
            self.info_box(str, self.assistant)
        elif self.dialog == 15:
            str = "Engineer:"
            self.professor.direction = 1
            str += "\nI'd imagine you have the responsibility of caring for your"
            str += "\nnew friend."
            self.info_box(str, self.professor)
        elif self.dialog == 16:
            self.professor.direction = 0
            str = "Engineer:"
            str += "\nTake this, you can use it to protect yourself."
            str += "\nI made it myself."
            self.info_box(str, self.professor)
        elif self.dialog == 17:
            str = "\nReceived the Crux!"
            g.saveData['weapon'] = 1
            g.saveData['displayhealth'] = 1
            self.info_box(str)
        elif self.dialog == 18:
            str = "Engineer:"
            str += "\nI'll open the door."
            self.info_box(str, self.professor)
            self.assistant.direction = 1
        elif self.dialog == 19:
            g.intermission = 0
            g.saveData['scene4'] = 1
            self.professor.walkto((11, 9))
            # walk the assistant to the door and remove her.
            if self.assistant in self.g.sprites:
                self.assistant.walkto((7, 9))
                if self.assistant.hasWalkedTo((7, 9)):
                    self.g.sprites.remove(self.assistant)

            # a small message to the player about the monsters outside
            if g.player.pos == (11,9) and g.event:
                self.pdialog = 1
            if self.pdialog == 1:
                str = "Engineer:"
                str += "\nThe weapon works by locating erroneous DNA left by"
                str += "\nmodified creatures, and storing it for reproduction."
                self.info_box(str, self.professor)
        elif self.dialog == 20: # if you've killed the fox, and Ima's been kidnapped
            if g.player.pos == (11,9) and g.event:
                g.intermission = 1
                self.dialog = 21
                self.timer = 0
        elif self.dialog == 21: # if you've killed the fox, and Ima's been kidnapped
            str = "Engineer:"
            str += "\nWhat? Ima's been kidnapped?! By a giant pumpkin?"
            self.professor.walkto((12,9))
            self.professor.direction = 1
            self.info_box(str, self.professor)
            self.professor.faceup = 0
            g.player.direction = 0
        elif self.dialog == 22:
            str = "Engineer:"
            str += "\nI know who he is. His name is Fox. "
            self.info_box(str, self.professor)
        elif self.dialog == 23:
            str = "Engineer:"
            str += "\nHe was made by terrorists, but found work with the "
            str += "\nNews Corperation."
            self.info_box(str, self.professor)
        elif self.dialog == 24:
            str = "Engineer:"
            str += "\n...The world has changed since you were last awake. A long time "
            str += "\nago terrorists got their hands on genetic manipulation equipment."
            self.info_box(str, self.professor)
        elif self.dialog == 25:
            str = "Engineer:"
            str += "\nAcross the globe people were attacked with cheap explosives,"
            str += "\npoisons and modified creatures."
            self.info_box(str, self.professor)
        elif self.dialog == 26:
            str = "Engineer:"
            str += "\nPeople found refuge underground. The only people on top"
            str += "\nare maintainers to their system they live in."
            self.info_box(str, self.professor)
        elif self.dialog == 27:
            str = "Engineer:"
            str += "\nLaw does not permit us to copy people, and Ima copied you. "
            str += "\nSo News Corp. must have sent someone take her..."
            self.info_box(str, self.professor)
        elif self.dialog == 28:
            str = "Engineer:"
            str += "\nYou'll have to go and get her. They probably just want"
            str += "\nto set an example anyway."
            self.info_box(str, self.professor)
        elif self.dialog == 29:
            str = "Engineer:"
            str += "\nGet to the Octagon were their office is and take her back."
            self.info_box(str, self.professor)
        elif self.dialog == 30:
            g.intermission = 0
            g.saveData['scene6'] = 1




        self.timer += 1
        self.ticker += 1
        # remmber last pos so I can remove old dialoge boxes
        if self.oldPos != g.player.pos:
            self.pdialog = 0
        self.oldPos = g.player.pos