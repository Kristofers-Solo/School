import pygame
from globals import *
from random import randrange


class Cube:

	def __init__(self, position, color=PURPLE) -> None:
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

	def __init__(self, position: tuple, color: tuple, name: str, player_number: int = 1, multiplayer: bool = False) -> None:
		self.color = color
		self.head = Cube(position, self.color)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.direction = (1, 0)
		self.number = player_number
		self.name = name
		self.multiplayer = multiplayer

	def move(self) -> None:
		keys = pygame.key.get_pressed()
		if self.multiplayer:
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
				from assets.scripts.menu import walls
				if walls:  # end game if goes into the wall
					from snake import end_screen
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


class Button():

	def __init__(self, position, text, font_size, base_color, hover_color) -> None:
		self.pos = position
		self.font = set_font(font_size)
		self.base_color = base_color
		self.hover_color = hover_color
		self.text = text
		self.text_rect = self.font.render(self.text, 1, self.base_color).get_rect(center=(self.pos))

	def update(self) -> None:
		WINDOW.blit(self.text, self.text_rect)

	def check_input(self, mouse_pos) -> bool:
		if mouse_pos[0] in range(self.text_rect.left, self.text_rect.right) and mouse_pos[1] in range(self.text_rect.top, self.text_rect.bottom):
			return True
		return False

	def change_color(self, mouse_pos) -> None:
		if mouse_pos[0] in range(self.text_rect.left,
		                         self.text_rect.right) and mouse_pos[1] in range(self.text_rect.top, self.text_rect.bottom):  # on hover
			self.text = self.font.render(self.text, 1, self.hover_color)
		else:
			self.text = self.font.render(self.text, 1, self.base_color)