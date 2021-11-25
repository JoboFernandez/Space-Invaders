from models import Asteroid, Bullet, Button, Drone, EnergyBar, FPS, Level, Message, MessageLog, ProgressBar, SpaceShip, Text, Image, Timer, Weapon
import settings
import sys
import pygame


level = Level()
space_ship = SpaceShip()
space_ship.change_ship(settings.SHIP_LIST[0])
space_ship.weapon.change_weapon(settings.WEAPON_LIST[0])

energy_gauge = EnergyBar()
msg1 = Message()
msg2 = Message()
msglog = MessageLog()
fps = FPS(settings.SCREEN_WIDTH - 74, 10)
timer = Timer(26, settings.SCREEN_HEIGHT - 32 - 12)

# asteroids = [Asteroid() for _ in range(level.asteroid_count)]
# drones = [Drone() for _ in range(level.drone_count)]
# drone_bullets = [drone.bullet for drone in drones]
# bullets = [Bullet() for _ in range(space_ship.bullet.ammo)]
asteroids = []
drones = []
drone_bullets = []
bullets = []

menu_buttons = [
    Button(left=160, top=162, width=480, height=75,
           text=Text(label="PLAY SURVIVAL MODE", size=33, left=214, top=185, color=settings.COLORS["beigeglow"])),
    Button(left=160, top=262, width=480, height=75,
           text=Text(label="ABOUT THE GAME & CREDITS", size=25, left=212, top=290, color=settings.COLORS["beigeglow"])),
    Button(left=160, top=362, width=480, height=75,
           text=Text(label="EXIT", size=50, left=340, top=378, color=settings.COLORS["beigeglow"])),
]

about_and_credits_texts = [
    Text(label="ABOUT THE GAME", size=18, left=10, top=10, color=settings.COLORS["slimegreen"]),
    Text(label="This game is developed by Jobo solely for the purpose of coding practice. Not all products used herein are created by the game developer. That said, the developer would like to give credit to where it is due.",
         size=14, left=10, top=40, width=1200, wrap=True, color=settings.COLORS["mellowgreen"]),
    Text(label="GRAPHICS", size=18, left=10, top=110, color=settings.COLORS["slimegreen"]),
    Text(label="Background Images: https://wallpaperscraft.com/", size=14, left=10, top=140, width=1200, color=settings.COLORS["mellowgreen"]),
    Text(label="Sprites & Icons: https://www.flaticon.com/, http://kidscancode.org/",
         size=14, left=10, top=160, width=1200, color=settings.COLORS["mellowgreen"]),
    Text(label="MUSIC", size=18, left=10, top=200, color=settings.COLORS["slimegreen"]),
    Text(label="Background Musics: (1) https://www.youtube.com/watch?v=ewxxcH0mKDQ, (2) The real folk Blues, (3) Overtaken",
         size=14, left=10, top=230, width=1200, wrap=True, color=settings.COLORS["mellowgreen"]),
    Text(label="Sound Effects: https://www.zapsplat.com/sound-effect-categories/",
         size=14, left=10, top=270, width=1200, color=settings.COLORS["mellowgreen"]),
]
about_and_credits_buttons = [
    Button(left=275, top=500, width=250, height=50,
           text=Text(label="BACK TO MENU", size=24, left=305, top=513, color=settings.COLORS["beige"])),
]

