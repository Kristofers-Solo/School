import pygame
from globals import *
from assets.scripts.score import read_score, sort
from assets.scripts.classes import Button

MID_WIDTH = WIDTH / 2
MID_HEIGHT = WINDOW_HEIGHT / 2

user_name = ["", ""]
color_index = [0, 1]


def main_menu() -> None:
    pygame.display.set_caption("Snake - Menu")
    while True:
        WINDOW.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        menu_text = set_font(100).render("SNAKE GAME", 1, WHITE)
        menu_rect = menu_text.get_rect(center=(MID_WIDTH, 125))
        WINDOW.blit(menu_text, menu_rect)

        play_button = Button((MID_WIDTH, MID_HEIGHT - 50),
                             "PLAY", 75, GRAY, WHITE)
        options_button = Button(
            (MID_WIDTH, MID_HEIGHT + 50), "OPTIONS", 75, GRAY, WHITE)
        score_button = Button((MID_WIDTH, MID_HEIGHT + 150),
                              "SCORE", 75, GRAY, WHITE)
        quit_button = Button((MID_WIDTH, MID_HEIGHT + 250),
                             "QUIT", 75, GRAY, WHITE)
        buttons = [play_button, options_button, score_button, quit_button]

        on_hover(buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.check_input(mouse_pos):
                    user_input(0)
                if options_button.check_input(mouse_pos):
                    options()
                if score_button.check_input(mouse_pos):
                    scoreboard()
                if quit_button.check_input(mouse_pos):
                    quit()

        pygame.display.update()


def user_input(player: int) -> None:
    from snake import main
    global user_name
    global color_index
    pygame.display.set_caption("Snake")
    select_active = True
    outline_color = WHITE
    name_rect_w = 140
    while True:
        from globals import multiplayer
        WINDOW.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        menu_text = set_font(100).render(f"PLAYER {player + 1}", 1, WHITE)
        menu_rect = menu_text.get_rect(center=(MID_WIDTH, 125))
        WINDOW.blit(menu_text, menu_rect)

        back_button = Button((130, WINDOW_HEIGHT - 50),
                             "BACK", 75, GRAY, WHITE)
        if multiplayer and player == 0:
            next_button = Button(
                (WIDTH - 130, WINDOW_HEIGHT - 50), "NEXT", 75, GRAY, WHITE)
            buttons = [back_button, next_button]
        else:
            play_button = Button(
                (WIDTH - 130, WINDOW_HEIGHT - 50), "PLAY", 75, GRAY, WHITE)
            buttons = [back_button, play_button]

        on_hover(buttons)

        name_rect = pygame.Rect(
            MID_WIDTH - name_rect_w / 2, 200, name_rect_w, 32)
        pygame.draw.rect(WINDOW, outline_color, name_rect, 2)
        user_text = set_font(20).render(user_name[player], 1, WHITE)
        WINDOW.blit(user_text, (name_rect.x + 5, name_rect.y + 5))
        name_rect_w = max(140, user_text.get_width() + 10)

        color = COLORS[color_index[player]]
        color_rect = pygame.Rect(MID_WIDTH - 50, 350, 100, 100)
        pygame.draw.rect(WINDOW, color, color_rect)

        if select_active:
            outline_color = WHITE
        else:
            outline_color = DARK_GRAY

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if name_rect.collidepoint(event.pos):
                        select_active = True
                    else:
                        select_active = False

                    if back_button.check_input(mouse_pos):
                        main_menu()
                    if multiplayer and player == 0:
                        if next_button.check_input(mouse_pos):
                            user_input(1)
                    else:
                        if play_button.check_input(mouse_pos):
                            main()
                    if color_rect.collidepoint(event.pos):
                        color_index[player] += 1
                        if color_index[player] == len(COLORS) - 1:
                            color_index[player] = 0

                if event.button == 3:  # clear user name on mouse right click
                    if name_rect.collidepoint(event.pos):
                        user_name[player] = ""

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

                if select_active:
                    if event.key == pygame.K_BACKSPACE:
                        user_name[player] = user_name[player][:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        continue
                    else:
                        user_name[player] += event.unicode

                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if multiplayer and player == 0:
                        user_input(1)
                    else:
                        main()

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
        if multiplayer:
            multiplayer_state = "on"
        else:
            multiplayer_state = "off"
        # walls
        if walls:
            walls_state = "on"
        else:
            walls_state = "off"

        speed_state = {5: "Slow", 10: "Normal", 15: "Fast"}

        speed_button = Button((MID_WIDTH, MID_HEIGHT - 100),
                              f"SPEED - {speed_state[fps]}", 75, GRAY, WHITE)
        multiplayer_button = Button(
            (MID_WIDTH, MID_HEIGHT), f"MULTIPLAYER - {multiplayer_state}", 75, GRAY, WHITE)
        walls_button = Button((MID_WIDTH, MID_HEIGHT + 100),
                              f"WALLS - {walls_state}", 75, GRAY, WHITE)
        back_button = Button((MID_WIDTH, MID_HEIGHT + 200),
                             "BACK", 75, GRAY, WHITE)
        buttons = [speed_button, multiplayer_button, walls_button, back_button]

        on_hover(buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if speed_button.check_input(mouse_pos):
                    change_speed()
                if multiplayer_button.check_input(mouse_pos):
                    switch_multiplayer()
                if walls_button.check_input(mouse_pos):
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
        back_button = Button((MID_WIDTH, MID_HEIGHT + 250),
                             "BACK", 75, GRAY, WHITE)
        on_hover([back_button])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.check_input(mouse_pos):
                    main_menu()

        csv_file = read_score(BASE_PATH)
        for i, line in enumerate(sort(csv_file, reverse=True)[:11]):
            for j, text in enumerate(line):
                score_text = set_font(30).render(text, 1, WHITE)
                score_rect = score_text.get_rect(
                    center=(MID_WIDTH - 150 + 300 * j, 150 + 30 * i))
                WINDOW.blit(score_text, score_rect)

        pygame.display.update()


def on_hover(buttons: list) -> None:
    for button in buttons:
        button.change_color(pygame.mouse.get_pos())
        button.update()
