from . import Explosion
from utils import collision
from random import randint
from math import cos, sin, pi
import settings
import pygame


class Bullet:

    def __init__(self):
        self.name = "bullet"
        self.img = pygame.image.load("imgs/bluebullet32.png")
        self.damage = 1
        self.ammo = 3
        self.hp = 3
        self.xpos = randint(0, settings.SCREEN_WIDTH - 64)
        self.ypos = randint(-192, -64)
        self.theta = pi / 2
        self.onfire = False
        self.vel = 4
        self.explosion = Explosion()
        self.destroyed = False

    def move(self, source="fromplayer"):
        if self.onfire:
            width = self.img.get_rect()[2]
            height = self.img.get_rect()[3]
            self.xpos = self.xpos + (self.vel * cos(self.theta))
            self.ypos = self.ypos - (self.vel * sin(self.theta))

            if source == "fromplayer":
                self.onfire = False if self.ypos < -height else True
            else:
                self.onfire = False if (self.ypos > 600 or self.xpos < -width or self.xpos > 800) else True

    def bring_to_ship(self, source):
        self.destroyed = False
        width1 = source.img.get_rect()[2] / 2
        height1 = source.img.get_rect()[3] / 2
        width2 = self.img.get_rect()[2] / 2
        height2 = self.img.get_rect()[3] / 2
        if not self.onfire:
            self.xpos = source.xpos + width1 - width2
            self.ypos = source.ypos + height1 - height2

    def hide(self):
        self.xpos = 0
        self.ypos = -600

    def explode(self):
        self.explosion.show(self.xpos + 32, self.ypos + 32)
        self.onfire = False
        self.hp = 3
        self.hide()

    def detect_collision(self, objects, player, energy_gauge):
        for i in range(self.ammo):
            if self.onfire:
                center_x1 = self.xpos + self.img.get_rect()[2] / 2
                center_y1 = self.ypos + self.img.get_rect()[3] / 2
                for j in range(len(objects)):
                    center_x2 = objects[j].xpos + objects[j].img.get_rect()[2] / 2
                    center_y2 = objects[j].ypos + objects[j].img.get_rect()[3] / 2
                    dist = (self.img.get_rect()[2] + objects[j].img.get_rect()[2]) * 0.93 / 2
                    if collision(center_x1, center_y1, center_x2, center_y2, dist):
                        self.onfire = False
                        objects[j].explosion.frame = 0
                        if objects[j].hp <= self.damage:
                            objects[j].explosion.size = "large"
                            objects[j].explode()
                            pygame.mixer.Sound("musics/asteroid_collision.wav").play(0, 0, 400)
                            energy_gauge.update(player.energy*2.5)
                        else:
                            objects[j].hp -= self.damage
                            objects[j].explosion.size = "small"
                            objects[j].explosion.show(self.xpos + 16, self.ypos + 16)
                            pygame.mixer.Sound("musics/drone_collision.wav").play(0, 0, 400)
                        break

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(self.img, (round(self.xpos), round(self.ypos)))
