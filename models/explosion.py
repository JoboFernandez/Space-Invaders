import pygame


explosion_frames = []
explosion_frames_small = []
for i in range(9):
    filename = f"imgs/regularExplosion0{i}.png"
    explosion_frames.append(pygame.image.load(filename))
    small = pygame.transform.scale(explosion_frames[i], (32, 32))
    explosion_frames_small.append(small)


class Explosion:

    def __init__(self):
        self.left = 0
        self.top = -600
        self.img = explosion_frames[0]
        self.frame = 0
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()
        self.ongoing = False
        self.center_x = self.left
        self.center_y = self.top
        self.size = "large"

    def update(self):
        if self.ongoing:
            if self.size == "large":
                self.left = self.center_x - explosion_frames[self.frame].get_rect()[2] / 2
                self.top = self.center_y - explosion_frames[self.frame].get_rect()[2] / 2
            else:
                self.left = self.center_x - 16
                self.top = self.center_y - 16
            now = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.last_update >= self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame < 9:
                    if self.size == "large":
                        self.img = explosion_frames[self.frame]
                    else:
                        self.img = explosion_frames_small[self.frame]
                else:
                    self.frame = 0
                    self.hide()

    def hide(self):
        self.left = 0
        self.top = -600
        self.ongoing = False

    def show(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.ongoing = True
