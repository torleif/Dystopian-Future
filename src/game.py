"""<title>An adventure game</title>"""

import pygame
from pygame.rect import Rect
from pygame.locals import *
import os
from player import Player
import pickle
import gc

# import level
import level

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import tilevid, timer

SW,SH = 640,480
TW,TH = 32,32
FPS = 30


# create the player object
def player_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    g.player = Player(g, t)

def save_game(g):
    output = open('save.data', 'wb')
    g.saveData['pos'] = g.player.pos
    g.saveData['currentLevel'] = g.currentLevel
    g.saveData['health'] = g.player.health
    g.saveData['healthmax'] = g.player.healthmax

    pickle.dump(g.saveData, output, -1)
    output.close()
    print 'save game'

def load_game(g):
    try:
        pkl_file = open('save.data', 'rb')
        g.saveData = dict(pickle.load(pkl_file))
        g.loadPosition = g.saveData['pos']
        g.currentLevel = g.saveData['currentLevel']
        g.intermission = 0
        pkl_file.close()
        return 1
    except EOFError:
        return 0
    except IOError:
        return 0

    print 'load game'
    

# init the game
def init():
    print 'init'
    pygame.mixer.init()
    g = tilevid.Tilevid()
    g.player = None
    g.view.w,g.view.h = SW,SH
    g.shaking_screen = 0
    def shake_screen():
        g.shaking_screen = 1
    g.shake_screen = shake_screen
    pygame.display.set_icon( pygame.image.load("icon.png"))
    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    pygame.display.set_caption('Dystopian Future')
    g.removeOnLeave = []
    g.bullets = []
    g.save = save_game
    g.tmpPlayerPos = None # when chaning levels

    g.drawhealth = 0
    g.healthmax = 0
    g.following = None
    g.connected = 0

    # data that gets saved
    g.saveData = {}
    g.saveData['displayhealth'] = 0
    g.saveData['weapon'] = 0
    g.saveData['shot1'] = 0
    g.saveData['shot2'] = 0
    g.saveData['shot4'] = 0
    g.saveData['shot5'] = 0
    g.saveData['shot7'] = 0
    g.saveData['shot1_lvl'] = 0 #each weapon level
    g.saveData['shot2_lvl'] = 0
    g.saveData['shot4_lvl'] = 0
    g.saveData['shot7_lvl'] = 0
    g.saveData['health'] = 4
    g.saveData['healthmax'] = 4

    # player texture
    idata = [
        ('player',      os.path.join("textures",  "player.png"),    (0,0,32,32)),
        ('inventory',   os.path.join("textures",  "inventory.png"), (0,0,32,32)),
        ('bird',        os.path.join("textures",  "bird.tga"),      (0,0,32,32)),
        ('rat',         os.path.join("textures",  "rat.tga"),       (0,0,32,32)),
        ('monster0',    os.path.join("textures",  "monster0.png"),  (0,0,32,32)),
        ('monster1',    os.path.join("textures",  "monster1.png"),  (0,0,32,64)),
        ('monster2',    os.path.join("textures",  "monster2.png"),  (0,0,32,32)),
        ('nurse',       os.path.join("textures",  "monster4.png"),  (0,0,32,32)),
        ('monster5',    os.path.join("textures",  "monster5.png"),  (0,0,32,32)),
        ('monster6',    os.path.join("textures",  "monster6.png"),  (0,0,32,32))
    ]
    g.load_images(idata)
    # bounds of the rect
    pygame.font.init()

    # sound effects
    g.shootSound1 = pygame.mixer.Sound(os.path.join("effects",  "shoot1.wav"))
    g.shootSound2 = pygame.mixer.Sound(os.path.join("effects",  "shoot2.wav"))
    g.shootSound3 = pygame.mixer.Sound(os.path.join("effects",  "shoot3.wav"))
    g.shootSound4 = pygame.mixer.Sound(os.path.join("effects",  "shoot4.wav"))
    g.shootSound5 = pygame.mixer.Sound(os.path.join("effects",  "shoot5.wav"))
    g.sel = pygame.mixer.Sound(os.path.join("effects",  "sel.wav"))
    #g.shootSound2.set_volume(.4)
    shootSoundFile = os.path.join("effects",  "hurt.wav")
    g.hurt = pygame.mixer.Sound(shootSoundFile)
    g.hurt.set_volume(.5)
    shootSoundFile = os.path.join("effects",  "exp2.wav")
    g.exp2 = pygame.mixer.Sound(shootSoundFile)

    g.exp3 = pygame.mixer.Sound(os.path.join("effects",  "exp3.wav"))
    g.exp4 = pygame.mixer.Sound(os.path.join("effects",  "exp4.wav"))
    g.exp5 = pygame.mixer.Sound(os.path.join("effects",  "exp5.wav"))
    
    # entering a new level
    g.enterLevelSound = pygame.mixer.Sound(os.path.join("effects",  "enter.wav"))

    # fonts
    g.font = pygame.font.Font('seven.ttf', 14)
    g.player = None
    g.level = level.LevelBase(g, player_new, (SW,SH))
    g.event = 0

    getItemSoundFile = os.path.join("effects",  "pickup.wav")
    g.pickup = pygame.mixer.Sound(getItemSoundFile)

    # data loaded
    return g


