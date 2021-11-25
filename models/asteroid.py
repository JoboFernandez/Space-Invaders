from . import Explosion
from random import randint, choice
import settings
import pygame


class Asteroid:

    def __init__(self):
        self.name = "asteroid"
        self.img = pygame.image.load("imgs/meteor64.png")
        self.hp = 1
        self.xpos = randint(0, settings.SCREEN_WIDTH - 64)
        self.ypos = randint(-settings.SCREEN_HEIGHT, -64)
        self.xvel = 3 * choice([-0.15, -0.1, 0.1, 0.15])
        self.yvel = 3 * choice([0.4, 0.5, 0.6])
        self.explosion = Explosion()
        self.destroyed = False

    def move(self):
        self.xpos += self.xvel
        self.ypos += self.yvel
        if self.xpos < 0 or self.xpos > 736: self.xvel *= -1
        if self.ypos > 600:
            self.xvel *= 1.075
            self.yvel *= 1.075
            self.explode()

    def explode(self):
        self.explosion.show(self.xpos + 32, self.ypos + 32)
        self.xpos = randint(0, settings.SCREEN_WIDTH - 64)
        self.ypos = randint(-settings.SCREEN_HEIGHT, -64)
        self.hp = 1

    def hide(self):
        self.xpos = 0
        self.ypos = -600
        self.xvel = 0
        self.yvel = 0

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(self.img, (round(self.xpos), round(self.ypos)))
        screen.blit(self.explosion.img, (round(self.explosion.left), round(self.explosion.top)))