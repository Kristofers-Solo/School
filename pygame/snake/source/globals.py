import pygame
from os.path import join, abspath, dirname

CELL_SIZE = 30
ROWS, COLUMNS = 30, 20
WIDTH, HEIGHT = ROWS * CELL_SIZE, COLUMNS * CELL_SIZE
WINDOW_HEIGHT = HEIGHT + 100
WINDOW = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.font.init()
pygame.display.set_caption("Snake")

BASE_PATH = abspath(dirname(__file__))
SPRITE_PATH = join(BASE_PATH, "assets", "sprites")
apple_texture = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "golden_apple.png")), (CELL_SIZE, CELL_SIZE))
poison_texture = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "poison.png")), (CELL_SIZE, CELL_SIZE))
cobblestone_texture = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "cobblestone.jpeg")), (CELL_SIZE, CELL_SIZE))
FONT = join(BASE_PATH, "fonts", "roboto.ttf")

RED = (255, 0, 0)
WHITE = (242, 242, 242)
GRAY = (204, 204, 204)
DARK_GRAY = (51, 51, 51)
BLACK = (0, 0, 0)
GREEN = (0, 128, 30)
PURPLE = (170, 0, 255)
BLUE = (85, 85, 255)

set_font = lambda size: pygame.font.Font(FONT, size)  # sets font size

FPS = 10  # speed
multiplayer = False
walls = False
