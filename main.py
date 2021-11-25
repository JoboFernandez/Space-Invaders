from models import GameManager
import settings
import pygame
import os


pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders 1.0")
icon = pygame.image.load("imgs/spaceship32.png")
pygame.display.set_icon(icon)
pygame.mixer.music.load("musics/main_bgmusic.mp3")
pygame.mixer.music.play(-1)

game_manager = GameManager()
while True:
    game_manager.handle_events()
    game_manager.update_in_game_status()
    game_manager.draw(screen=screen)