import pygame
from globals import *
from assets.scripts.score import read_score, sort


def main_menu() -> None:
	text = set_font(20).render("QUIT", 1, GRAY)
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
