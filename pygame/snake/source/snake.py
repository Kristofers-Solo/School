# Author - Kristiāns Francis Cagulis
# Date - 10.04.2022
# Title - Snake

import pygame
from random import randrange, randint
from os.path import abspath, dirname, join

CELL_SIZE = 30
ROWS, COLUMNS = 30, 20
WIDTH, HEIGHT = ROWS * CELL_SIZE, COLUMNS * CELL_SIZE
WINDOW_HEIGHT = HEIGHT + 100
WINDOW = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.font.init()
pygame.display.set_caption("Snake")

BASE_PATH = abspath(dirname(__file__))
SPRITE_PATH = join(BASE_PATH, "assets", "sprites")
FONT = join(BASE_PATH, "fonts", "roboto.ttf")

apple_texture = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "golden_apple.png")), (CELL_SIZE, CELL_SIZE))
poison_texture = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "poison.png")), (CELL_SIZE, CELL_SIZE))
cobblestone_texture = pygame.transform.scale(pygame.image.load(join(SPRITE_PATH, "cobblestone.jpeg")), (CELL_SIZE, CELL_SIZE))

RED = (255, 0, 0)
WHITE = (242, 242, 242)
GRAY = (204, 204, 204)
DARK_GRAY = (51, 51, 51)
BLACK = (0, 0, 0)
GREEN = (0, 128, 30)
PURPLE = (170, 0, 255)
BLUE = (85, 85, 255)
RANDOM_COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))

multiplayer = False
walls = False


class Cube:

	def __init__(self, position, color=RANDOM_COLOR) -> None:
		self.pos = position
		self.direction = (1, 0)
		self.color = color

	def move(self, direction: tuple) -> None:
		self.direction = direction
		self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])

	def draw(self, eyes=False) -> None:
		distance = WIDTH // ROWS
		i, j = self.pos

		pygame.draw.rect(WINDOW, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))
		if eyes:
			center = distance // 2
			radius = 3
			circle_middle = (i * distance + center - radius, j * distance + 8)
			circle_middle_2 = (i * distance + distance - radius * 2, j * distance + 8)
			pygame.draw.circle(WINDOW, BLACK, circle_middle, radius)
			pygame.draw.circle(WINDOW, BLACK, circle_middle_2, radius)


class Snake:

	def __init__(self, pos: tuple, color: tuple, player_number: int = 1) -> None:
		self.color = color
		self.head = Cube(pos, self.color)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.direction = (1, 0)
		self.number = player_number

	def move(self) -> None:
		keys = pygame.key.get_pressed()
		if multiplayer:
			num_1, num_2 = 1, 2
		else:
			num_1, num_2 = 1, 1

		if self.number == num_1:
			if keys[pygame.K_LEFT] and self.direction != (1, 0):  # turn left
				self.direction = -1, 0
				self.turns[self.head.pos[:]] = self.direction

			if keys[pygame.K_RIGHT] and self.direction != (-1, 0):  # turn right
				self.direction = 1, 0
				self.turns[self.head.pos[:]] = self.direction

			if keys[pygame.K_UP] and self.direction != (0, 1):  # turn up
				self.direction = 0, -1
				self.turns[self.head.pos[:]] = self.direction

			if keys[pygame.K_DOWN] and self.direction != (0, -1):  # turn down
				self.direction = 0, 1
				self.turns[self.head.pos[:]] = self.direction

		if self.number == num_2:
			if keys[pygame.K_a] and self.direction != (1, 0):  # turn left
				self.direction = -1, 0
				self.turns[self.head.pos[:]] = self.direction

			if keys[pygame.K_d] and self.direction != (-1, 0):  # turn right
				self.direction = 1, 0
				self.turns[self.head.pos[:]] = self.direction

			if keys[pygame.K_w] and self.direction != (0, 1):  # turn up
				self.direction = 0, -1
				self.turns[self.head.pos[:]] = self.direction

			if keys[pygame.K_s] and self.direction != (0, -1):  # turn down
				self.direction = 0, 1
				self.turns[self.head.pos[:]] = self.direction

		for index, head in enumerate(self.body):
			head_pos = head.pos[:]
			if head_pos in self.turns:
				turn = self.turns[head_pos]
				head.move((turn[0], turn[1]))
				if index == len(self.body) - 1:
					self.turns.pop(head_pos)
			else:
				if walls:  # end game if goes into the wall
					head.move(head.direction)
					if head.direction[0] == -1 and head.pos[0] < 0:  # left to right
						end_screen()

					if head.direction[0] == 1 and head.pos[0] >= ROWS:  # right to left
						end_screen()

					if head.direction[1] == 1 and head.pos[1] >= COLUMNS:  # bottom to top
						end_screen()

					if head.direction[1] == -1 and head.pos[1] < 0:  # top to bottom
						end_screen()

				else:  # move player to other screen size
					if head.direction[0] == -1 and head.pos[0] <= 0:  # left to right
						head.pos = (ROWS - 1, head.pos[1])

					elif head.direction[0] == 1 and head.pos[0] >= ROWS - 1:  # right to left
						head.pos = (0, head.pos[1])

					elif head.direction[1] == 1 and head.pos[1] >= COLUMNS - 1:  # bottom to top
						head.pos = (head.pos[0], 0)

					elif head.direction[1] == -1 and head.pos[1] <= 0:  # top to bottom
						head.pos = (head.pos[0], COLUMNS - 1)

					else:
						head.move(head.direction)

	def add_cube(self) -> None:
		tail = self.body[-1]
		if tail.direction == (1, 0):
			self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]), self.color))
		elif tail.direction == (-1, 0):
			self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), self.color))
		elif tail.direction == (0, 1):
			self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), self.color))
		elif tail.direction == (0, -1):
			self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), self.color))

		self.body[-1].direction = tail.direction

	def remove_cube(self) -> None:
		self.body.pop(-1)

	def draw(self) -> None:
		for index, head in enumerate(self.body):
			if index == 0:
				head.draw(eyes=True)
			else:
				head.draw()


class Snack:

	def __init__(self, texture) -> None:
		self.texture = texture
		self.randomize()

	def draw_snack(self) -> None:
		snack_rect = pygame.Rect(self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
		WINDOW.blit(self.texture, snack_rect)

	def randomize(self) -> None:
		self.pos = (randrange(ROWS), randrange(COLUMNS))


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
	quit()


def main() -> None:
	FPS = 10
	run = True
	clock = pygame.time.Clock()
	snake_one = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), PURPLE)
	snakes = [snake_one]

	if multiplayer:
		snake_two = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), BLUE, 2)
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
		pygame.time.delay(10)

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
				snake.remove_cube()
				poison = Snack(poison_texture)
				collision_check(snakes, poison)

			for i in range(len(snake.body)):
				if snake.body[i].pos in list(map(lambda z: z.pos, snake.body[i + 1:])):
					run = False
		redraw_window()


set_font = lambda size: pygame.font.Font(FONT, size)  # sets font size


def main_menu() -> None:
	text = set_font(20).render("QUIT", 1, GRAY)
	while True:
		WINDOW.fill(BLACK)
		title_label = set_font(50).render("Press any key to start...", 1, WHITE)
		WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, WINDOW_HEIGHT / 2 - title_label.get_height() / 2))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				main()
		pygame.display.update()


if __name__ == '__main__':
	main_menu()
