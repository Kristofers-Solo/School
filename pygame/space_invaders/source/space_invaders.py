# Author - Kristiāns Francis Cagulis
# Date - 06.03.2022
# Title - Space invaders
# TODO: Add enemy movement in groups

import pygame
from random import randint, randrange, choice
from os.path import abspath, dirname, join

WIDTH, HEIGHT = 800, 800

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
pygame.font.init()

# paths
BASE_PATH = abspath(dirname(__file__))
SPRITE_PATH = join(BASE_PATH, "assets", "sprites")
ENEMY_PATH = join(SPRITE_PATH, "enemies")
FONT = join(BASE_PATH, "fonts", "space_invaders.ttf")

# load sprites
SPACESHIP = pygame.image.load(join(SPRITE_PATH, "playership.png"))  # player
PLAYER_MISSILE = pygame.image.load(join(SPRITE_PATH, "missiles", "playermissile.png"))  # player missile

# enemies
ENEMY_1 = pygame.transform.scale(pygame.image.load(join(ENEMY_PATH, "enemy1", "enemy1_1.png")), (40, 35))
ENEMY_2 = pygame.transform.scale(pygame.image.load(join(ENEMY_PATH, "enemy2", "enemy2_1.png")), (40, 35))
ENEMY_3 = pygame.transform.scale(pygame.image.load(join(ENEMY_PATH, "enemy3", "enemy3_1.png")), (40, 35))
ENEMY_MISSILE = pygame.image.load(join(SPRITE_PATH, "missiles", "enemymissile.png"))  # enemy missile

# background
BACKGROUND = pygame.transform.scale(pygame.image.load(join(BASE_PATH, "assets", "background.jpg")), (WIDTH, HEIGHT))

# colors (R, G, B)
BLUE = (16, 16, 69)
WHITE = (255, 255, 255)
RED = (188, 2, 5)


class Missile:
	def __init__(self, x: int, y: int, img) -> None:
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self, window) -> None:
		window.blit(self.img, (self.x, self.y))

	def move(self, vel: int) -> None:
		self.y += vel

	def off_screen(self, height: int) -> bool:
		return not (self.y <= height and self.y >= 0)

	def collision(self, obj) -> bool:
		return collide(self, obj)


class Ship:
	COOLDOWN = 30

	def __init__(self, x: int, y: int, lives: int = 5) -> None:
		self.x = x
		self.y = y
		self.lives = lives
		self.ship_img = None
		self.missile_img = None
		self.missiles = []
		self.cooldown_counter = 0

	def draw(self, window) -> None:
		window.blit(self.ship_img, (self.x, self.y))
		for missile in self.missiles:
			missile.draw(WINDOW)

	def move_missiles(self, vel: int, obj) -> None:
		self.cooldown()
		for missile in self.missiles:
			missile.move(vel)
			if missile.off_screen(HEIGHT):
				self.missiles.remove(missile)
			elif missile.collision(obj):
				obj.lives -= 1
				self.missiles.remove(missile)

	def cooldown(self) -> None:
		if self.cooldown_counter >= self.COOLDOWN:
			self.cooldown_counter = 0
		elif self.cooldown_counter > 0:
			self.cooldown_counter += 1

	def shoot(self) -> None:
		if self.cooldown_counter == 0:
			missile = Missile(self.x + self.get_width() / 2 - 5 / 2, self.y, self.missile_img)  # missile spawn with offset
			self.missiles.append(missile)
			self.cooldown_counter = 1

	def get_width(self) -> int:
		return self.ship_img.get_width()

	def get_height(self) -> int:
		return self.ship_img.get_height()


class Player(Ship):
	def __init__(self, x: int, y: int, lives: int = 5) -> None:
		super().__init__(x, y, lives)
		self.ship_img = SPACESHIP
		self.missile_img = PLAYER_MISSILE
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_lives = lives
		self.score = 0

	def move_missiles(self, vel: int, objs: list) -> None:
		self.cooldown()
		for missile in self.missiles:
			missile.move(vel)
			if missile.off_screen(HEIGHT):
				self.missiles.remove(missile)
				self.score -= 10
			else:
				for obj in objs:
					if missile.collision(obj):
						objs.remove(obj)
						self.score += 50
						if missile in self.missiles:
							self.missiles.remove(missile)


