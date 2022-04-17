import pygame
from globals import *
from assets.scripts.score import read_score, sort
from assets.scripts.classes import Button

MID_WIDTH = WIDTH / 2
MID_HEIGHT = WINDOW_HEIGHT / 2


def menu() -> None:
	while True:
		WINDOW.fill(BLACK)
		title_label = set_font(50).render("Press any key to start...", 1, WHITE)
		WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, WINDOW_HEIGHT / 2 - title_label.get_height() / 2))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				csv_file = read_score(BASE_PATH)
				for line in sort(csv_file, reverse=True):
					print(line)
				quit()
			if event.type == pygame.KEYDOWN:
				from snake import main
				main()
		pygame.display.update()


def main_menu() -> None:
	global run
	run = True
	pygame.display.set_caption("Snake - Menu")
	while True:
		print(run)
		WINDOW.fill(BLACK)
		mouse_pos = pygame.mouse.get_pos()
		menu_text = set_font(100).render("SNAKE GAME", 1, WHITE)
		menu_rect = menu_text.get_rect(center=(MID_WIDTH, 125))
		WINDOW.blit(menu_text, menu_rect)

		play_button = Button((MID_WIDTH, MID_HEIGHT - 50), "PLAY", 75, GRAY, WHITE)
		options_button = Button((MID_WIDTH, MID_HEIGHT + 50), "OPTIONS", 75, GRAY, WHITE)
		quit_button = Button((MID_WIDTH, MID_HEIGHT + 150), "QUIT", 75, GRAY, WHITE)
		buttons = [play_button, options_button, quit_button]

		for button in buttons:
			button.change_color(mouse_pos)
			button.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if play_button.check_input(mouse_pos):
					from snake import main
					main()
				if options_button.check_input(mouse_pos):
					options()
				if quit_button.check_input(mouse_pos):
					quit()

		pygame.display.update()


def options() -> None:
	global FPS
	global multiplayer
	global walls
	pygame.display.set_caption("Snake - Options")
	while True:
		mouse_pos = pygame.mouse.get_pos()

		WINDOW.fill(BLACK)
		options_text = set_font(100).render("OPTIONS", 1, WHITE)
		options_rect = options_text.get_rect(center=(MID_WIDTH, 125))
		WINDOW.blit(options_text, options_rect)

		# change state names
		# multiplayer
		if multiplayer: multiplayer_state = "on"
		else: multiplayer_state = "off"
		# walls
		if walls: walls_state = "on"
		else: walls_state = "off"
		# speed
		if FPS == 5: speed_state = "Slow"
		elif FPS == 10: speed_state = "Normal"
		elif FPS == 15: speed_state = "Fast"

		speed_button = Button((MID_WIDTH, MID_HEIGHT - 100), f"SPEED - {speed_state}", 75, GRAY, WHITE)
		multiplayer_button = Button((MID_WIDTH, MID_HEIGHT), f"MULTIPLAYER - {multiplayer_state}", 75, GRAY, WHITE)
		walls_button = Button((MID_WIDTH, MID_HEIGHT + 100), f"WALLS - {walls_state}", 75, GRAY, WHITE)
		back_button = Button((MID_WIDTH, MID_HEIGHT + 200), "BACK", 75, GRAY, WHITE)
		buttons = [speed_button, multiplayer_button, walls_button, back_button]

		for button in buttons:
			button.change_color(mouse_pos)
			button.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if speed_button.check_input(mouse_pos):
					if FPS == 5: FPS = 10
					elif FPS == 10: FPS = 15
					elif FPS == 15: FPS = 5
				if multiplayer_button.check_input(mouse_pos):
					multiplayer = not multiplayer
				if walls_button.check_input(mouse_pos):
					walls = not walls
				if back_button.check_input(mouse_pos):
					main_menu()

		pygame.display.update()
