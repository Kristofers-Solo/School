# Author - Kristiāns Francis Cagulis
# Date - 28.03.2022
# Title - Snake

import pygame
from random import randrange, randint

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 30)
PURPLE = (170, 0, 255)
RANDOM_COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))

SQUARE_SIZE = 30
ROWS, COLUMNS = 30, 20
WIDTH, HEIGHT = ROWS * SQUARE_SIZE, COLUMNS * SQUARE_SIZE

RANDOM_POS = (randint(0, ROWS - 1), randint(0, COLUMNS - 1))

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


class Cube(object):
	def __init__(self, start, color=RANDOM_COLOR) -> None:
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny) -> None:
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	# eyes
	def draw(self, surface, eyes=False) -> None:
		distance = WIDTH // ROWS
		# print(distance)
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))
		if eyes:
			center = distance // 2
			radius = 3
			circle_middle = (i * distance + center - radius, j * distance + 8)
			circle_middle_2 = (i * distance + distance - radius * 2, j * distance + 8)
			pygame.draw.circle(surface, BLACK, circle_middle, radius)
			pygame.draw.circle(surface, BLACK, circle_middle_2, radius)


class Snake(object):
	def __init__(self, pos, color) -> None:
		self.color = color
		self.head = Cube(pos, self.color)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def move(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # turn left
				self.dirnx = -1
				self.dirny = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]  # turn right

			elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.dirnx = 1
				self.dirny = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			elif keys[pygame.K_UP] or keys[pygame.K_w]:  # turn up
				self.dirnx = 0
				self.dirny = -1
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # turn down
				self.dirnx = 0
				self.dirny = 1
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, head in enumerate(self.body):
			head_pos = head.pos[:]
			if head_pos in self.turns:
				turn = self.turns[head_pos]
				head.move(turn[0], turn[1])
				if i == len(self.body) - 1:
					self.turns.pop(head_pos)

			else:  # move player to other screen size
				if head.dirnx == -1 and head.pos[0] <= 0:  # left to right
					head.pos = (ROWS - 1, head.pos[1])

				elif head.dirnx == 1 and head.pos[0] >= ROWS - 1:  # right to left
					head.pos = (0, head.pos[1])

				elif head.dirny == 1 and head.pos[1] >= COLUMNS - 1:  # bottom to top
					head.pos = (head.pos[0], 0)

				elif head.dirny == -1 and head.pos[1] <= 0:  # top to bottom
					head.pos = (head.pos[0], COLUMNS - 1)

				else:
					head.move(head.dirnx, head.dirny)

	def reset(self, pos) -> None:
		self.head = Cube(pos, self.color)
		self.body = []
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def add_cube(self) -> None:
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]), self.color))
		elif dx == -1 and dy == 0:
			self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), self.color))
		elif dx == 0 and dy == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), self.color))
		elif dx == 0 and dy == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), self.color))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy

	def draw(self, surface) -> None:
		for i, head in enumerate(self.body):
			if i == 0:
				head.draw(surface, True)

			else:
				head.draw(surface)


def draw_grid(surface) -> None:
	size_between = WIDTH // ROWS
	x = 0
	y = 0
	for _ in range(ROWS):
		x += size_between
		y += size_between

		pygame.draw.line(surface, WHITE, (x, 0), (x, HEIGHT))
		pygame.draw.line(surface, WHITE, (0, y), (WIDTH, y))


def redraw_window(snake, snack) -> None:
	WINDOW.fill(BLACK)
	draw_grid(WINDOW)
	snake.draw(WINDOW)
	snack.draw(WINDOW)
	pygame.display.update()


def random_snack(rows, columns, item) -> tuple:
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
	snake = Snake(RANDOM_POS, PURPLE)
	snack = Cube(random_snack(ROWS, COLUMNS, snake), color=GREEN)
	while run:
		clock.tick(FPS)
		pygame.time.delay(50)
		snake.move()
		if snake.body[0].pos == snack.pos:
			snake.add_cube()
			snack = Cube(random_snack(ROWS, COLUMNS, snake), color=GREEN)
		for i in range(len(snake.body)):
			if snake.body[i].pos in list(map(lambda z: z.pos, snake.body[i + 1:])):
				print(f"Score: {len(snake.body)}")
				run = False
				# snake.reset(RANDOM_POS)
		redraw_window(snake, snack)


set_font = lambda size: pygame.font.SysFont("roboto", size)  # sets font size


def main_menu() -> None:
	while True:
		WINDOW.fill(BLACK)
		# title_label = set_font(50).render("Press any key to start...", 1, WHITE)
		title_label = pygame.font.SysFont("roboto", 50).render("Press any key to start...", 1, WHITE)
		WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height() / 2))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				main()


if __name__ == '__main__':
	main_menu()
