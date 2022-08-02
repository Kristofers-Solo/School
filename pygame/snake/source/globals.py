from os.path import join, abspath, dirname
import pygame

CELL_SIZE = 30
ROWS, COLUMNS = 30, 20
WIDTH, HEIGHT = ROWS * CELL_SIZE, COLUMNS * CELL_SIZE
WINDOW_HEIGHT = HEIGHT + 100
WINDOW = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.font.init()

BASE_PATH = abspath(dirname(__file__))
FONT = join(BASE_PATH, "fonts", "roboto.ttf")
SPRITE_PATH = join(BASE_PATH, "assets", "sprites")
APPLE_TEXTURE = pygame.transform.scale(pygame.image.load(
    join(SPRITE_PATH, "golden_apple.png")), (CELL_SIZE, CELL_SIZE))
POISON_TEXTURE = pygame.transform.scale(pygame.image.load(
    join(SPRITE_PATH, "poison.png")), (CELL_SIZE, CELL_SIZE))
COBBLESTONE_TEXTURE = pygame.transform.scale(pygame.image.load(
    join(SPRITE_PATH, "cobblestone.jpeg")), (CELL_SIZE, CELL_SIZE))

BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 170)
DARK_GREEN = (0, 170, 0)
DARK_AQUA = (0, 170, 170)
DARK_RED = (170, 0, 0)
DARK_PURPLE = (170, 170, 0)
GOLD = (255, 170, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (85, 85, 85)
BLUE = (85, 85, 255)
GREEN = (85, 255, 85)
AQUA = (85, 255, 255)
RED = (255, 85, 85)
LIGHT_PURPLE = (255, 85, 255)
YELLOW = (255, 255, 85)
WHITE = (242, 242, 242)

COLORS = [DARK_BLUE, DARK_GREEN, DARK_AQUA, DARK_RED, DARK_PURPLE,
          GOLD, BLUE, GREEN, AQUA, RED, LIGHT_PURPLE, YELLOW]


def set_font(size): return pygame.font.Font(FONT, size)  # sets font size


fps = 10  # speed
multiplayer = False
walls = False


def change_speed() -> None:
    global fps
    if fps == 5:
        fps = 10
    elif fps == 10:
        fps = 15
    elif fps == 15:
        fps = 5


def switch_multiplayer() -> None:
    global multiplayer
    multiplayer = not multiplayer


def switch_walls() -> None:
    global walls
    walls = not walls
