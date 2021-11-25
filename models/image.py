import pygame


class Image:

    def __init__(self, image=None, size=0, left=0, top=-600):
        # self.img = pygame.image.load("imgs/battleship32.png")
        self.img = image
        self.size = size
        self.left = left
        self.top = top
