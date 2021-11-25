import pygame


class Timer:

    def __init__(self, left: int, top: int):
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

    def updatecolor(self, color: tuple):
        self.color = color

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(pygame.font.Font('freesansbold.ttf', 24).render(f"{self.mm:02d} : {self.ss:02d}", True, self.color), (self.left, self.top))