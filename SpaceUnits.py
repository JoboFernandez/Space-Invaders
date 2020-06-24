import pygame
from random import choice, randint
from math import hypot, atan, sin, cos, fabs, pi

space_width = 0
space_height = 0

def collision(x1, y1, x2, y2, dist = 0):
    if hypot(x2 - x1, y2 - y1) <= dist:
        return True
    return False

def wraptxt(text, fontsize, width):
    texts = text.split()
    lines = []
    line = []
    line_width = 0
    for t in texts:
        if line_width + len(t) * fontsize <= width:
            line.append(t)
            line_width += len(t) * fontsize
        else:
            lines.append(' '.join(line))
            line = [t]
            line_width = 0
    else: lines.append(' '.join(line))
    return lines

def drawbtn(screen, object):
    screen.blit(object.bgcolor, (object.left, object.top))
    pygame.draw.rect(screen, object.color, (round(object.left), round(object.top), round(object.width), round(object.height)), object.border_width)
    if object.img.img != None:
        screen.blit(object.img.img, (object.img.left, object.img.top))
    # if object.text.label == '': lines = wraptxt(object.text.label, object.text.size, object.text.width)
    # else: lines = wraptxt(object.text.label, object.text.size, object.text.width)
    lines = wraptxt(object.text.label, object.text.size, object.text.width)
    for i in range(len(lines)):
        screen.blit(pygame.font.Font("freesansbold.ttf", object.text.size).render(lines[i], True, object.text.color),
            (round(object.text.left), round(object.text.top) + i * (object.text.size + 2)))
    if object.hasselection and not object.selected:
        greyout = pygame.Surface((object.width, object.height))
        greyout.fill((62, 88, 105))
        greyout.set_alpha(128)
        screen.blit(greyout, (object.left, object.top))

