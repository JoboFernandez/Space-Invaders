from . import Bullet, Weapon
from utils import collision
from math import pi, fabs, hypot, atan, cos, sin
from random import randint, choice
import settings
import pygame


class SpaceShip:

    def __init__(self):
        self.xpos = settings.SCREEN_WIDTH // 2 - 32
        self.ypos = settings.SCREEN_HEIGHT - 150
        self.vel = 3
        self.direction = 0
        self.durability = 4
        self.energy = 0
        self.bullet = Bullet()
        self.weapon = Weapon()

        self.name = settings.SHIP_LIST[0]
        self.img = settings.SHIP_IMAGES[0]
        self.avatar = settings.SHIP_AVATARS[0]

    def change_ship(self, name):
        self.name = name
        if name == settings.SHIP_LIST[0]:
            self.img = settings.SHIP_IMAGES[0]
            self.vel = 3
            self.durability = 2
            self.energy = 5
            self.bullet.ammo = 4
            self.avatar = settings.SHIP_AVATARS[0]
        elif name == settings.SHIP_LIST[1]:
            self.img = settings.SHIP_IMAGES[1]
            self.vel = 3
            self.durability = 5
            self.energy = 4
            self.bullet.ammo = 2
            self.avatar = settings.SHIP_AVATARS[1]
        elif name == settings.SHIP_LIST[2]:
            self.img = settings.SHIP_IMAGES[2]
            self.vel = 2
            self.durability = 4
            self.energy = 3
            self.bullet.ammo = 5
            self.avatar = settings.SHIP_AVATARS[2]

    def follow(self, pos):
        x, y = pos
        x_delta = x - 32 - self.xpos
        y_delta = y - 32 - self.ypos

        if x_delta == 0:
            if y_delta > 0:
                self.ypos += self.vel if self.vel <= y_delta else y_delta
            else:
                self.ypos -= self.vel if self.vel <= fabs(y_delta) else fabs(y_delta)
        elif y_delta == 0:
            if x_delta > 0:
                self.xpos += self.vel if self.vel <= x_delta else x_delta
            else:
                self.xpos -= self.vel if self.vel <= fabs(x_delta) else fabs(x_delta)
        else:
            dist = hypot(x_delta, y_delta)
            theta = atan(fabs(y_delta) / fabs(x_delta))
            x_increment = self.vel * cos(theta)
            y_increment = self.vel * sin(theta)
            if y_delta < 0 and x_delta > 0:
                self.xpos += x_increment if x_increment <= dist else dist
                self.ypos -= y_increment if y_increment <= dist else dist
            elif y_delta < 0 and x_delta < 0:
                self.xpos -= x_increment if x_increment <= dist else dist
                self.ypos -= y_increment if y_increment <= dist else dist
            elif y_delta > 0 and x_delta < 0:
                self.xpos -= x_increment if x_increment <= dist else dist
                self.ypos += y_increment if y_increment <= dist else dist
            else:
                self.xpos += x_increment if x_increment <= dist else dist
                self.ypos += y_increment if y_increment <= dist else dist

        if self.xpos < 0:
            self.xpos = 0
        if self.xpos > 736:
            self.xpos = 736
        if self.ypos <= 300:
            self.ypos = 300
        if self.ypos >= 450:
            self.ypos = 450

    def hide(self):
        self.ypos = 650

    def fire(self, bullets):
        for i in range(len(bullets)):
            if not bullets[i].onfire:
                bullets[i].bring_to_ship(self)
                bullets[i].onfire = True
                pygame.mixer.Sound("musics/laser_fired.wav").play(0, 0, 500)
                break

    def fire_specialweapon(self):
        self.weapon.bring_to_ship(self)
        self.weapon.onfire = [True for _ in range(self.weapon.count)]

        if self.weapon.name == settings.WEAPON_LIST[0]:
            pygame.mixer.Sound("musics/tpf7_fired.wav").play()
        elif self.weapon.name == settings.WEAPON_LIST[1]:
            pygame.mixer.Sound("musics/maruna_fired.wav").play()
        else:
            pygame.mixer.Sound("musics/eruma_fired.wav")

    def detect_collision(self, objects, level, msglog):
        center_x1 = self.xpos + self.img.get_rect()[2] / 2
        center_y1 = self.ypos + self.img.get_rect()[3] / 2
        for i in range(len(objects)):
            center_x2 = objects[i].xpos + objects[i].img.get_rect()[2] / 2
            center_y2 = objects[i].ypos + objects[i].img.get_rect()[3] / 2
            dist = (self.img.get_rect()[2] + objects[i].img.get_rect()[2]) * 0.93 / 2
            if collision(center_x1, center_y1, center_x2, center_y2, dist):
                if self.durability > 1:
                    self.durability -= 1
                else:
                    level.state = -1
                objects[i].explode()
                pygame.mixer.Sound("musics/ship_damaged.wav").play()
                msglog.update("SHIP HAS BEEN HIT", (255, 0, 0))

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(self.img, (round(self.xpos), round(self.ypos)))

        for i in range(self.weapon.count):

            if self.weapon.name == settings.WEAPON_LIST[0]:
                screen.blit(pygame.transform.rotate(self.weapon.img, -self.weapon.theta[i] * 180 / pi), (round(self.weapon.xpos[i]), round(self.weapon.ypos[i])))

            elif self.weapon.name == settings.WEAPON_LIST[1]:
                screen.blit(self.weapon.img, (round(self.weapon.xpos[i]), round(self.weapon.ypos[i])))

            elif self.weapon.name == settings.WEAPON_LIST[2]:
                cx, cy = self.weapon.xpos[0] + 16, self.weapon.ypos[0] + 16
                jet_length1 = randint(20, 28)
                jet_length2 = randint(28, 36)
                jet_length3 = randint(36, 44)

                if self.weapon.xdir == "left":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx) - jet_length1, round(cy)), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx) - jet_length2, round(cy)), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx) - jet_length3, round(cy)), 1)

                elif self.weapon.xdir == "right":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx) + jet_length1, round(cy)), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx) + jet_length2, round(cy)), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx) + jet_length3, round(cy)), 1)

                if self.weapon.ydir == "up":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx), round(cy) - jet_length1), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx), round(cy) - jet_length2), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx), round(cy) - jet_length3), 1)

                elif self.weapon.ydir == "down":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx), round(cy) + jet_length1), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx), round(cy) + jet_length2), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]),
                                     (round(cx), round(cy)), (round(cx), round(cy) + jet_length3), 1)

                now = pygame.time.get_ticks()
                explosion_time = 1500
                if now - self.weapon.detonation_time < explosion_time:
                    radius_rate = round(self.weapon.explosion_radius * (explosion_time - (now - self.weapon.detonation_time)) / 2000)
                    green_rate = round(200 * (now - self.weapon.detonation_time) / explosion_time)
                    blue_rate = round(150 * (now - self.weapon.detonation_time) / explosion_time)
                    width = 2
                    if radius_rate > width:
                        pygame.draw.circle(screen, (255, green_rate, blue_rate, 128),
                                           (round(self.weapon.detonation_x), round(self.weapon.detonation_y)),
                                           radius_rate, width)
                screen.blit(self.weapon.img, (round(self.weapon.xpos[i]), round(self.weapon.ypos[i])))