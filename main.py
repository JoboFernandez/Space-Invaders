import pygame
import os, sys
from random import choice, randint
from SpaceUnits import Asteroid, Bullet, Button, Color, drawbtn, drawpbar, drawtxt, Drone, EnergyBar, FPS, Level, Message, MessageLog, ProgressBar, space_area, SpaceShip, Text, Timer, Weapon
from math import pi

def initiate_objects():
    global asteroids, drones, drone_bullets, bullets, level
    asteroids = []
    drones = []
    drone_bullets = []
    bullets = []
    for i in range(level.asteroid_count):
        asteroids.append(Asteroid())
    for i in range(level.drone_count):
        drones.append(Drone())
        drone_bullets.append(drones[i].bullet)
    for i in range(player.bullet.ammo):
        bullets.append(Bullet())

class GameState():
    def __init__(self):
        self.scene = 'mainscene'

    def mainscene(self):
        # OBJECT COLLECTORS
        btn_objs = [btnplaygame, btnabout, btnexit]

        # EVENT HANDLER
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for i in range(len(btn_objs)):
                    if btn_objs[i].isover(pos):
                        btn_objs[i].color = color.slimegreen
                        btn_objs[i].text.color = color.slimegreen
                    else:
                        btn_objs[i].color = color.spacegray
                        btn_objs[i].text.color = color.beige
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnplaygame.isover(pos):
                    pygame.mixer.music.load("musics/shop_bgmusic.mp3")
                    pygame.mixer.music.play(-1)
                    self.scene = 'characterselectscene'
                if btnabout.isover(pos):
                    self.scene = 'aboutscene'
                if btnexit.isover(pos):
                    pygame.quit()
                    sys.exit()

        # DRAWING
        screen.fill((0,0,0))
        screen.blit(bg_main, (0,0))


        for obj in btn_objs:
            drawbtn(screen, obj)

        pygame.display.update()

    def aboutscene(self):
        # OBJECT COLLECTORS
        txt_objs = [txtheader_a, txtelement_a1, txtheader_b, txtelement_b1, txtelement_b2, txtheader_c, txtelement_c1, txtelement_c2]

        # EVENT HANDLER
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if btnabouttomenu.isover(pos):
                    btnabouttomenu.glow()
                else: btnabouttomenu.unglow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnabouttomenu.isover(pos):
                    self.scene = 'mainscene'

        # DRAWING
        screen.fill((0, 0, 0))
        screen.blit(bg_about, (0, 0))

        for obj in txt_objs:
            drawtxt(screen, obj)
        drawbtn(screen, btnabouttomenu)

        pygame.display.update()

    def characterselectscene(self):
        # region EVENT HANDLER
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if btnwelcome.isover(pos): btnwelcome.text.color = color.slimegreen
                else: btnwelcome.text.color = color.mellowgreen
                for i in range(3):
                    if btnships[i].isover(pos): btnships[i].glow()
                    else: btnships[i].unglow()
                    if btnweapons[i].isover(pos): btnweapons[i].glow()
                    else: btnweapons[i].unglow()
                if btnlaunch.isover(pos): btnlaunch.glow()
                else: btnlaunch.unglow()
                if btncstomenu.isover(pos): btncstomenu.glow()
                else: btncstomenu.unglow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    if btnships[i].isover(pos):
                        btnships[i].select()
                        player.change_ship(player.shiplist[i])
                        for j in range(3):
                            if j != i:
                                btnships[j].unselect()
                        btnshippreview.set_image(ships128[i], 128)
                        btnshippreview.text.set_properties(btnships[i].text.label, 20, color.slimegreen, 530, 290)
                    if btnweapons[i].isover(pos):
                        btnweapons[i].select()
                        player.weapon.change_weapon(player.weapon.weapon_list[i])
                        btnweaponpreview.set_image(weapons32[i], 32)
                        for j in range(3):
                            if j != i:
                                btnweapons[j].unselect()
                stats = [player.vel, player.durability, player.energy, player.bullet.ammo]
                for j in range(len(pbarstats)):
                    pbarstats[j].update(stats[j], 5)
                if btncstomenu.isover(pos):
                    pygame.mixer.music.load("musics/main_bgmusic.mp3")
                    pygame.mixer.music.play(-1)
                    self.scene = 'mainscene'
                if btnlaunch.isover(pos):
                    level.reset(player, energy_gauge, msglog, timer)
                    initiate_objects()
                    self.scene = 'battlescene'

        # endregion

        # region DRAWING

        #Background
        screen.fill(color.black)
        screen.blit(bg_shop, (0, 0))

        btn_objs = [btnwelcome, btnships[0], btnships[1], btnships[2], btnweapons[0], btnweapons[1], btnweapons[2], btnshippreview, btnweaponpreview, btncstomenu, btnlaunch]
        for obj in btn_objs:
            drawbtn(screen, obj)
        for i in range(len(pbarstats)):
            drawpbar(screen, pbarstats[i])
        pygame.draw.line(screen, color.spacegray, (179, 92), (179, 448), 5)


        pygame.display.update()

        # endregion

    def battlescene(self):
        # region EVENT HANDLER
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if level.state == -1:
                        pygame.mixer.music.load("musics/shop_bgmusic.mp3")
                        pygame.mixer.music.play(-1)
                        player.change_ship(player.name)
                        player.weapon.change_weapon(player.weapon.name)
                        self.scene = 'characterselectscene'
                    elif level.state == 1:
                        level.next(msglog, timer)
                        initiate_objects()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and level.state == 0:
                    player.fire(bullets)
                if event.button == 3 and level.state == 0:
                    if energy_gauge.energy == energy_gauge.limit:
                        player.fire_specialweapon()
                        if player.weapon.name == player.weapon.weapon_list[2]:
                            player.weapon.detecting = True
                        energy_gauge.expend()
                        msglog.update("ENERGY EXPENDED", color.mellowgreen)
                    else:
                        msglog.update("INSUFFICIENT ENERGY", color.spacegray)
                        pygame.mixer.Sound("musics/insufficient_energy.wav").play(0,0,0)
        # endregion

        # region GAME LOGIC
        # region Player
        player.follow(pos)
        if level.state == -1: player.hide()
        player.detect_collision(asteroids, level, msglog)
        player.detect_collision(drones, level, msglog)
        player.detect_collision(drone_bullets, level, msglog)
        # endregion

        # region Bullets
        for i in range(player.bullet.ammo):
            bullets[i].move()
            bullets[i].detect_collision(asteroids, player, energy_gauge)
            bullets[i].detect_collision(drones, player, energy_gauge)
            bullets[i].detect_collision(drone_bullets, player, energy_gauge)
            bullets[i].bring_to_ship(player)
        # endregion

        # region Energy
        energy_gauge.update()
        if energy_gauge.energy == energy_gauge.limit and not energy_gauge.notified:
            msglog.update("WEAPON READY!!!", color.blue)
            energy_gauge.notify()
        # endregion

        # region Special Weapon
        if player.weapon.detecting:
            player.weapon.nearest_object = player.weapon.detect_nearest_object(asteroids + drones + drone_bullets)
            player.weapon.detecting = False
        player.weapon.move()
        player.weapon.detect_collision(asteroids)
        player.weapon.detect_collision(drones)
        player.weapon.detect_collision(drone_bullets)
        if player.weapon.detonate: player.weapon.explode(asteroids + drones + drone_bullets)
        # endregion

        # region Drones
        for i in range(level.drone_count):
            drones[i].follow(player)
            drones[i].bullet.move("fromdrone")
            drones[i].explosion.update()
            drones[i].bullet.explosion.update()
        # endregion

        # region Asteroids
        for i in range(level.asteroid_count):
            asteroids[i].move()
            asteroids[i].explosion.update()
        # endregion

        # region Game Status
        if level.state == -1:
            msg1.set("GAME OVER", 64, color.red, screen_w // 4, screen_h // 2 - 32)
            msg2.set("<< Press Space Bar to go back to character select >>", 16, color.red, screen_w // 4 -5, screen_h // 2 + 64)
            timer.updatecolor(color.red)
        if level.state == 0:
            msg1.msg = ""
            msg2.msg = ""
            rem = timer.remaining()
            if rem <= 0: timer.updatecolor(color.blue); level.state = 1
            elif 0 < rem <= 15: timer.updatecolor(color.orange)
            else: timer.updatecolor(color.green)
        else:
            for i in range(level.asteroid_count):
                if asteroids[i].ypos > -64:
                    asteroids[i].hide()
                    asteroids[i].explode()
            for i in range(level.drone_count):
                if drones[i].xpos > -128:
                    drones[i].explode()
                    drones[i].bullet.explode()
                    drones[i].bullet.onfire = False
        if level.state == 1:
            msg1.set("SPACE LEVEL INVADED", 64, color.blue, 30, screen_h // 2 - 32)
            msg2.set("<< Press Space Bar to proceed to the next level >>", 16, color.blue, screen_w // 4 + 15, screen_h // 2 + 64)

        fps.update()
        # endregion

        # endregion

        # region DRAWING
        # Background
        screen.fill(color.black)
        screen.blit(bg_space, (0, 0))
        # FPS
        screen.blit(fps.font.render(str(fps.fps) + " FPS", True, fps.color), (fps.left, fps.top))
        # Bullet
        for i in range(player.bullet.ammo):
            screen.blit(bullets[i].img, (round(bullets[i].xpos), round(bullets[i].ypos)))
        # Special weapon
        for i in range(player.weapon.count):
            if player.weapon.name == player.weapon.weapon_list[0]:
                screen.blit(pygame.transform.rotate(player.weapon.img, -player.weapon.theta[i] * 180/pi), (round(player.weapon.xpos[i]), round(player.weapon.ypos[i])))
            elif player.weapon.name == player.weapon.weapon_list[1]:
                screen.blit(player.weapon.img, (round(player.weapon.xpos[i]), round(player.weapon.ypos[i])))
            elif player.weapon.name == player.weapon.weapon_list[2]:
                cx, cy = player.weapon.xpos[0] + 16, player.weapon.ypos[0] + 16
                jet_length1 = randint(20, 28)
                jet_length2 = randint(28, 36)
                jet_length3 = randint(36, 44)
                if player.weapon.xdir == "left":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]), (round(cx), round(cy)), (round(cx) - jet_length1, round(cy)), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]), (round(cx), round(cy)), (round(cx) - jet_length2, round(cy)), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]), (round(cx), round(cy)), (round(cx) - jet_length3, round(cy)), 1)
                elif player.weapon.xdir == "right":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]), (round(cx), round(cy)), (round(cx) + jet_length1, round(cy)), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]), (round(cx), round(cy)), (round(cx) + jet_length2, round(cy)), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]), (round(cx), round(cy)), (round(cx) + jet_length3, round(cy)), 1)
                if player.weapon.ydir == "up":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]), (round(cx), round(cy)), (round(cx), round(cy) - jet_length1), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]), (round(cx), round(cy)), (round(cx), round(cy) - jet_length2), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]), (round(cx), round(cy)), (round(cx), round(cy) - jet_length3), 1)
                elif player.weapon.ydir == "down":
                    pygame.draw.line(screen, choice([(0, 200, 200), (0, 255, 255), (50, 255, 255)]), (round(cx), round(cy)), (round(cx), round(cy) + jet_length1), 5)
                    pygame.draw.line(screen, choice([(50, 255, 255), (100, 255, 255), (150, 255, 255)]), (round(cx), round(cy)), (round(cx), round(cy) + jet_length2), 3)
                    pygame.draw.line(screen, choice([(150, 200, 200), (200, 255, 255), (255, 255, 255)]), (round(cx), round(cy)), (round(cx), round(cy) + jet_length3), 1)
                now = pygame.time.get_ticks()
                explosion_time = 1500
                if now - player.weapon.detonation_time < explosion_time:
                    radius_rate = round(player.weapon.explosion_radius * (explosion_time - (now - player.weapon.detonation_time)) / 2000)
                    green_rate = round(200 * ((now - player.weapon.detonation_time)) / explosion_time)
                    blue_rate = round(150 * ((now - player.weapon.detonation_time)) / explosion_time)
                    width = 2
                    if radius_rate > width:
                        pygame.draw.circle(screen, (255,green_rate,blue_rate, 128), (round(player.weapon.detonation_x), round(player.weapon.detonation_y)), radius_rate, width)
                screen.blit(player.weapon.img, (round(player.weapon.xpos[i]), round(player.weapon.ypos[i])))
        # Player
        screen.blit(player.img, (round(player.xpos), round(player.ypos)))
        # Drones, drone bullets, drone explosion, drone bullet explosion
        for i in range(level.drone_count):
            screen.blit(drones[i].bullet.img, (round(drones[i].bullet.xpos), round(drones[i].bullet.ypos)))
            screen.blit(drones[i].bullet.explosion.img, (round(drones[i].bullet.explosion.left), round(drones[i].bullet.explosion.top)))
            screen.blit(pygame.transform.rotate(drones[i].img, drones[i].angle), (round(drones[i].xpos), round(drones[i].ypos)))
            screen.blit(drones[i].explosion.img, (round(drones[i].explosion.left), round(drones[i].explosion.top)))
        # Asteroids, asteroid explosion
        for i in range(level.asteroid_count):
            screen.blit(asteroids[i].img, (round(asteroids[i].xpos), round(asteroids[i].ypos)))
            screen.blit(asteroids[i].explosion.img, (round(asteroids[i].explosion.left), round(asteroids[i].explosion.top)))
        # Navigation control
        pygame.draw.rect(screen, color.black, (0, screen_h - 64, 800, 64))
        pygame.draw.line(screen, color.cockpit_expt, (0, screen_h - 64), (screen_w, screen_h - 64), 5)
        pygame.draw.line(screen, color.cockpit_expt, (280,539), (280,600), 5)
        pygame.draw.line(screen, color.cockpit_expt, (520,539), (520,600), 5)
        # Timer
        screen.blit(timer.font.render(f"{timer.mm:02d} : {timer.ss:02d}", True, timer.color), (timer.left, timer.top))
        # Remaining Lives
        for i in range(player.durability - 1):
            screen.blit(player.avatar, (130 + i * 32, screen_h - 16 - 32))
        # Message log
        for i in range(3):
            screen.blit(msglog.font.render(msglog.msg[i], True, msglog.color[i]), (msglog.left, msglog.tops[i]))
        # Special weapon energy gauge bar
        pygame.draw.arc(screen, (62, 88, 105), (538, 541, 56, 56), 0, 2 * pi, 6)
        pygame.draw.arc(screen, (96, 164, 247), (538, 541, 56, 56), 0, energy_gauge.bar_angle, 6)
        pygame.draw.arc(screen, (155, 198, 250), (540, 543, 52, 52), 0, energy_gauge.bar_angle, 4)
        pygame.draw.arc(screen, (205, 226, 252), (542, 545, 48, 48), 0, energy_gauge.bar_angle, 2)
        screen.blit(player.weapon.img, (550, 552))
        # Level
        screen.blit(pygame.font.Font("freesansbold.ttf", 32).render("Level : " + str(level.level), True, (255, 255, 255)),
                    (620, 552))
        # Game over / next level message
        screen.blit(msg1.font.render(msg1.msg, True, msg1.color), (msg1.left, msg1.top))
        screen.blit(msg2.font.render(msg2.msg, True, msg2.color), (msg2.left, msg2.top))

        pygame.display.update()
        # endregion

    def state_manager(self):
        if self.scene == 'mainscene':
            self.mainscene()
        elif self.scene == 'aboutscene':
            self.aboutscene()
        elif self.scene == 'characterselectscene':
            self.characterselectscene()
        elif self.scene == 'battlescene':
            self.battlescene()