def drawpbar(screen, object):
    pbarbg = pygame.Surface((object.width, 14))
    pbarbg.fill((0,0,0))
    pbarbg.set_alpha(128)
    screen.blit(pbarbg, (object.left, object.top))
    pygame.draw.rect(screen, object.backcolor, (round(object.left), round(object.top), round(object.width), round(object.height)), 2)
    pygame.draw.rect(screen, object.progresscolor, (round(object.progressleft), round(object.progresstop), round(object.progresswidth), round(object.progressheight)))
    pbarlight = pygame.Surface((object.progresswidth, object.progressheight - 5))
    pbarlight.fill((255,255,255))
    pbarlight.set_alpha(96)
    screen.blit(pbarlight, (object.progressleft, object.progresstop + object.height // 3))
    pbarlight = pygame.Surface((object.progresswidth, object.progressheight - (2 * object.progressheight // 3)))
    pbarlight.fill((255, 255, 255))
    pbarlight.set_alpha(128)
    screen.blit(pbarlight, (object.progressleft, object.progresstop + object.height // 3 + 4))
    screen.blit(pygame.font.Font("freesansbold.ttf", object.text.size).render(object.text.label, True, object.text.color),
        (round(object.text.left), round(object.text.top)))

def drawtxt(screen, object):
    lines = wraptxt(object.label, object.size, object.width)
    for i in range(len(lines)):
        screen.blit(object.font.render(lines[i], True, object.color),
                    (round(object.left), round(object.top) + i * (object.size + 2)))

def space_area(width, height):
    global space_width
    global space_height
    space_width = width
    space_height = height
    return space_width, space_height

class Asteroid():
    def __init__(self):
        self.name = "asteroid"
        self.img = pygame.image.load("imgs/meteor64.png")
        self.hp = 1
        self.xpos = randint(0, space_width - 64)
        self.ypos = randint(-space_height, -64)
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
        self.xpos = randint(0, space_width - 64)
        self.ypos = randint(-space_height, -64)
        self.hp = 1

    def hide(self):
        self.xpos = 0
        self.ypos = -600
        self.xvel = 0
        self.yvel = 0

class Bullet():
    def __init__(self):
        self.name = "bullet"
        self.img = pygame.image.load("imgs/bluebullet32.png")
        self.damage = 1
        self.ammo = 3
        self.hp = 3
        self.xpos = randint(0, space_width - 64)
        self.ypos = randint(-192, -64)
        self.theta = pi/2
        self.onfire = False
        self.vel = 4
        self.explosion = Explosion()
        self.destroyed = False

    def move(self, source = "fromplayer"):
        if self.onfire:
            width = self.img.get_rect()[2]
            height = self.img.get_rect()[3]
            self.xpos = self.xpos + (self.vel * cos(self.theta))
            self.ypos = self.ypos - (self.vel * sin(self.theta))
            if source == "fromplayer":
                self.onfire = False if self.ypos < -height else True
            else:
                self.onfire = False if (self.ypos > 600 or self.xpos < -width or self.xpos > 800) else True

    def bring_to_ship(self, object):
        self.destroyed = False
        width1 = object.img.get_rect()[2] / 2
        height1 = object.img.get_rect()[3] / 2
        width2 = self.img.get_rect()[2] / 2
        height2 = self.img.get_rect()[3] / 2
        if not self.onfire:
            self.xpos = object.xpos + width1 - width2
            self.ypos = object.ypos + height1 - height2

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
                centerx1 = self.xpos + self.img.get_rect()[2] / 2
                centery1 = self.ypos + self.img.get_rect()[3] / 2
                for j in range(len(objects)):
                    centerx2 = objects[j].xpos + objects[j].img.get_rect()[2] / 2
                    centery2 = objects[j].ypos + objects[j].img.get_rect()[3] / 2
                    dist = (self.img.get_rect()[2] + objects[j].img.get_rect()[2]) * 0.93 / 2
                    if collision(centerx1, centery1, centerx2, centery2, dist):
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

class Button():
    def __init__(self, left, top, width, height, hasselection = False):
        self.text = Text()
        self.text.left = left
        self.text.top = top
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = (62, 88, 105)
        self.border_width = 2
        self.bgcolor = pygame.Surface((width, height))
        self.bgcolor.fill((0,0,0))
        self.bgcolor.set_alpha(128)
        self.img = Image()
        self.selected = False
        self.hasselection = hasselection

    def isover(self, pos):
        if (self.left < pos[0] < self.left + self.width) and (self.top < pos[1] < self.top + self.height): return True

    def glow(self):
        if not self.selected:
            self.text.color = (248, 193, 188)
            self.color = (248, 193, 188)

    def unglow(self):
        if not self.selected:
            self.text.color = (255, 179, 160)
            self.color = (62, 88, 105)

    def select(self):
        self.text.color = (182, 252, 116)
        self.color = (182, 252, 116)
        self.selected = True

    def unselect(self):
        self.text.color = (255, 179, 160)
        self.color = (62, 88, 105)
        self.selected = False

    def set_image(self, img, size):
        self.img.img = img
        self.img.size = size
        self.img.left = self.left + (self.width - size) // 2
        self.img.top = self.top + (self.height - size) // 2

class Color():
    beige = (255, 179, 160)
    beigeglow = (248, 193, 188)
    black = (0, 0, 0)
    blue = (0, 200, 200)
    cockpit = (62, 79, 99)
    cockpit_expt = (31, 40, 50)
    green = (0, 255, 0)
    mellowgreen = (76, 196, 40)
    orange = (255, 127, 39)
    red = (255, 0, 0)
    slimegreen = (182, 252, 116)
    spacegray = (62, 88, 105)
    white = (255, 255, 255)

class Drone():
    def __init__(self):
        self.name = "drone"
        self.img = pygame.image.load("imgs/drone128.png")
        self.xpos = randint(0, space_width - 128)
        self.ypos = randint(0,100)
        self.angle = 0
        self.angle_vel = 0.065
        self.hp = 15
        self.explosion = Explosion()
        self.bullet = Bullet()
        self.bullet.img = pygame.image.load("imgs/bomb64.png")
        self.bullet.vel = 3
        self.fire_delay = 2000 + randint(0,1000)
        self.last_fire = pygame.time.get_ticks()
        self.destroyed = False

    def hide(self):
        self.xpos = 0
        self.ypos = -600

    def explode(self):
        self.explosion.show(self.xpos + 64, self.ypos + 64)
        self.hide()
        self.destroyed = True

    def follow(self, object):
        if not self.destroyed:
            xaccuracy, yaccuracy = randint(int(object.xpos), int(object.xpos + 62)), object.ypos
            x_delta = xaccuracy - (self.xpos + 64)
            y_delta = yaccuracy - (self.ypos + 64)
            theta = atan(fabs(x_delta) / fabs(y_delta)) * 180 / pi
            if x_delta < 0: theta *= -1
            if self.angle > theta: self.angle -= self.angle_vel
            else: self.angle += self.angle_vel
            if self.angle <= -60: self.angle = -60
            elif self.angle >= 60: self.angle = 60
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

class EnergyBar():
    def __init__(self):
        self.energy = 0
        self.limit = 100
        self.bar_angle = 0
        self.notified = False

    def update(self, increment = 0):
        if self.energy + increment > self.limit: self.energy = self.limit
        else: self.energy += increment
        self.bar_angle = 2 * pi * self.energy / self.limit

    def expend(self):
        self.energy = 0
        self.bar_angle = 0
        self.notified = False

    def notify(self):
        self.notified = True

class Explosion():
    explosion_frames = []
    explosion_frames_small = []
    for i in range(9):
        filename = f"imgs/regularExplosion0{i}.png"
        explosion_frames.append(pygame.image.load(filename))
        small = pygame.transform.scale(explosion_frames[i], (32, 32))
        explosion_frames_small.append(small)
    # frame_sizes = [(192,192), (152,150), (82,91), (92, 102), (120, 124), (133, 134), (138, 140), (143, 144), (149, 151)]
    def __init__(self):
        self.left = 0
        self.top = -600
        self.img = self.explosion_frames[0]
        self.frame = 0
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()
        self.ongoing = False
        self.centerx = self.left
        self.centery = self.top
        self.size = "large"

    def update(self):
        if self.ongoing:
            if self.size == "large":
                self.left = self.centerx - self.explosion_frames[self.frame].get_rect()[2] / 2
                self.top = self.centery - self.explosion_frames[self.frame].get_rect()[2] / 2
            else:
                self.left = self.centerx - 16
                self.top = self.centery - 16
            now = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.last_update >= self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame < 9:
                    if self.size == "large": self.img = self.explosion_frames[self.frame]
                    else: self.img = self.explosion_frames_small[self.frame]
                else:
                    self.frame = 0
                    self.hide()

    def hide(self):
        self.left = 0
        self.top = -600
        self.ongoing = False

    def show(self, centerx, centery):
        self.centerx = centerx
        self.centery = centery
        self.ongoing = True

class FPS():
    def __init__(self, left, top):
        self.frames = 0
        self.fps = randint(60,115)
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.color = (0, 255, 0)
        self.left = left
        self.top = top
        self.time1 = pygame.time.get_ticks()

    def update(self, inc = 1):
        if (pygame.time.get_ticks() - self.time1) // 1000 >= 1:
            self.time1 = pygame.time.get_ticks()
            self.fps = self.frames
            self.frames = 0
        self.frames += inc

class Image():
    def __init__(self):
        self.img = pygame.image.load("imgs/battleship32.png")
        self.size = 0
        self.left = 0
        self.top = -600

class Level():
    def __init__(self):
        self.level = 1
        self.state = 0 # 1=LevelCleared, 0=OngoingLevel, -1=LevelGameOver
        self.asteroid_count = 0
        self.drone_count = 0
        self.time_limit = 0

    def next(self, msglog, timer):
        self.level += 1
        self.state = 0
        self.time_limit += 1
        if self.level % 5 == 0:
            pass
        else:
            self.asteroid_count += 3
            self.drone_count += 1
        pygame.mouse.set_pos(400, 418)
        msglog.update("", (255,255,255))
        msglog.update("", (255,255,255))
        msglog.update(f"WELCOME TO LEVEL {self.level}", (255,255,255))
        timer.start(self.time_limit)

    def reset(self, player, energy_gauge, msglog, timer):
        pygame.mixer.music.load("musics/background01.mp3")
        pygame.mixer.music.play(-1)
        self.level = 1
        self.state = 0
        self.asteroid_count = 15
        self.drone_count = 0
        self.time_limit = 40
        player.change_ship(player.name)
        energy_gauge.energy = 0
        pygame.mouse.set_pos(400, 418)
        msglog.update("", (255,255,255))
        msglog.update("", (255,255,255))
        msglog.update("WELCOME TO LEVEL 1", (255,255,255))
        timer.start(self.time_limit)

class Message():
    def __init__(self):
        self.msg = ""
        self.size = 0
        self.color = (0,0,0)
        self.left = 0
        self.top = 0
        self.font = pygame.font.Font('freesansbold.ttf', self.size)

    def set(self, msg, size, color, left, top):
        self.msg = msg
        self.size = size
        self.color = color
        self.left = left
        self.top = top
        self.font = pygame.font.Font('freesansbold.ttf', self.size)

class MessageLog():
    def __init__(self):
        self.msg = ["", "", ""]
        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.color = [(0,0,0), (0,0,0), (0,0,0)]
        self.left = 290
        self.tops = [542, 562, 582]

    def update(self, msg, color):
        for i in range(2):
            self.msg[i] = self.msg[i+1]
            self.color[i] = self.color[i+1]
        self.msg[2] = msg
        self.color[2] = color

class ProgressBar():
    def __init__(self, left, top, width, height, backcolor, progresscolor):
        self.text = Text()
        self.text.left = left
        self.text.top = top
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.backcolor = backcolor
        self.progresscolor = progresscolor
        self.progressleft = self.left + 2
        self.progresstop = self.top + 2
        self.progresswidth = 0
        self.progressheight = self.height - 3

    def update(self, progress, limit):
        self.progresswidth = int(progress * self.width / limit)

class SpaceShip():
    shiplist = ["ZCEVERINESKY", "RXCRAP", "PSTRYK"]
    shipimgs = [pygame.image.load("imgs/whiteship64.png"),
                pygame.image.load("imgs/transporter64.png"),
                pygame.image.load("imgs/battleship64.png")]
    shipavatar = [pygame.image.load("imgs/whiteship32.png"),
                  pygame.image.load("imgs/transporter32.png"),
                  pygame.image.load("imgs/battleship32.png")]

    def __init__(self):
        self.name = self.shiplist[0]
        self.img = self.shipimgs[0]
        self.xpos = space_width // 2 - 32
        self.ypos = space_height - 150
        self.vel = 3
        self.direction = 0
        self.durability = 4
        self.energy = 0
        self.bullet = Bullet()
        self.avatar = self.shipavatar[0]
        self.weapon = Weapon()

    def change_ship(self, name):
        self.name = name
        if name == self.shiplist[0]:
            self.img = self.shipimgs[0]
            self.vel = 3
            self.durability = 2
            self.energy = 5

            self.bullet.ammo = 4
            self.avatar = self.shipavatar[0]
        elif name == self.shiplist[1]:
            self.img = self.shipimgs[1]
            self.vel = 3
            self.durability = 5
            self.energy = 4
            self.bullet.ammo = 2
            self.avatar = self.shipavatar[1]
        elif name == self.shiplist[2]:
            self.img = self.shipimgs[2]
            self.vel = 2
            self.durability = 4
            self.energy = 3
            self.bullet.ammo = 5
            self.avatar = self.shipavatar[2]

    def follow(self, pos):
        x_delta = pos[0] - 32 - self.xpos
        y_delta = pos[1] - 32 - self.ypos
        if x_delta == 0:
            if y_delta > 0: self.ypos += self.vel if self.vel <= y_delta else y_delta
            else: self.ypos -= self.vel if self.vel <= fabs(y_delta) else fabs(y_delta)
        elif y_delta == 0:
            if x_delta > 0: self.xpos += self.vel if self.vel <= x_delta else x_delta
            else: self.xpos -= self.vel if self.vel <= fabs(x_delta) else fabs(x_delta)
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
        if self.xpos < 0: self.xpos = 0
        if self.xpos > 736: self.xpos = 736
        if self.ypos <= 300: self.ypos = 300
        if self.ypos >= 450: self.ypos = 450

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
        if self.weapon.name == self.weapon.weapon_list[0]:
            pygame.mixer.Sound("musics/tpf7_fired.wav").play()
        elif self.weapon.name == self.weapon.weapon_list[1]:
            pygame.mixer.Sound("musics/maruna_fired.wav").play()
        else:
            pygame.mixer.Sound("musics/eruma_fired.wav")

    def detect_collision(self, objects, level, msglog):
        centerx1 = self.xpos + self.img.get_rect()[2] / 2
        centery1 = self.ypos + self.img.get_rect()[3] / 2
        for i in range(len(objects)):
            centerx2 = objects[i].xpos + objects[i].img.get_rect()[2] / 2
            centery2 = objects[i].ypos + objects[i].img.get_rect()[3] / 2
            dist = (self.img.get_rect()[2] + objects[i].img.get_rect()[2]) * 0.93 / 2
            if collision(centerx1, centery1, centerx2, centery2, dist):
                if self.durability > 1:
                    self.durability -= 1
                else:
                    level.state = -1
                objects[i].explode()
                pygame.mixer.Sound("musics/ship_damaged.wav").play()
                msglog.update("SHIP HAS BEEN HIT", (255, 0, 0))

class Text():
    def __init__(self, label = "", size = 12, color = (0,0,0), left = 0, top = 0, width = None):
        self.label = label
        self.size = size
        self.font = pygame.font.Font("freesansbold.ttf", self.size)
        self.color = color
        self.left = left
        self.top = top
        self.leftcopy = self.left
        self.topcopy = self.top
        if width == None: self.width = self.size * len(self.label)
        else: self.width = width

    def set_properties(self, label, size, color, left, top, width = None):
        self.label = label
        self.size = size
        self.font = pygame.font.Font("freesansbold.ttf", self.size)
        self.color = color
        self.left = left
        self.top = top
        self.leftcopy = self.left
        self.topcopy = self.top
        if width == None: self.width = self.size * len(self.label)
        else: self.width = width

class Timer():
    def __init__(self, left, top):
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.color = (0, 255, 0)
        self.time1 = 0
        self.left = left
        self.top = top
        self.mm = 0
        self.ss = 0

    def start(self, limit):
        self.mm = limit // 60
        self.ss = limit % 60
        self.time1 = pygame.time.get_ticks() + limit * 1000

    def remaining(self):
        rem = (self.time1 - pygame.time.get_ticks()) // 1000
        self.mm = rem // 60 if rem > 0 else 0
        self.ss = rem % 60 if rem > 0 else 0
        return rem

    def updatecolor(self, color):
        self.color = color

class Weapon():
    weapon_list = ["TPF7", "MARUNA", "ERUMA"]
    weapon_imgs = [pygame.image.load("imgs/missile32.png"),
                  pygame.image.load("imgs/nuclear32.png"),
                  pygame.image.load("imgs/reactor32.png")]
    def __init__(self):
        self.name = self.weapon_list[0]
        self.img = self.weapon_imgs[0]
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
            self.name = self.weapon_list[0]
            self.img = self.weapon_imgs[0]
            self.count = 7
            self.xpos = [0 for i in range(self.count)]
            self.ypos = [0 for i in range(self.count)]
            self.vel = 4
            self.onfire = [False for i in range(self.count)]
            self.theta = [-pi/2 + i * pi/6 for i in range(self.count)]
            self.explosion_radius = 50
        elif name == "MARUNA":
            self.name = self.weapon_list[1]
            self.img = self.weapon_imgs[1]
            self.count = 2
            self.xpos = [0 for _ in range(self.count)]
            self.ypos = [0 for _ in range(self.count)]
            self.vel = 4
            self.onfire = [False for _ in range(self.count)]
            self.theta = [pi/4 for _ in range(self.count)]
            self.explosion_radius = 0
        else:
            self.name = self.weapon_list[2]
            self.img = self.weapon_imgs[2]
            self.count = 1
            self.xpos = [0]
            self.ypos = [0]
            self.vel = 3
            self.onfire = [False]
            self.theta = [pi/2]
            self.explosion_radius = 200

    def bring_to_ship(self, object):
        for i in range(self.count):
            if self.name == self.weapon_list[1]:
                self.xpos[i] = object.xpos + i * ((object.img.get_rect()[2] - 32) / (self.count - 1))
            else:
                self.xpos[i] = object.xpos + 32 - 16
            self.ypos[i] = object.ypos + 32 - 16

    def track(self, object):
        self.track = object

    def move(self):
        for i in range(self.count):
            if self.onfire[i]:
                if self.name == self.weapon_list[0]:
                    self.xpos[i] += self.vel * sin(self.theta[i])
                    self.ypos[i] -= self.vel * cos(self.theta[i])
                elif self.name == self.weapon_list[1]:
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
                centerx1 = self.xpos[i] + self.img.get_rect()[2] / 2
                centery1 = self.ypos[i] + self.img.get_rect()[3] / 2
                for j in range(len(objects)):
                    centerx2 = objects[j].xpos + objects[j].img.get_rect()[2] / 2
                    centery2 = objects[j].ypos + objects[j].img.get_rect()[3] / 2
                    dist = (self.img.get_rect()[2] + objects[j].img.get_rect()[2]) * 0.93 / 2
                    if collision(centerx1, centery1, centerx2, centery2, dist):
                        if self.name == self.weapon_list[0]: self.onfire[i] = False
                        if self.name == self.weapon_list[1] and self.damage < objects[j].hp: self.onfire[i] = False
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
                        if self.name == self.weapon_list[2]: self.detonate = True
                        break


    def detect_nearest_object(self, objects):
        nearest = -1
        min_dist = 1000
        centerx1 = self.xpos[0] + self.img.get_rect()[2] / 2
        centery1 = self.ypos[0] + self.img.get_rect()[3] / 2
        for i in range(len(objects)):
            centerx2 = objects[i].xpos + objects[i].img.get_rect()[2] / 2
            centery2 = objects[i].ypos + objects[i].img.get_rect()[3] / 2
            dist = hypot(centerx1 - centerx2, centery1 - centery2)
            if dist < min_dist:
                nearest = i
                min_dist = dist
        return objects[nearest]

    def follow(self, tracked_object):
        for i in range(self.count):
            centerx1 = (self.xpos[i] - self.img.get_rect()[2] / 2)
            centery1 = (self.ypos[i] - self.img.get_rect()[3] / 2)
            centerx2 = (tracked_object.xpos + tracked_object.img.get_rect()[2] / 2)
            centery2 = (tracked_object.ypos + tracked_object.img.get_rect()[3] / 2)
            x_delta = centerx2 - centerx1
            y_delta = centery2 - centery1
            if x_delta < 0: self.xdir = "right"
            elif x_delta > 0: self.xdir = "left"
            else: self.xdir = ""
            if y_delta > 0: self.ydir = "up"
            elif y_delta < 0: self.ydir = "down"
            else: self.ydir = ""
            if x_delta == 0:
                if y_delta > 0: self.ypos[i] += self.vel
                else: self.ypos[i] -= self.vel
            elif y_delta == 0:
                if x_delta > 0: self.xpos[i] += self.vel
                else: self.xpos[i] -= self.vel
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
            if self.xpos[i] < 0: self.xpos[i] = 0; self.detecting = True
            elif self.xpos[i] > 800 - self.img.get_rect()[2]: self.xpos[i] = 800 - self.img.get_rect()[2]; self.detecting = True
            elif self.ypos[i] > 450 - self.img.get_rect()[2]: self.ypos[i] > 450 - self.img.get_rect()[2]; self.detecting = True
            if tracked_object.xpos < -tracked_object.img.get_rect()[2] or tracked_object.xpos > 800 \
                    or tracked_object.ypos < -tracked_object.img.get_rect()[3] or tracked_object.ypos > 550:
                self.detecting = True

    def explode(self, objects):
        for i in range(self.count):
            self.onfire[i] = False
            centerx1 = self.xpos[i] + self.img.get_rect()[2] / 2
            centery1 = self.ypos[i] + self.img.get_rect()[3] / 2
            for j in range(len(objects)):
                centerx2 = objects[j].xpos + objects[j].img.get_rect()[2] / 2
                centery2 = objects[j].ypos + objects[j].img.get_rect()[3] / 2
                dist = hypot(centerx1 - centerx2, centery1 - centery2)
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