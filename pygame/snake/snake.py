# Author - Kristiāns Francis Cagulis
# Date - 11.03.2022
# Title - Snake

from random import randrange, randint
import pygame
import tkinter as tk
from tkinter import messagebox

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 30)
PURPLE = (170, 0, 255)
RANDOM_COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))

WIDTH = 500
ROWS = 20


class Cube(object):
	width = WIDTH
	rows = ROWS

	def __init__(self, start, color=RANDOM_COLOR):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	# eyes
	def draw(self, surface, eyes=False):
		distance = self.width // self.rows
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
	body = []
	turns = {}

	def __init__(self, color, pos):
		self.color = color
		self.head = Cube(pos, self.color)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1

	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			keys = pygame.key.get_pressed()

			for _ in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body) - 1:
					self.turns.pop(p)

			else:
				if c.dirnx == -1 and c.pos[0] <= 0:
					c.pos = (c.rows - 1, c.pos[1])

				elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
					c.pos = (0, c.pos[1])

				elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
					c.pos = (c.pos[0], 0)

				elif c.dirny == -1 and c.pos[1] <= 0:
					c.pos = (c.pos[0], c.rows - 1)

				else:
					c.move(c.dirnx, c.dirny)

	def reset(self, pos):
		self.head = Cube(pos)
		self.body = []
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def add_cube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny

		if dx == 1 and dy == 0:
			self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
		elif dx == -1 and dy == 0:
			self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
		elif dx == 0 and dy == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
		elif dx == 0 and dy == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy

	def draw(self, surface):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)

			else:
				c.draw(surface)


def draw_grid(width, rows, surface):
	size_between = width // rows
	x = 0
	y = 0
	for _ in range(rows):
		x += size_between
		y += size_between

		pygame.draw.line(surface, WHITE, (x, 0), (x, width))
		pygame.draw.line(surface, WHITE, (0, y), (width, y))


def redraw_window(surface):
	surface.fill(BLACK)
	s.draw(surface)
	snack.draw(surface)
	draw_grid(WIDTH, ROWS, surface)
	pygame.display.update()


def random_snack(rows, item):
	positions = item.body
	while True:
		x = randrange(rows)
		y = randrange(rows)
		if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
			continue
		else:
			break
	return x, y


def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass


def main():
	win = pygame.display.set_mode((WIDTH, WIDTH))
	flag = True
	clock = pygame.time.Clock()
	global snack
	snack = Cube(random_snack(ROWS, s), color=RED)
	while flag:
		pygame.time.delay(50)
		clock.tick(10)
		s.move()
		if s.body[0].pos == snack.pos:
			s.add_cube()
			snack = Cube(random_snack(ROWS, s), color=RED)

		for i in range(len(s.body)):
			if s.body[i].pos in list(map(lambda z: z.pos, s.body[i + 1:])):
				print(f"Score: {len(s.body)}")
				message_box("You Lost!", f"Your score was {len(s.body)}.\nPlay again")
				s.reset((10, 10))
				break
		redraw_window(win)

	pass


s = Snake(PURPLE, (10, 10))

if __name__ == '__main__':
	main()