# region WINDOW SETTINGS
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

screen_w, screen_h = space_area(800, 600)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Space Invaders 1.0")
icon = pygame.image.load("imgs/spaceship32.png")
pygame.display.set_icon(icon)
# endregion

# region GAME ENVIRONMENT
bg_main = pygame.image.load("imgs/bg_intro.jpg")
bg_about = pygame.image.load("imgs/bg_about.jpg")
bg_shop = pygame.image.load("imgs/bg_shop.jpg")
bg_space = pygame.image.load("imgs/bg_space.jpg")
pygame.mixer.music.load("musics/main_bgmusic.mp3")
pygame.mixer.music.play(-1)
# endregion

# region INITIALIZATIONS: GENERAL
game_state = GameState()
color = Color()
# endregion

# region INITIALIZATIONS: MAIN SCENE
btnplaygame = Button(160, 162, 480, 75)
btnplaygame.text.set_properties("PLAY SURVIVAL MODE", 33, color.beigeglow, 214, 185)
btnabout = Button(160, 262, 480, 75)
btnabout.text.set_properties("ABOUT THE GAME & CREDITS", 25, color.beigeglow, 212, 290)
btnexit = Button(160, 362, 480, 75)
btnexit.text.set_properties("EXIT", 50, color.beigeglow, 340, 378)
# endregion