ships64 = [pygame.image.load("imgs/whiteship64.png"), pygame.image.load("imgs/transporter64.png"), pygame.image.load("imgs/battleship64.png")]
ships128 = [pygame.image.load("imgs/whiteship128.png"), pygame.image.load("imgs/transporter128.png"), pygame.image.load("imgs/battleship128.png")]
weapons32 = [pygame.image.load("imgs/missile32.png"), pygame.image.load("imgs/nuclear32.png"), pygame.image.load("imgs/reactor32.png")]
weapons64 = [pygame.image.load("imgs/missile64.png"), pygame.image.load("imgs/nuclear64.png"), pygame.image.load("imgs/reactor64.png")]
selection_buttons = [
    Button(left=-10, top=5, width=settings.SCREEN_WIDTH+20, height=40,
           text=Text(label="SELECT YOUR SHIP AND WEAPONRY, PILOT!", size=24, left=140, top=14, color=settings.COLORS["mellowgreen"])),
    Button(left=50, top=settings.SCREEN_HEIGHT-100, width=258, height=50,
           text=Text(label="BACK TO MENU", size=24, left=85, top=settings.SCREEN_HEIGHT-87, color=settings.COLORS["beige"])),
    Button(left=520, top=settings.SCREEN_HEIGHT-100, width=230, height=50,
           text=Text(label="LAUNCH", size=24, left=585, top=settings.SCREEN_HEIGHT-87, color=settings.COLORS["beige"])),
]
selection_ship_buttons = [
    Button(left=50, top=94+126*i, width=104, height=104, has_selection=True,
           text=Text(label=settings.SHIP_LIST[i], size=0, left=0, top=settings.SCREEN_HEIGHT, color=settings.COLORS["slimegreen"]),
           image=Image(image=ships64[i], size=64)) for i in range(3)
]
selection_weapon_buttons = [
    Button(left=204, top=94, width=104, height=104, has_selection=True,
           text=Text(label="MISSILE TPF - VII: Simultaneously release 7 missiles in front and at the sides", size=12, left=318, top=94, width=202, color=settings.COLORS["slimegreen"]),
           image=Image(image=weapons64[0], size=64)),
    Button(left=204, top=220, width=104, height=104, has_selection=True,
           text=Text(label="MISSILE MARU 1850: Fires 3 missiles which pierce through destructible objects along a line", size=12, left=318, top=220, width=202, color=settings.COLORS["beige"]),
           image=Image(image=weapons64[1], size=64)),
    Button(left=204, top=346, width=104, height=104, has_selection=True,
           text=Text(label="BOMB ERUMA 1/2: Releases a homing bomb that locks unto the nearest visible space object", size=12, left=318, top=346, width=202, color=settings.COLORS["beige"]),
           image=Image(image=weapons64[2], size=64)),
]
selection_ship_preview = Button(left=520, top=92, width=230, height=230,
                                text=Text(label=selection_ship_buttons[0].text.label, size=20, left=530, top=290, color=settings.COLORS["slimegreen"]),
                                image=Image(image=ships128[0], size=128))
selection_weapon_preview = Button(left=702, top=274, width=48, height=48, text=Text(),
                                  image=Image(image=weapons32[0], size=32))
selection_progress_bars = [
    ProgressBar(left=620, top=344, width=130, height=14, back_color=(62, 88, 105), progress_color=(255, 166, 51), progress_width=space_ship.vel,
                text=Text(label="Speed", size=14, left=520, top=344, color=settings.COLORS["slimegreen"])),
    ProgressBar(left=620, top=372, width=130, height=14, back_color=(62, 88, 105), progress_color=(23, 156, 99), progress_width=space_ship.durability,
                text=Text(label="Durability", size=14, left=520, top=372, color=settings.COLORS["slimegreen"])),
    ProgressBar(left=620, top=400, width=130, height=14, back_color=(62, 88, 105), progress_color=(96, 164, 247), progress_width=space_ship.energy,
                text=Text(label="Energy", size=14, left=520, top=400, color=settings.COLORS["slimegreen"])),
    ProgressBar(left=620, top=428, width=130, height=14, back_color=(62, 88, 105), progress_color=(227, 30, 47), progress_width=space_ship.bullet.ammo,
                text=Text(label="Ammunition", size=14, left=520, top=428, color=settings.COLORS["slimegreen"])),
]
selection_ship_buttons[0].select()
selection_weapon_buttons[0].select()
stats = [space_ship.vel, space_ship.durability, space_ship.energy, space_ship.bullet.ammo]
for progress_bar, stat in zip(selection_progress_bars, stats):
    progress_bar.update(stat, 5)


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
    for i in range(space_ship.bullet.ammo):
        bullets.append(Bullet())


