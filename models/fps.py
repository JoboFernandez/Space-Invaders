from random import randint
import pygame


class FPS:

    def __init__(self, left: int, top: int):
        self.left = left
        self.top = top
        self.frames = 0
        self.fps = randint(60, 115)
        self.color = (0, 255, 0)
        self.time1 = pygame.time.get_ticks()

    def update(self, inc=1):
        if (pygame.time.get_ticks() - self.time1) // 1000 >= 1:
            self.time1 = pygame.time.get_ticks()
            self.fps = self.frames
            self.frames = 0
        self.frames += inc

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(pygame.font.Font('freesansbold.ttf', 16).render(str(self.fps) + " FPS", True, self.color), (self.left, self.top))
