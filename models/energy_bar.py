from math import pi
import pygame


class EnergyBar:

    def __init__(self):
        self.energy = 0
        self.limit = 100
        self.bar_angle = 0
        self.notified = False

    def update(self, increment=0):
        if self.energy + increment > self.limit:
            self.energy = self.limit
        else:
            self.energy += increment
        self.bar_angle = 2 * pi * self.energy / self.limit

    def expend(self):
        self.energy = 0
        self.bar_angle = 0
        self.notified = False

    def notify(self):
        self.notified = True

    def draw(self, screen: pygame.display.set_mode):
        pygame.draw.arc(screen, (62, 88, 105), (538, 541, 56, 56), 0, 2 * pi, 6)
        pygame.draw.arc(screen, (96, 164, 247), (538, 541, 56, 56), 0, self.bar_angle, 6)
        pygame.draw.arc(screen, (155, 198, 250), (540, 543, 52, 52), 0, self.bar_angle, 4)
        pygame.draw.arc(screen, (205, 226, 252), (542, 545, 48, 48), 0, self.bar_angle, 2)