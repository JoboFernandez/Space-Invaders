import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

COLORS = {
    "beige": (255, 179, 160),
    "beigeglow": (248, 193, 188),
    "black": (0, 0, 0),
    "blue": (0, 200, 200),
    "cockpit": (62, 79, 99),
    "cockpit_expt": (31, 40, 50),
    "green": (0, 255, 0),
    "mellowgreen": (76, 196, 40),
    "orange": (255, 127, 39),
    "red": (255, 0, 0),
    "slimegreen": (182, 252, 116),
    "spacegray": (62, 88, 105),
    "white": (255, 255, 255),
}

SHIP_LIST = ["ZCEVERINESKY", "RXCRAP", "PSTRYK"]
SHIP_IMAGES = [
    pygame.image.load("imgs/whiteship64.png"),
    pygame.image.load("imgs/transporter64.png"),
    pygame.image.load("imgs/battleship64.png")
]
SHIP_AVATARS = [
    pygame.image.load("imgs/whiteship32.png"),
    pygame.image.load("imgs/transporter32.png"),
    pygame.image.load("imgs/battleship32.png")
]

WEAPON_LIST = ["TPF7", "MARUNA", "ERUMA"]
WEAPON_IMAGES = [
    pygame.image.load("imgs/missile32.png"),
    pygame.image.load("imgs/nuclear32.png"),
    pygame.image.load("imgs/reactor32.png")
]