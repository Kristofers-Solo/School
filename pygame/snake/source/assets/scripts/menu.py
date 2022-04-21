import pygame
from globals import *
from assets.scripts.score import read_score, sort
from assets.scripts.classes import Button

MID_WIDTH = WIDTH / 2
MID_HEIGHT = WINDOW_HEIGHT / 2


def main_menu() -> None:
	pygame.display.set_caption("Snake - Menu")
	while True:
		WINDOW.fill(BLACK)
		mouse_pos = pygame.mouse.get_pos()
		menu_text = set_font(100).render("SNAKE GAME", 1, WHITE)
		menu_rect = menu_text.get_rect(center=(MID_WIDTH, 125))
		WINDOW.blit(menu_text, menu_rect)

		play_button = Button((MID_WIDTH, MID_HEIGHT - 50), "PLAY", 75, GRAY, WHITE)
		options_button = Button((MID_WIDTH, MID_HEIGHT + 50), "OPTIONS", 75, GRAY, WHITE)
		score_button = Button((MID_WIDTH, MID_HEIGHT + 150), "SCORE", 75, GRAY, WHITE)
		quit_button = Button((MID_WIDTH, MID_HEIGHT + 250), "QUIT", 75, GRAY, WHITE)
		buttons = [play_button, options_button, score_button, quit_button]

		on_hover(buttons)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if play_button.check_input(mouse_pos):
					from snake import main
					main()
				if options_button.check_input(mouse_pos):
					options()
				if score_button.check_input(mouse_pos):
					scoreboard()
				if quit_button.check_input(mouse_pos):
					quit()

		pygame.display.update()


def options() -> None:
	pygame.display.set_caption("Snake - Options")
	while True:
		from globals import fps, multiplayer, walls
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

		speed_state = {5: "Slow", 10: "Normal", 15: "Fast"}

		speed_button = Button((MID_WIDTH, MID_HEIGHT - 100), f"SPEED - {speed_state[fps]}", 75, GRAY, WHITE)
		multiplayer_button = Button((MID_WIDTH, MID_HEIGHT), f"MULTIPLAYER - {multiplayer_state}", 75, GRAY, WHITE)
		walls_button = Button((MID_WIDTH, MID_HEIGHT + 100), f"WALLS - {walls_state}", 75, GRAY, WHITE)
		back_button = Button((MID_WIDTH, MID_HEIGHT + 200), "BACK", 75, GRAY, WHITE)
		buttons = [speed_button, multiplayer_button, walls_button, back_button]

		on_hover(buttons)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if speed_button.check_input(mouse_pos):
					change_speed()
				if multiplayer_button.check_input(mouse_pos):
					multiplayer = not multiplayer  # switch
					switch_multiplayer()
				if walls_button.check_input(mouse_pos):
					# walls = not walls  # switch
					switch_walls()
				if back_button.check_input(mouse_pos):
					main_menu()

		pygame.display.update()


def scoreboard() -> None:
	while True:
		mouse_pos = pygame.mouse.get_pos()
		WINDOW.fill(BLACK)
		top_text = set_font(100).render("TOP 10", 1, WHITE)
		top_rect = top_text.get_rect(center=(MID_WIDTH, 55))
		WINDOW.blit(top_text, top_rect)
		back_button = Button((MID_WIDTH, MID_HEIGHT + 250), "BACK", 75, GRAY, WHITE)
		on_hover([back_button])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if back_button.check_input(mouse_pos):
					main_menu()

		csv_file = read_score(BASE_PATH)
		for i, line in enumerate(sort(csv_file, reverse=True)[:11]):
			for j, text in enumerate(line):
				score_text = set_font(30).render(text, 1, WHITE)
				score_rect = score_text.get_rect(center=(MID_WIDTH - 150 + 300 * j, 150 + 30 * i))
				WINDOW.blit(score_text, score_rect)

		pygame.display.update()


def on_hover(buttons: list) -> None:
	for button in buttons:
		button.change_color(pygame.mouse.get_pos())
		button.update()