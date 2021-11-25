from . import Text, Image
from utils import wraptxt
import settings
import pygame


class Button:

    def __init__(self, left: int, top: int, width: int, height: int, text: Text, image=None,
                 color=settings.COLORS["spacegray"], border_width=2, selected=False, has_selection=False):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
        self.selected = selected

        self.bg_color = pygame.Surface((width, height))
        self.bg_color.fill((0, 0, 0))
        self.bg_color.set_alpha(128)

        self.text = text
        # self.text.left = left
        # self.text.top = top

        self.img = image
        if image:
            self.img.left = self.left + (self.width - self.img.size) // 2
            self.img.top = self.top + (self.height - self.img.size) // 2

        self.has_selection = has_selection

    def mouse_is_over(self, pos: tuple):
        x, y = pos
        return True if (self.left < x < self.left + self.width) and (self.top < y < self.top + self.height) else False

    def glow(self):
        if not self.selected:
            self.text.color = settings.COLORS["beigeglow"]
            self.color = settings.COLORS["beigeglow"]

    def unglow(self):
        if not self.selected:
            self.text.color = settings.COLORS["beige"]
            self.color = settings.COLORS["spacegray"]

    def select(self):
        self.text.color = settings.COLORS["slimegreen"]
        self.color = settings.COLORS["slimegreen"]
        self.selected = True

    def unselect(self):
        self.text.color = settings.COLORS["beige"]
        self.color = settings.COLORS["spacegray"]
        self.selected = False

    def set_image(self, img: pygame.Surface, size: int):
        self.img.img = img
        self.img.size = size
        self.img.left = self.left + (self.width - size) // 2
        self.img.top = self.top + (self.height - size) // 2

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(self.bg_color, (self.left, self.top))
        pygame.draw.rect(screen, self.color, (round(self.left), round(self.top), round(self.width), round(self.height)), self.border_width)
        if self.img is not None:
            screen.blit(self.img.img, (self.img.left, self.img.top))

        # if object.text.label == '': lines = wraptxt(object.text.label, object.text.size, object.text.width)
        # else: lines = wraptxt(object.text.label, object.text.size, object.text.width)

        lines = wraptxt(self.text.label, self.text.size, self.text.width)
        for i in range(len(lines)):
            screen.blit(
                pygame.font.Font("freesansbold.ttf", self.text.size).render(lines[i], True, self.text.color),
                (round(self.text.left), round(self.text.top) + i * (self.text.size + 2)))

        if self.has_selection and not self.selected:
            greyout = pygame.Surface((self.width, self.height))
            greyout.fill((62, 88, 105))
            greyout.set_alpha(128)
            screen.blit(greyout, (self.left, self.top))