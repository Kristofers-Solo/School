import pygame
from os.path import join, abspath, dirname

CELL_SIZE = 30
ROWS, COLUMNS = 30, 20
WIDTH, HEIGHT = ROWS * CELL_SIZE, COLUMNS * CELL_SIZE
WINDOW_HEIGHT = HEIGHT + 100
WINDOW = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.font.init()

BASE_PATH = abspath(dirname(__file__))
FONT = join(BASE_PATH, "fonts", "roboto.ttf")
SPRITE_PATH = join(BASE_PATH, "assets", "sprites")
APPLE_TEXTURE = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "golden_apple.png")), (CELL_SIZE, CELL_SIZE))
POISON_TEXTURE = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "poison.png")), (CELL_SIZE, CELL_SIZE))
COBBLESTONE_TEXTURE = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "cobblestone.jpeg")), (CELL_SIZE, CELL_SIZE))

RED = (255, 0, 0)
WHITE = (242, 242, 242)
GRAY = (204, 204, 204)
DARK_GRAY = (51, 51, 51)
BLACK = (0, 0, 0)
GREEN = (0, 128, 30)
PURPLE = (170, 0, 255)
BLUE = (85, 85, 255)

set_font = lambda size: pygame.font.Font(FONT, size)  # sets font size

fps = 10  # speed
multiplayer = False
walls = False


def change_speed() -> None:
	global fps
	if fps == 5: fps = 10
	elif fps == 10: fps = 15
	elif fps == 15: fps = 5


def switch_multiplayer() -> None:
	global multiplayer
	multiplayer = not multiplayer


def switch_walls() -> None:
	global walls
	walls = not walls
