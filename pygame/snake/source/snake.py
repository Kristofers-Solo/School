# Author - Kristiāns Francis Cagulis
# Date - 23.04.2022
# Title - Snake

import pygame
from random import randint
from os.path import abspath, dirname

from globals import *
from assets.scripts.score import *
from assets.scripts.menu import main_menu
from assets.scripts.classes import *

BASE_PATH = abspath(dirname(__file__))

snakes = []


def draw_grid() -> None:
	x, y = 0, 0
	for _ in range(ROWS):
		x += CELL_SIZE
		pygame.draw.line(WINDOW, WHITE, (x, 0), (x, HEIGHT))
	for _ in range(COLUMNS):
		y += CELL_SIZE
		pygame.draw.line(WINDOW, WHITE, (0, y), (WIDTH, y))


def draw_score(snakes) -> None:
	for index, snake in enumerate(snakes):
		score_label = set_font(40).render(f"Score {len(snake.body) - 1}", 1, snake.color)
		WINDOW.blit(score_label, (10 + (index * (WIDTH - score_label.get_width() - 20)), (WINDOW_HEIGHT - score_label.get_height())))


def collision_check(snakes, snack) -> None:
	for snake in snakes:
		for block in snake.body:
			if block.pos == snack.pos:
				snack.randomize()


def end_screen() -> None:
	for snake in snakes:
		if len(snake.body) > 1:
			write_score(snake.name, len(snake.body) - 1, BASE_PATH)
	main_menu()


def main() -> None:
	snakes.clear()
	from globals import fps, multiplayer, walls
	pygame.display.set_caption("Snake")

	clock = pygame.time.Clock()
	from assets.scripts.menu import user_name, color_index
	snake_one = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), COLORS[color_index[0]], user_name[0], 1, multiplayer)
	snakes.append(snake_one)

	if multiplayer:
		snake_two = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), COLORS[color_index[1]], user_name[1], 2, multiplayer)
		snakes.append(snake_two)
	apple = Snack(APPLE_TEXTURE)
	collision_check(snakes, apple)
	poison = Snack(POISON_TEXTURE)
	collision_check(snakes, poison)

	def redraw_window() -> None:
		WINDOW.fill(BLACK)
		draw_grid()
		draw_score(snakes)
		for snake in snakes:
			snake.draw()
		apple.draw_snack()
		poison.draw_snack()
		if walls:
			for i in range(ROWS):
				COBBLE_RECT = pygame.Rect(i * CELL_SIZE, HEIGHT, WIDTH, CELL_SIZE)
				WINDOW.blit(COBBLESTONE_TEXTURE, COBBLE_RECT)
		pygame.display.update()

	while True:
		clock.tick(fps)
		pygame.time.delay(0)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					end_screen()

		for snake in snakes:
			snake.move()
			if snake.body[0].pos == apple.pos:
				snake.add_cube()
				apple = Snack(APPLE_TEXTURE)
				collision_check(snakes, apple)

			if snake.body[0].pos == poison.pos:
				if len(snake.body) > 1:
					snake.remove_cube()
				poison = Snack(POISON_TEXTURE)
				collision_check(snakes, poison)

			for i in range(len(snake.body)):
				if snake.body[i].pos in list(map(lambda z: z.pos, snake.body[i + 1:])):
					end_screen()
		if multiplayer:
			for i in snakes[0].body:
				if i.pos == snakes[1].head.pos:
					end_screen()
			for i in snakes[1].body:
				if i.pos == snakes[0].head.pos:
					end_screen()

		redraw_window()


if __name__ == '__main__':
	main_menu()