# Author - Kristiāns Francis Cagulis
# Date - 18.04.2022
# Title - Snake

import pygame
from random import randint
from os.path import abspath, dirname

from globals import *
from assets.scripts.score import *
from assets.scripts.menu import main_menu
from assets.scripts.classes import *
from assets.scripts.menu import FPS, multiplayer, walls

BASE_PATH = abspath(dirname(__file__))


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
	global run
	for snake in snakes:
		write_score(snake.name, len(snake.body), BASE_PATH)
	run = False


def main() -> None:
	global snakes
	pygame.display.set_caption("Snake")

	clock = pygame.time.Clock()
	snake_one = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), PURPLE, "test1")
	snakes.append(snake_one)

	if multiplayer:
		snake_two = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), BLUE, "test2", 2)
		snakes.append(snake_two)

	apple = Snack(apple_texture)
	collision_check(snakes, apple)
	poison = Snack(poison_texture)
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
				cobble_rect = pygame.Rect(i * CELL_SIZE, HEIGHT, WIDTH, CELL_SIZE)
				WINDOW.blit(cobblestone_texture, cobble_rect)
		pygame.display.update()

	while run:
		clock.tick(FPS)
		pygame.time.delay(0)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		for snake in snakes:
			snake.move()
			if snake.body[0].pos == apple.pos:
				snake.add_cube()
				apple = Snack(apple_texture)
				collision_check(snakes, apple)

			if snake.body[0].pos == poison.pos:
				if len(snake.body) > 1:
					snake.remove_cube()
				poison = Snack(poison_texture)
				collision_check(snakes, poison)

			for i in range(len(snake.body)):
				if snake.body[i].pos in list(map(lambda z: z.pos, snake.body[i + 1:])):
					end_screen()
		redraw_window()


if __name__ == '__main__':
	main_menu()
	# for i in range(50, 100):
	# 	write_score(f"test{i}", randint(1, 1_000_000), BASE_PATH)
	# csv_file = read_score(BASE_PATH)
	# # print(csv_file)
	# for line in sort(csv_file, reverse=True):
	# 	print(line)