def run(g): 
    g.quit = 0
    g.pause = 0
    g.currentLevel = 0
    g.intermission = 0
    g.keyup = 0
    clevel = 0
    g.inTitle = 1
    g.dead = 0
    g.loadPosition = None
    g.disable_fire = 1
    selection = 1
    t = timer.Timer(FPS)
    deadmsg = 0

    while not g.quit:
        g.event = 0
        g.keyup = 0
        # events
        for e in pygame.event.get():
            if e.type is QUIT: g.quit = 1
            if e.type is KEYDOWN:
                if e.key == K_ESCAPE: g.quit = 1
                if e.key == K_F10 or e.key == K_f:
                    pygame.display.toggle_fullscreen()
                if e.key == K_RETURN:
                    g.pause ^= 1
                if e.key == K_DOWN:
                    g.event = 1
                    # get the players position
                    if g.event and g.player:
                        print g.player.pos ," (",g.player.rect.x,g.player.rect.y,")"
                if not g.inTitle:
                    if e.key == K_s:
                        g.level.inventory_gui += 1
                    if e.key == K_a:
                        g.level.inventory_gui -= 1
                    if e.key == K_v:
                        g.level.weapon_gui += 1
                    if e.key == K_c:
                        g.level.weapon_gui -= 1
                    if (e.key == K_z or e.key == K_RETURN) and (g.level.weapon_gui != 0 or g.level.inventory_gui != 0):
                        g.level.select_gui = 1
            if e.type is KEYUP:
                g.keyup = 1
                #if e.key == K_SPACE and not g.inTitle:
                    #g.player.shotcounter = 0

        # running code
        if not g.pause and not g.inTitle:
            g.screen.fill((0,0,0))
            g.level.draw_back()
            g.level.tick_msg_box()
            g.loop()
            g.level.loop_render() # hack to get ima holding hands right
            if g.shaking_screen != 0:
                if g.shaking_screen == 1:
                    g.startshakey = g.view.y
                g.shaking_screen += 1
                g.view.y = g.startshakey + ((g.shaking_screen % 3)-1) * 50 / g.shaking_screen
                if(g.shaking_screen > 20):
                    g.shaking_screen = 0
            g.paint(g.screen)
            if g.dead == 1:
                if deadmsg == 0:
                    g.level.info_box("\nYou have died.")
                    if g.level.contains_msg_box_counter > 30:
                        if g.keyup:
                            g.level.contains_msg_box_counter = 0
                            deadmsg = 1
                            g.level.option_gui = 1
                if deadmsg == 1:
                    g.level.info_box("\nRety?")
                if g.level.option_gui == 3: #selected yes
                    load_game(g)
                    g.level.option_gui = 0
                    g.dead = 0
                    deadmsg = 0
                    clevel = -1
                if g.level.option_gui == 4: #selected no
                    g.quit = 1
                    g.level.option_gui = 0

            g.level.level_loop()
            g.level.draw_gui()
            pygame.display.flip()
        
        # if in the loading title screen
        if g.inTitle:
            g.disable_fire = 1
            keys = pygame.key.get_pressed()
            g.screen.fill((0,0,0))
            img = g.font.render('New',1,(255,255,255))
            g.screen.blit(img, (SW / 2-30,SH/2))
            img = g.font.render('Load',1,(255,255,255))
            g.screen.blit(img, (SW / 2-30,SH/2+30))
            if keys[K_UP]:
                if selection != 1:
                    g.sel.play()
                selection = 1
            if keys[K_DOWN]:
                if selection != 2:
                    g.sel.play()
                selection = 2
            if selection == 1:
                img = g.font.render('>',1,(255,255,255))
                g.screen.blit(img, (SW / 2-45,SH/2))
                if keys[K_SPACE] or keys[K_RETURN] or keys[K_z]:
                    g.inTitle = 0
                    clevel = -1
                    g.currentLevel = 0
            if selection == 2:
                img = g.font.render('>',1,(255,255,255))
                g.screen.blit(img, (SW / 2-45,SH/2+30))
                if keys[K_SPACE] or keys[K_RETURN] or keys[K_z]:
                    if load_game(g):
                        clevel = -1
                        g.inTitle = 0
            pygame.display.flip()

        # changing to a new level (put an eval here? lol)
        if g.currentLevel != clevel:
            print 'Change to level :' ,g.currentLevel
            g.level.leave()
            level_name = "level" + str(g.currentLevel)
            try:
                loadedLevelModule = __import__(level_name)
                g.level = loadedLevelModule.Level(g, player_new, (SW,SH), clevel)
            except ImportError as inst:
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to printed directly
                print level_name, " failed to load"
                print ImportError
            
            clevel = g.currentLevel
            g.saveData['level'] = clevel
            gc.collect()
        # cleaning up
        t.tick()
run(init())