""" a little drip """
from pygame.locals import *
import random
import sys; sys.path.insert(0, "..")
from enemy import Enemy
from enemies.drop import Drop




class Drip(Enemy):
    """ a water dripping in a cave

    """

    def __init__(self, g, pos):
        Enemy.__init__(self, g, pos, 'drop')
        self.frm1 = g.images['inventory'][0].subsurface((0 * 32, 8 * 32, 32, 32))
        self.frm2 = g.images['inventory'][0].subsurface((1 * 32, 8 * 32, 32, 32))
        self.frm3 = g.images['inventory'][0].subsurface((2 * 32, 8 * 32, 32, 32))
        self.frm4 = g.images['inventory'][0].subsurface((3 * 32, 8 * 32, 32, 32))
        self.timer = random.randint(0, 50)
    # behavour
    def loop(self, g, r):
        frme = (self.timer / 3) % 30
        if frme == 1:
            self.image = self.frm2
        elif frme == 2:
            self.image = self.frm3
        elif frme == 3:
            self.image = self.frm4
        elif frme == 4:
            #Enemy(g, (self.rect.x, self.rect.y), 'drop')
            Drop(g, (self.rect.x, self.rect.y))
            self.timer += 3 # hack. to the next frame
        else:
            self.image = self.frm1
        self.timer += 1

    # walk away from the wall
    def rebound(self, h):
        if h == 1:
            self.flying = 0
        elif h == 2:
            self.vecx = -5
        elif h == 3:
            self.vecx = 5