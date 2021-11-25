import pygame


class MessageLog:

    def __init__(self):
        self.msg = ["", "", ""]
        self.color = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.left = 290
        self.tops = [542, 562, 582]

    def update(self, msg: str, color: tuple):
        self.msg = self.msg[1:] + [msg]
        self.color = self.color[1:] + [color]

    def draw(self, screen: pygame.display.set_mode):
        for i in range(3):
            screen.blit(pygame.font.Font("freesansbold.ttf", 14).render(self.msg[i], True, self.color[i]), (self.left, self.tops[i]))
