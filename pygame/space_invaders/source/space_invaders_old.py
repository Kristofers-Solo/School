# Author - Kristiāns Francis Cagulis
# Date - 25.02.2022
# Title - Space invaders

import pygame
import math
import random

BLUE = (16, 16, 69)

# init game
pygame.init()
pygame.display.set_caption("Space invaders")

# 32x32 game icon
icon = pygame.image.load("icons/space_invader_enemy_icon.png")
pygame.display.set_icon(icon)
# 64x64 player icon
player = pygame.image.load("icons/space_shuttle_player_icon.png")
player_x = 370
player_y = 480
player_x_change = 0

# 64x64 enemy icon
enemy = pygame.image.load("icons/space_invader_enemy_icon.png")
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_x_change = .2
enemy_y_change = 10


# missile
missile = pygame.image.load("icons/fireball_icon.png")
missile_x = 0
missile_y = 480  # player_y
missile_x_change = 0
missile_y_change = .50
missile_state = "ready"

screen = pygame.display.set_mode((800, 600))


def display_player(x, y):
	screen.blit(player, (x, y))


def display_enemy(x, y):
	screen.blit(enemy, (x, y))


def display_missile(x, y):
	global missile_state
	missile_state = "fire"
	screen.blit(missile, (x + 16, y - 10))


def is_collision(enemy_x, enemy_y, missile_x, missile_y):
	distance = math.sqrt(math.pow(enemy_x - missile_x, 2) + math.pow(enemy_y - missile_y, 2))
	if distance < 27:
		return True
	else:
		return False


running = True

while running:
	screen.fill(BLUE)

	# change player pos
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player_x_change = -.5
			if event.key == pygame.K_RIGHT:
				player_x_change = .5
			if event.key == pygame.K_SPACE:
				if missile_state == "ready":
					missile_x = player_x
					# missile_state = "fire"
					display_missile(missile_x, missile_y)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				player_x_change = 0

	# player pos
	if player_x + player_x_change > 0 and player_x + player_x_change < 736:
		player_x += player_x_change

	enemy_x += enemy_x_change
	enemy_y += enemy_y_change

	# enemy pos
	if enemy_x >= 736:
		enemy_x_change = -.2
	elif enemy_x <= 0:
		enemy_x_change = .2
	if enemy_y >= 336:
		enemy_y_change = -.1
	elif enemy_y <= 50:
		enemy_y_change = .1

	collision = is_collision(enemy_x, enemy_y, missile_x, missile_y)
	if collision:
		missile_y = 480
		missile_state = "ready"
		# score ...

	display_enemy(enemy_x, enemy_y)

	if missile_y <= 0:
		missile_state = "ready"
	if missile_state == "fire":
		display_missile(missile_x, missile_y)
		missile_y -= missile_y_change

	display_player(player_x, player_y)
	pygame.display.update()
