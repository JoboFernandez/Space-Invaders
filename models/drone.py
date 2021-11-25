from . import Bullet, Explosion
from math import atan, fabs, pi
from random import randint
import settings
import pygame


class Drone:

    def __init__(self):
        self.name = "drone"
        self.img = pygame.image.load("imgs/drone128.png")
        self.xpos = randint(0, settings.SCREEN_WIDTH - 128)
        self.ypos = randint(0,100)
        self.angle = 0
        self.angle_vel = 0.065
        self.hp = 15
        self.explosion = Explosion()
        self.bullet = Bullet()
        self.bullet.img = pygame.image.load("imgs/bomb64.png")
        self.bullet.vel = 3
        self.fire_delay = 2000 + randint(0, 1000)
        self.last_fire = pygame.time.get_ticks()
        self.destroyed = False

    def hide(self):
        self.xpos = 0
        self.ypos = -600

    def explode(self):
        self.explosion.show(self.xpos + 64, self.ypos + 64)
        self.hide()
        self.destroyed = True

    def follow(self, target):
        if not self.destroyed:
            x_accuracy, y_accuracy = randint(int(target.xpos), int(target.xpos + 62)), target.ypos
            x_delta = x_accuracy - (self.xpos + 64)
            y_delta = y_accuracy - (self.ypos + 64)
            theta = atan(fabs(x_delta) / fabs(y_delta)) * 180 / pi

            if x_delta < 0:
                theta *= -1

            if self.angle > theta:
                self.angle -= self.angle_vel
            else:
                self.angle += self.angle_vel

            if self.angle <= -60:
                self.angle = -60
            elif self.angle >= 60:
                self.angle = 60

            if fabs(self.angle - theta) < self.angle_vel:
                now = pygame.time.get_ticks()
                if now - self.last_fire > self.fire_delay and not self.bullet.onfire:
                    self.last_fire = now
                    self.bullet.theta = (self.angle - 90) * pi / 180
                    self.bullet.bring_to_ship(self)
                    pygame.mixer.Sound("musics/dronebullet_fired.wav").play(0,0,0)
                    self.bullet.onfire = True
                    self.angle_vel *= 1.075
                    self.bullet.vel *= 1.075

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(self.bullet.img, (round(self.bullet.xpos), round(self.bullet.ypos)))
        screen.blit(self.bullet.explosion.img, (round(self.bullet.explosion.left), round(self.bullet.explosion.top)))
        screen.blit(pygame.transform.rotate(self.img, self.angle), (round(self.xpos), round(self.ypos)))
        screen.blit(self.explosion.img, (round(self.explosion.left), round(self.explosion.top)))
