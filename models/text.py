from utils import wraptxt
import pygame


class Text:

    def __init__(self, label="", size=12, color=(0, 0, 0), left=0, top=0, width=None, wrap=False):
        self.label = label
        self.size = size
        self.color = color
        self.left = left
        self.top = top
        self.width = self.size * len(self.label) if width is None else width
        self.wrap = wrap

    def draw(self, screen: pygame.display.set_mode):
        if self.wrap:
            lines = wraptxt(text=self.label, fontsize=self.size, width=self.width)
        else:
            lines = [self.label]

        for i in range(len(lines)):
            screen.blit(pygame.font.Font("freesansbold.ttf", self.size).render(lines[i], True, self.color),
                        (round(self.left), round(self.top) + i * (self.size + 2)))
