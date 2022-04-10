# Author - Kristiāns Francis Cagulis
# Date - 10.04.2022
# Title - Snake

import pygame
from random import randrange, randint

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 30)
PURPLE = (170, 0, 255)
BLUE = (85, 85, 255)
RANDOM_COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))

SQUARE_SIZE = 30
ROWS, COLUMNS = 30, 20
WIDTH, HEIGHT = ROWS * SQUARE_SIZE, COLUMNS * SQUARE_SIZE

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()

multiplayer = False


class Cube(object):

	def __init__(self, start_pos, color=RANDOM_COLOR) -> None:
		self.pos = start_pos
		self.direction = (1, 0)
		self.color = color

	def move(self, direction: tuple) -> None:
		self.direction = direction
		self.pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])

	def draw(self, surface, eyes=False) -> None:
		distance = WIDTH // ROWS
		i, j = self.pos

		pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))
		if eyes:
			center = distance // 2
			radius = 3
			circle_middle = (i * distance + center - radius, j * distance + 8)
			circle_middle_2 = (i * distance + distance - radius * 2, j * distance + 8)
			pygame.draw.circle(surface, BLACK, circle_middle, radius)
			pygame.draw.circle(surface, BLACK, circle_middle_2, radius)


class Snake(object):

	def __init__(self, pos: tuple, color: tuple, player_number: int = 1) -> None:
		self.color = color
		self.head = Cube(pos, self.color)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.direction = (1, 0)
		self.number = player_number

	def move(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()

			if multiplayer:
				num_1, num_2 = 1, 2
			else:
				num_1, num_2 = 1, 1

			if self.number == num_1:
				if keys[pygame.K_LEFT] and self.direction != (1, 0):  # turn left
					self.direction = -1, 0

				if keys[pygame.K_RIGHT] and self.direction != (-1, 0):  # turn right
					self.direction = 1, 0

				if keys[pygame.K_UP] and self.direction != (0, 1):  # turn up
					self.direction = 0, -1

				if keys[pygame.K_DOWN] and self.direction != (0, -1):  # turn down
					self.direction = 0, 1

			if self.number == num_2:
				if keys[pygame.K_a] and self.direction != (1, 0):  # turn left
					self.direction = -1, 0

				if keys[pygame.K_d] and self.direction != (-1, 0):  # turn right
					self.direction = 1, 0

				if keys[pygame.K_w] and self.direction != (0, 1):  # turn up
					self.direction = 0, -1

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

	# def reset(self, pos) -> None:
	# 	self.head = Cube(pos, self.color)
	# 	self.body = []
	# 	self.turns = {}
	# 	self.direction = randint(-1, 1), randint(-1, 1)

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

	def draw(self, surface) -> None:
		for index, head in enumerate(self.body):
			if index == 0:
				head.draw(surface, eyes=True)
			else:
				head.draw(surface)


def draw_grid(surface) -> None:
	size_between = WIDTH // ROWS
	x, y = 0, 0
	for _ in range(ROWS):
		x += size_between
		y += size_between

		pygame.draw.line(surface, WHITE, (x, 0), (x, HEIGHT))
		pygame.draw.line(surface, WHITE, (0, y), (WIDTH, y))


def redraw_window(sprites: list) -> None:
	WINDOW.fill(BLACK)
	draw_grid(WINDOW)
	for sprite in sprites:
		sprite.draw(WINDOW)
	pygame.display.update()


def random_snack(items, rows=ROWS, columns=COLUMNS) -> tuple:
	for item in items:
		positions = item.body
		while True:
			x = randrange(rows)
			y = randrange(columns)
			if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
				continue
			else:
				break
	return x, y


def main() -> None:
	FPS = 10
	run = True
	clock = pygame.time.Clock()
	snake_one = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), PURPLE)
	snakes = [snake_one]

	if multiplayer:
		snake_two = Snake((randint(0, ROWS - 1), randint(0, COLUMNS - 1)), BLUE, 2)
		snakes.append(snake_two)

	snack = Cube(random_snack(snakes), color=GREEN)
	poison = Cube(random_snack(snakes), color=RED)
	while run:
		clock.tick(FPS)
		pygame.time.delay(50)
		for snake in snakes:
			snake.move()
			if snake.body[0].pos == snack.pos:
				snake.add_cube()
				snack = Cube(random_snack(snakes), color=GREEN)
			if snake.body[0].pos == poison.pos:
				snake.remove_cube()
				poison = Cube(random_snack(snakes), color=RED)
			for i in range(len(snake.body)):
				if snake.body[i].pos in list(map(lambda z: z.pos, snake.body[i + 1:])):
					print(f"Score: {len(snake.body)}")
					run = False
		redraw_window(list(set(snakes + [snack, poison])))


set_font = lambda size: pygame.font.SysFont("roboto", size)  # sets font size


def main_menu() -> None:
	while True:
		WINDOW.fill(BLACK)
		title_label = set_font(50).render("Press any key to start...", 1, WHITE)
		WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height() / 2))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				main()


if __name__ == '__main__':
	main_menu()