class Enemy(Ship):
	COLOR_MAP = {
	    "magenta": ENEMY_1,
	    "cyan": ENEMY_2,
	    "lime": ENEMY_3,
	}

	def __init__(self, x: int, y: int, color: str) -> None:
		super().__init__(x, y)
		self.ship_img = self.COLOR_MAP[color]
		self.missile_img = ENEMY_MISSILE
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self, vel_x: int, vel_y: int) -> None:
		self.x += vel_x
		self.y += vel_y


class EnemiesGroup(Enemy):
	def __init__(self, rows: int, columns: int) -> None:
		super().__init__(rows, columns)


def main() -> None:
	run = True
	lost = False
	lost_count = 0
	FPS = 60
	level = 0

	enemies = []
	player_vel = 7
	player_missile_vel = 7
	enemy_x_vel = 2
	vel_y = 0
	vel_x = enemy_x_vel
	enemy_missile_vel = 4
	# velocities = [[5, 0], [0, 2], [-5, 0], [-5, 0], [0, 2], [5, 0]]
	# velocities = {"down": [0, 2], "right": [2, 0], "left": [-5, 0]}
	# directions = ["right", "down", "left", "left", "down", "right"]

	player = Player(WIDTH / 2, 650)

	clock = pygame.time.Clock()

	def redraw_window() -> None:
		WINDOW.blit(BACKGROUND, (0, 0))
		# draw text
		lives_label = set_font(40).render(f"Lives: {player.lives}", 1, WHITE)
		score_label = set_font(40).render(f"Score {player.score}", 1, WHITE)
		level_label = set_font(40).render(f"Level: {level}", 1, WHITE)
		WINDOW.blit(lives_label, (10, 10))
		WINDOW.blit(score_label, (10, lives_label.get_height() + 10))
		WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		for enemy in enemies:
			enemy.draw(WINDOW)

		player.draw(WINDOW)

		if lost:
			lost_label = set_font(60).render("You lost!", 1, RED)
			WINDOW.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

		pygame.display.update()

	while run:
		clock.tick(FPS)
		redraw_window()

		if player.lives <= 0:
			lost = True
			lost_count += 1

		# stop game
		if lost:
			if lost_count > FPS * 3:
				run = False
			else:
				continue

		if len(enemies) == 0:
			level += 1
			margin = 75
			width = 75
			for x in range(margin, WIDTH - margin, width):
				for y in range(margin, int(HEIGHT / 2), width):
					enemy = Enemy(x, y, choice(["magenta", "lime", "cyan"]))
					enemies.append(enemy)

		for event in pygame.event.get():
			# quit game
			if event.type == pygame.QUIT:
				quit()

		keys = pygame.key.get_pressed()

		# move left
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (player.x - player_vel > 0):
			player.x -= player_vel
		# move right
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (player.x + player_vel + player.get_width() < WIDTH):
			player.x += player_vel
		# shoot
		if keys[pygame.K_SPACE]:
			player.shoot()

		# enemies action

		# for _ in range(len(directions)):
		# 	if pygame.time.get_ticks() % 100 == 0:
		# 		for direction in directions:
		# 			vel_x, vel_y = velocities[direction]
		# 			for enemy in enemies[:]:
		# 				enemy.move(vel_x, vel_y)

		# if pygame.time.get_ticks() % 10 == 0:
		# 	for vel_x, vel_y in velocities:
		# 		for enemy in enemies[:]:
		# 			enemy.move(vel_x, vel_y)

		for enemy in enemies[:]:
			# enemy.move(0, enemy_y_vel)
			# enemy.move(randint(-enemy_x_vel, enemy_x_vel), randint(0, enemy_y_vel))
			if enemy.x >= WIDTH - enemy.get_width():
				vel_x = -enemy_x_vel
			elif enemy.x <= 0:
				vel_x = enemy_x_vel
			enemy.move(vel_x, vel_y)

			enemy.move_missiles(enemy_missile_vel, player)

			if randrange(0, 2 * FPS) == 1:
				# enemy.shoot()
				pass

			if collide(enemy, player) or (enemy.y + enemy.get_height() > HEIGHT):
				player.score -= 10
				player.lives -= 1
				enemies.remove(enemy)

		player.move_missiles(-player_missile_vel, enemies)


# lambda functions
set_font = lambda size, font=FONT: pygame.font.Font(font, size)  # sets font size
collide = lambda obj1, obj2: obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) != None  # checks if 2 objs collide/overlap


def main_menu() -> None:
	while True:
		WINDOW.blit(BACKGROUND, (0, 0))
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