from . import Text
import pygame


class ProgressBar:

    def __init__(self, left: int, top: int, width: int, height: int, back_color: tuple, progress_color: tuple, text: Text, progress_width=0):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.back_color = back_color
        self.progress_color = progress_color
        self.progress_left = self.left + 2
        self.progress_top = self.top + 2
        self.progress_height = self.height - 3
        self.progress_width = progress_width

        self.text = text
        # self.text.left = left
        # self.text.top = top

    def update(self, progress: int, limit: int):
        self.progress_width = int(progress * self.width / limit)

    def draw(self, screen: pygame.display.set_mode):
        pbarbg = pygame.Surface((self.width, 14))
        pbarbg.fill((0, 0, 0))
        pbarbg.set_alpha(128)
        screen.blit(pbarbg, (self.left, self.top))
        pygame.draw.rect(screen, self.back_color, (round(self.left), round(self.top), round(self.width), round(self.height)), 2)
        pygame.draw.rect(screen, self.progress_color, (round(self.progress_left), round(self.progress_top), round(self.progress_width), round(self.progress_height)))
        pbarlight = pygame.Surface((self.progress_width, self.progress_height - 5))
        pbarlight.fill((255, 255, 255))
        pbarlight.set_alpha(96)
        screen.blit(pbarlight, (self.progress_left, self.progress_top + self.height // 3))
        pbarlight = pygame.Surface((self.progress_width, self.progress_height - (2 * self.progress_height // 3)))
        pbarlight.fill((255, 255, 255))
        pbarlight.set_alpha(128)
        screen.blit(pbarlight, (self.progress_left, self.progress_top + self.height // 3 + 4))
        screen.blit(pygame.font.Font("freesansbold.ttf", self.text.size).render(self.text.label, True, self.text.color), (round(self.text.left), round(self.text.top)))