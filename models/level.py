from . import Asteroid, Drone, MessageLog, Timer, SpaceShip, EnergyBar
import pygame


class Level:

    def __init__(self):
        self.level = 1
        self.asteroid_count = 0
        self.drone_count = 0
        self.time_limit = 0

        # state: 1=LevelCleared, 0=OngoingLevel, -1=LevelGameOver
        self.state = 0

    def next(self, msglog: MessageLog, timer: Timer):
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

    def reset(self, space_ship: SpaceShip, energy_gauge: EnergyBar, msglog: MessageLog, timer: Timer):
        pygame.mixer.music.load("musics/background01.mp3")
        pygame.mixer.music.play(-1)
        self.level = 1
        self.state = 0
        self.asteroid_count = 15
        self.drone_count = 1
        self.time_limit = 40
        space_ship.change_ship(space_ship.name)
        energy_gauge.energy = 0
        pygame.mouse.set_pos(400, 418)
        msglog.update("", (255,255,255))
        msglog.update("", (255,255,255))
        msglog.update("WELCOME TO LEVEL 1", (255,255,255))
        timer.start(self.time_limit)

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(pygame.font.Font("freesansbold.ttf", 32).render("Level : " + str(self.level), True, (255, 255, 255)), (620, 552))