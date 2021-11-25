from . import Asteroid
from utils import collision
from math import pi, sin, cos, hypot, atan, fabs
import settings
import pygame


class Weapon:

    def __init__(self):
        self.name = settings.WEAPON_LIST[0]
        self.img = settings.WEAPON_IMAGES[0]
        self.count = 1
        self.damage = 3
        self.xpos = [0]
        self.ypos = [0]
        self.vel = 8
        self.onfire = [False]
        self.theta = [pi/2]
        self.explosion_radius = 0
        self.track = None
        self.nearest_object = Asteroid()
        self.detonate = False
        self.detonation_time = pygame.time.get_ticks()
        self.detonation_x = 0
        self.detonation_y = 1000
        self.xdir = ""
        self.ydir = ""
        self.detecting = False

    def change_weapon(self, name):
        if name == "TPF7":
            self.name = settings.WEAPON_LIST[0]
            self.img = settings.WEAPON_IMAGES[0]
            self.count = 7
            self.xpos = [0 for i in range(self.count)]
            self.ypos = [0 for i in range(self.count)]
            self.vel = 4
            self.onfire = [False for i in range(self.count)]
            self.theta = [-pi/2 + i * pi/6 for i in range(self.count)]
            self.explosion_radius = 50
        elif name == "MARUNA":
            self.name = settings.WEAPON_LIST[1]
            self.img = settings.WEAPON_IMAGES[1]
            self.count = 2
            self.xpos = [0 for _ in range(self.count)]
            self.ypos = [0 for _ in range(self.count)]
            self.vel = 4
            self.onfire = [False for _ in range(self.count)]
            self.theta = [pi/4 for _ in range(self.count)]
            self.explosion_radius = 0
        else:
            self.name = settings.WEAPON_LIST[2]
            self.img = settings.WEAPON_IMAGES[2]
            self.count = 1
            self.xpos = [0]
            self.ypos = [0]
            self.vel = 3
            self.onfire = [False]
            self.theta = [pi / 2]
            self.explosion_radius = 200

    def bring_to_ship(self, object):
        for i in range(self.count):
            if self.name == settings.WEAPON_LIST[1]:
                self.xpos[i] = object.xpos + i * ((object.img.get_rect()[2] - 32) / (self.count - 1))
            else:
                self.xpos[i] = object.xpos + 32 - 16
            self.ypos[i] = object.ypos + 32 - 16

    def track(self, object):
        self.track = object

    def move(self):
        for i in range(self.count):
            if self.onfire[i]:
                if self.name == settings.WEAPON_LIST[0]:
                    self.xpos[i] += self.vel * sin(self.theta[i])
                    self.ypos[i] -= self.vel * cos(self.theta[i])
                elif self.name == settings.WEAPON_LIST[1]:
                    self.ypos[i] -= self.vel
                else:
                    self.follow(self.nearest_object)
                if self.ypos[i] < -32 or self.xpos[i] < -32 or self.xpos[i] > 800:
                    self.onfire[i] = False
            else:
                self.xpos[i] = 0
                self.ypos[i] = 1200

    def detect_collision(self, objects):
        for i in range(self.count):
            if self.onfire[i]:
                center_x1 = self.xpos[i] + self.img.get_rect()[2] / 2
                center_y1 = self.ypos[i] + self.img.get_rect()[3] / 2
                for j in range(len(objects)):
                    center_x2 = objects[j].xpos + objects[j].img.get_rect()[2] / 2
                    center_y2 = objects[j].ypos + objects[j].img.get_rect()[3] / 2
                    dist = (self.img.get_rect()[2] + objects[j].img.get_rect()[2]) * 0.93 / 2
                    if collision(center_x1, center_y1, center_x2, center_y2, dist):
                        if self.name == settings.WEAPON_LIST[0]:
                            self.onfire[i] = False
                        if self.name == settings.WEAPON_LIST[1] and self.damage < objects[j].hp:
                            self.onfire[i] = False
                        objects[j].explosion.frame = 0
                        if objects[j].hp <= self.damage:
                            objects[j].explosion.size = "large"
                            objects[j].explode()
                            pygame.mixer.Sound("musics/asteroid_collision.wav").play(0, 0, 400)
                        else:
                            objects[j].hp -= self.damage
                            objects[j].explosion.size = "small"
                            objects[j].explosion.show(self.xpos[i] + 16, self.ypos[i] + 16)
                            pygame.mixer.Sound("musics/drone_collision.wav").play(0, 0, 400)
                        if self.name == settings.WEAPON_LIST[2]:
                            self.detonate = True
                        break

    def detect_nearest_object(self, objects):
        nearest = -1
        min_dist = 1000
        center_x1 = self.xpos[0] + self.img.get_rect()[2] / 2
        center_y1 = self.ypos[0] + self.img.get_rect()[3] / 2
        for i in range(len(objects)):
            center_x2 = objects[i].xpos + objects[i].img.get_rect()[2] / 2
            center_y2 = objects[i].ypos + objects[i].img.get_rect()[3] / 2
            dist = hypot(center_x1 - center_x2, center_y1 - center_y2)
            if dist < min_dist:
                nearest = i
                min_dist = dist
        return objects[nearest]

    def follow(self, tracked_object):
        for i in range(self.count):
            center_x1 = (self.xpos[i] - self.img.get_rect()[2] / 2)
            center_y1 = (self.ypos[i] - self.img.get_rect()[3] / 2)
            center_x2 = (tracked_object.xpos + tracked_object.img.get_rect()[2] / 2)
            center_y2 = (tracked_object.ypos + tracked_object.img.get_rect()[3] / 2)
            x_delta = center_x2 - center_x1
            y_delta = center_y2 - center_y1

            if x_delta < 0:
                self.xdir = "right"
            elif x_delta > 0:
                self.xdir = "left"
            else:
                self.xdir = ""

            if y_delta > 0:
                self.ydir = "up"
            elif y_delta < 0:
                self.ydir = "down"
            else:
                self.ydir = ""

            if x_delta == 0:
                if y_delta > 0:
                    self.ypos[i] += self.vel
                else:
                    self.ypos[i] -= self.vel
            elif y_delta == 0:
                if x_delta > 0:
                    self.xpos[i] += self.vel
                else:
                    self.xpos[i] -= self.vel
            else:
                dist = hypot(x_delta, y_delta)
                theta = atan(fabs(y_delta) / fabs(x_delta))
                x_increment = self.vel * cos(theta)
                y_increment = self.vel * sin(theta)

                if y_delta < 0 and x_delta > 0:
                    self.xpos[i] += x_increment
                    self.ypos[i] -= y_increment
                elif y_delta < 0 and x_delta < 0:
                    self.xpos[i] -= x_increment
                    self.ypos[i] -= y_increment
                elif y_delta > 0 and x_delta < 0:
                    self.xpos[i] -= x_increment
                    self.ypos[i] += y_increment
                else:
                    self.xpos[i] += x_increment
                    self.ypos[i] += y_increment

            if self.xpos[i] < 0:
                self.xpos[i] = 0
                self.detecting = True
            elif self.xpos[i] > 800 - self.img.get_rect()[2]:
                self.xpos[i] = 800 - self.img.get_rect()[2]
                self.detecting = True
            elif self.ypos[i] > 450 - self.img.get_rect()[2]:
                self.ypos[i] = 450 - self.img.get_rect()[2]
                self.detecting = True

            if tracked_object.xpos < -tracked_object.img.get_rect()[2] or tracked_object.xpos > 800 \
                    or tracked_object.ypos < -tracked_object.img.get_rect()[3] or tracked_object.ypos > 550:
                self.detecting = True

    def explode(self, objects):
        for i in range(self.count):
            self.onfire[i] = False
            center_x1 = self.xpos[i] + self.img.get_rect()[2] / 2
            center_y1 = self.ypos[i] + self.img.get_rect()[3] / 2
            for j in range(len(objects)):
                center_x2 = objects[j].xpos + objects[j].img.get_rect()[2] / 2
                center_y2 = objects[j].ypos + objects[j].img.get_rect()[3] / 2
                dist = hypot(center_x1 - center_x2, center_y1 - center_y2)
                if dist <= self.explosion_radius:
                    objects[j].explosion.frame = 0
                    if objects[j].hp <= self.damage:
                        objects[j].explosion.size = "large"
                        objects[j].explode()
                        pygame.mixer.Sound("musics/asteroid_collision.wav").play(0, 0, 400)
                    else:
                        objects[j].hp -= self.damage
                        objects[j].explosion.size = "small"
                        objects[j].explosion.show(self.xpos[i] + 16, self.ypos[i] + 16)
                        pygame.mixer.Sound("musics/drone_collision.wav").play(0, 0, 400)

        self.detonate = False
        self.detecting = False
        self.detonation_x = self.xpos[0]
        self.detonation_y = self.ypos[0]
        self.detonation_time = pygame.time.get_ticks()