# region INITIALIZATIONS: ABOUT & CREDITS SCENE
txtheader_a = Text("ABOUT THE GAME", 18, color.slimegreen, 10, 10)
txtelement_a1 = Text("This game is developed by Jobo a.k.a. ThePokerFaceVII solely for the purpose of coding practice. Not all products used herein are created by the game developer. That said, the developer would like to give credit to where it is due.", 14, color.mellowgreen, 10, 40, 1200)

txtheader_b = Text("GRAPHICS", 18, color.slimegreen, 10, 110)
txtelement_b1 = Text("Background Images: https://wallpaperscraft.com/", 14, color.mellowgreen, 10, 140, 1200)
txtelement_b2 = Text("Sprites & Icons: https://www.flaticon.com/, http://kidscancode.org/", 14, color.mellowgreen, 10, 160, 1200)

txtheader_c = Text("MUSIC", 18, color.slimegreen, 10, 200)
txtelement_c1 = Text("Background Musics: (1) https://www.youtube.com/watch?v=ewxxcH0mKDQ, (2) The real folk Blues, (3) Overtaken", 14, color.mellowgreen, 10, 230, 1200)
txtelement_c2 = Text("Sound Effects: https://www.zapsplat.com/sound-effect-categories/", 14, color.mellowgreen, 10, 270, 1200)