class GameManager:

    def __init__(self):
        self.state = 'menu'
        self.state_scheduler = {
            "menu": {
                "event handler": self.handle_event_menu,
                "objects": menu_buttons,
                "background": pygame.image.load("imgs/bg_intro.jpg"),
            },
            "about": {
                "event handler": self.handle_event_about,
                "objects": about_and_credits_texts + about_and_credits_buttons,
                "background": pygame.image.load("imgs/bg_about.jpg"),
            },
            "selection": {
                "event handler": self.handle_event_selection,
                "objects": selection_buttons + selection_ship_buttons + selection_weapon_buttons + [selection_ship_preview] + [selection_weapon_preview] + selection_progress_bars,
                "background": pygame.image.load("imgs/bg_shop.jpg"),
            },
            "in-game": {
                "event handler": self.handle_event_in_game,
                "objects": [],
                "background": pygame.image.load("imgs/bg_space.jpg"),
            },
        }

    def handle_events(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            # handle exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # handle event by game state
            self.state_scheduler[self.state]["event handler"](event=event, pos=pos)

    def handle_event_menu(self, event: pygame.event.Event, pos: tuple):
        if event.type == pygame.MOUSEMOTION:
            # button mouse over: select and unselect
            for button in menu_buttons:
                button.select() if button.mouse_is_over(pos) else button.unselect()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # button click: exit
            if menu_buttons[-1].mouse_is_over(pos):
                pygame.quit()
                sys.exit()

            # button click: play game
            if menu_buttons[0].mouse_is_over(pos):
                pygame.mixer.music.load("musics/shop_bgmusic.mp3")
                pygame.mixer.music.play(-1)
                self.state = 'selection'

            # button click: about the game
            if menu_buttons[1].mouse_is_over(pos):
                self.state = 'about'

    def handle_event_about(self, event: pygame.event.Event, pos: tuple):
        if event.type == pygame.MOUSEMOTION:
            # button mouse over: glow & unglow
            for button in about_and_credits_buttons:
                button.glow() if button.mouse_is_over(pos) else button.unglow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # button click: back to menu
            if about_and_credits_buttons[0].mouse_is_over(pos):
                self.state = 'menu'

    def handle_event_selection(self, event: pygame.event.Event, pos: tuple):
        if event.type == pygame.MOUSEMOTION:
            # handle button mouse over
            selection_buttons[0].text.color = settings.COLORS["slimegreen"] if selection_buttons[0].mouse_is_over(pos) else settings.COLORS["mellowgreen"]
            for button in selection_ship_buttons + selection_weapon_buttons + selection_buttons[1:]:
                button.glow() if button.mouse_is_over(pos=pos) else button.unglow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # button click: back to menu
            if selection_buttons[1].mouse_is_over(pos):
                pygame.mixer.music.load("musics/main_bgmusic.mp3")
                pygame.mixer.music.play(-1)
                self.state = 'menu'

            if selection_buttons[2].mouse_is_over(pos):
                # button click: launch game
                level.reset(space_ship, energy_gauge, msglog, timer)
                initiate_objects()
                self.update_in_game_objects()
                self.state = 'in-game'

            for i in range(3):
                # button click: ship is chosen
                if selection_ship_buttons[i].mouse_is_over(pos):
                    selection_ship_buttons[i].select()
                    space_ship.change_ship(settings.SHIP_LIST[i])

                    # update preview
                    selection_ship_preview.set_image(ships128[i], 128)
                    selection_ship_preview.text.label = selection_ship_buttons[i].text.label
                    stats = [space_ship.vel, space_ship.durability, space_ship.energy, space_ship.bullet.ammo]
                    for j in range(len(stats)):
                        selection_progress_bars[j].update(stats[j], 5)

                    # unselect other ship buttons
                    for j in range(len(selection_ship_buttons)):
                        if j != i:
                            selection_ship_buttons[j].unselect()

                # button click: weapon is chosen
                if selection_weapon_buttons[i].mouse_is_over(pos):
                    selection_weapon_buttons[i].select()
                    space_ship.weapon.change_weapon(settings.WEAPON_LIST[i])

                    # update preview
                    selection_weapon_preview.set_image(weapons32[i], 32)

                    # unselect other weapon buttons
                    for j in range(3):
                        if j != i:
                            selection_weapon_buttons[j].unselect()

    def handle_event_in_game(self, event: pygame.event.Event, pos: tuple):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # game lost: back to selection state
                if level.state == -1:
                    pygame.mixer.music.load("musics/shop_bgmusic.mp3")
                    pygame.mixer.music.play(-1)
                    space_ship.change_ship(space_ship.name)
                    space_ship.weapon.change_weapon(space_ship.weapon.name)
                    self.state = 'selection'
                # game won: go to next level
                elif level.state == 1:
                    level.next(msglog, timer)
                    initiate_objects()
                    self.update_in_game_objects()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # fire bullets
            if event.button == 1 and level.state == 0:
                space_ship.fire(bullets)

            # fire special weapon
            if event.button == 3 and level.state == 0:
                if energy_gauge.energy == energy_gauge.limit:
                    space_ship.fire_specialweapon()
                    if space_ship.weapon.name == settings.WEAPON_LIST[2]:
                        space_ship.weapon.detecting = True
                    energy_gauge.expend()
                    msglog.update("ENERGY EXPENDED", settings.COLORS["mellowgreen"])
                else:
                    msglog.update("INSUFFICIENT ENERGY", settings.COLORS["spacegray"])
                    pygame.mixer.Sound("musics/insufficient_energy.wav").play(0, 0, 0)

    def update_in_game_status(self):
        if self.state != "in-game":
            return

        pos = pygame.mouse.get_pos()

        # update player space ship
        space_ship.follow(pos)
        if level.state == -1:
            space_ship.hide()
        space_ship.detect_collision(asteroids + drones + drone_bullets, level, msglog)

        # update player bullets
        for i in range(space_ship.bullet.ammo):
            bullets[i].move()
            bullets[i].detect_collision(asteroids + drones + drone_bullets, space_ship, energy_gauge)
            bullets[i].bring_to_ship(space_ship)

        # update energy bar
        energy_gauge.update()
        if energy_gauge.energy == energy_gauge.limit and not energy_gauge.notified:
            msglog.update("WEAPON READY!!!", settings.COLORS["blue"])
            energy_gauge.notify()

        # update special weapon
        if space_ship.weapon.detecting:
            space_ship.weapon.nearest_object = space_ship.weapon.detect_nearest_object(asteroids + drones + drone_bullets)
            space_ship.weapon.detecting = False
        space_ship.weapon.move()
        space_ship.weapon.detect_collision(asteroids + drones + drone_bullets)
        if space_ship.weapon.detonate:
            space_ship.weapon.explode(asteroids + drones + drone_bullets)

        # update drones
        for i in range(len(drones)):
            drones[i].follow(space_ship)
            drones[i].bullet.move("fromdrone")
            drones[i].explosion.update()
            drones[i].bullet.explosion.update()

        # update asteroids
        for i in range(len(asteroids)):
            asteroids[i].move()
            asteroids[i].explosion.update()

        # game lost
        if level.state == -1:
            msg1.set("GAME OVER", 64, settings.COLORS["red"], settings.SCREEN_WIDTH // 4, settings.SCREEN_HEIGHT // 2 - 32)
            msg2.set("<< Press Space Bar to go back to character select >>", 16, settings.COLORS["red"], settings.SCREEN_WIDTH // 4 - 5,
                     settings.SCREEN_HEIGHT // 2 + 64)
            timer.updatecolor(settings.COLORS["red"])

        # in-game
        if level.state == 0:
            msg1.msg = ""
            msg2.msg = ""
            rem = timer.remaining()
            if rem <= 0:
                timer.updatecolor(settings.COLORS["blue"]); level.state = 1
            elif 0 < rem <= 15:
                timer.updatecolor(settings.COLORS["orange"])
            else:
                timer.updatecolor(settings.COLORS["green"])
        # game won or lost
        else:
            for i in range(len(asteroids)):
                if asteroids[i].ypos > -64:
                    asteroids[i].hide()
                    asteroids[i].explode()
            for i in range(len(drones)):
                if drones[i].xpos > -128:
                    drones[i].explode()
                    drones[i].bullet.explode()
                    drones[i].bullet.onfire = False
        # game won
        if level.state == 1:
            msg1.set("SPACE LEVEL INVADED", 64, settings.COLORS["blue"], 30, settings.SCREEN_HEIGHT // 2 - 32)
            msg2.set("<< Press Space Bar to proceed to the next level >>", 16, settings.COLORS["blue"], settings.SCREEN_WIDTH // 4 + 15,
                     settings.SCREEN_HEIGHT // 2 + 64)

        # update fps reading
        fps.update()

    def update_in_game_objects(self):
        self.state_scheduler["in-game"]["objects"] = asteroids + drones + bullets + [space_ship] + [fps] + [timer] + [msglog] + [level] + [energy_gauge]

    def draw(self, screen: pygame.display.set_mode):
        screen.fill((0, 0, 0))
        screen.blit(self.state_scheduler[self.state]["background"], (0, 0))

        if self.state == "selection":
            # draw additional line division
            pygame.draw.line(screen, settings.COLORS["spacegray"], (179, 92), (179, 448), 5)
        elif self.state == "in-game":
            # draw dashboard
            pygame.draw.rect(screen, settings.COLORS["black"], (0, settings.SCREEN_HEIGHT - 64, 800, 64))
            pygame.draw.line(screen, settings.COLORS["cockpit_expt"], (0, settings.SCREEN_HEIGHT - 64), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - 64), 5)
            pygame.draw.line(screen, settings.COLORS["cockpit_expt"], (280, 539), (280, 600), 5)
            pygame.draw.line(screen, settings.COLORS["cockpit_expt"], (520, 539), (520, 600), 5)
            screen.blit(space_ship.weapon.img, (550, 552))
            for i in range(space_ship.durability - 1):
                screen.blit(space_ship.avatar, (130 + i * 32, settings.SCREEN_HEIGHT - 16 - 32))

            # draw end-game messages
            screen.blit(pygame.font.Font("freesansbold.ttf", msg1.size).render(msg1.msg, True, msg1.color), (msg1.left, msg1.top))
            screen.blit(pygame.font.Font("freesansbold.ttf", msg2.size).render(msg2.msg, True, msg2.color), (msg2.left, msg2.top))

        # draw game state objects
        for obj in self.state_scheduler[self.state]["objects"]:
            obj.draw(screen=screen)

        # update display
        pygame.display.update()