btnabouttomenu = Button(275, 500, 250, 50)
btnabouttomenu.text.set_properties("BACK TO MENU", 24, color.beige, 305, 513)
# endregion

# region INITIALIZATIONS: CHARACTER SELECT SCENE
player = SpaceShip()
player.change_ship(player.shiplist[0])
player.weapon.change_weapon(player.weapon.weapon_list[0])

btnwelcome = Button(-10, 5, screen_w + 20, 40)
btnwelcome.text.set_properties("SELECT YOUR SHIP AND WEAPONRY, PILOT!", 24, color.mellowgreen, 140, 14)

ships64 = [pygame.image.load("imgs/whiteship64.png"), pygame.image.load("imgs/transporter64.png"), pygame.image.load("imgs/battleship64.png")]
ships128 = [pygame.image.load("imgs/whiteship128.png"), pygame.image.load("imgs/transporter128.png"), pygame.image.load("imgs/battleship128.png")]
weapons32 = [pygame.image.load("imgs/missile32.png"), pygame.image.load("imgs/nuclear32.png"), pygame.image.load("imgs/reactor32.png")]
weapons64 = [pygame.image.load("imgs/missile64.png"), pygame.image.load("imgs/nuclear64.png"), pygame.image.load("imgs/reactor64.png")]

btnships = []
btnweapons = []
for i in range(3):
    btnwidth = 64 + 40
    marginy = 70 + (22 * (i + 1)) + (64+40)*i
    btnships.append(Button(50, marginy, btnwidth, btnwidth, True))
    btnships[i].set_image(ships64[i], 64)
    btnweapons.append(Button(204, marginy, btnwidth, btnwidth, True))
    btnweapons[i].set_image(weapons64[i], 64)
for i in range(3):
    btnships[i].text.set_properties(player.shiplist[i], 0, color.slimegreen, 0, screen_h)
btnships[0].select()
btnweapons[0].select()
btnweapons[0].text.set_properties("MISSILE TPF - VII: Simultaneously release 7 missiles in front and at the sides", 12, color.slimegreen, btnweapons[0].left + btnweapons[0].width + 10, btnweapons[0].top, 202)
btnweapons[1].text.set_properties("MISSILE MARU 1850: Fires 3 missiles which pierce through destructible objects along a line", 12, color.beige, btnweapons[1].left + btnweapons[1].width + 10, btnweapons[1].top, 202)
btnweapons[2].text.set_properties("BOMB ERUMA 1/2: Releases a homing bomb that locks unto the nearest visible space object", 12, color.beige, btnweapons[2].left + btnweapons[2].width + 10, btnweapons[2].top, 202)
btnshippreview = Button(520, 70 + 22, 230, 230)
btnshippreview.text.set_properties(btnships[0].text.label, 20, color.slimegreen, 530, 290)
btnshippreview.set_image(ships128[0], 128)
btnweaponpreview = Button(702, 274, 48, 48)
btnweaponpreview.set_image(weapons32[0], 32)

stats = [player.vel, player.durability, player.energy, player.bullet.ammo]
pbarstats = []
for i in range(4):
    pbarstats.append(ProgressBar(620, 344 + 28 * i, 130, 14, (62, 88, 105), (255, 221, 87)))
    pbarstats[i].update(stats[i], 5)
pbarstats[0].progresscolor = (255, 166, 51)
pbarstats[1].progresscolor = (23, 156, 99)
pbarstats[2].progresscolor = (96, 164, 247)
pbarstats[3].progresscolor = (227, 30, 47)
pbarstats[0].text.set_properties("Speed", 14, color.slimegreen, 520, 344)
pbarstats[1].text.set_properties("Durability", 14, color.slimegreen, 520, 372)
pbarstats[2].text.set_properties("Energy", 14, color.slimegreen, 520, 400)
pbarstats[3].text.set_properties("Ammunition", 14, color.slimegreen, 520, 428)

btncstomenu = Button(50, screen_h - 100, 258, 50)
btncstomenu.text.set_properties("BACK TO MENU", 24, color.beige, 85, screen_h - 100 + 13)
btnlaunch = Button(520, screen_h - 100, 230, 50)
btnlaunch.text.set_properties("LAUNCH", 24, color.beige, 585, screen_h - 100 + 13)
# endregion

# region INITIALIZATIONS: BATTLE SCENE
energy_gauge = EnergyBar()
level = Level()

asteroids = []
drones = []
drone_bullets = []
bullets = []

msg1 = Message()
msg2 = Message()
msglog = MessageLog()
fps = FPS(screen_w - 74, 10)
timer = Timer(26, screen_h - 32 - 12)

# endregion

# GAME LOOP
running = True
while running:
    game_state.state_manager()