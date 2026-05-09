# =========================================
#        ULTIMATE CAR RACING GAME
# =========================================
# INSTALL:
# pip install pygame
#
# RUN:
# python racing_game.py
#
# CONTROLS:
# LEFT / RIGHT  -> Move
# UP            -> Nitro Boost
# R             -> Restart Game
# =========================================

import pygame
import random
import math

pygame.init()

# ---------------- WINDOW ----------------
WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ULTIMATE RACER")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 70, 70)
BLUE = (70, 170, 255)
GREEN = (0, 255, 120)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (180, 0, 255)
ROAD = (55, 55, 55)

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Arial", 30, bold=True)
big_font = pygame.font.SysFont("Arial", 70, bold=True)

# ---------------- ROAD ----------------
road_x = 200
road_width = 600

# ---------------- PLAYER ----------------
player_width = 70
player_height = 130

# ---------------- GAME VARIABLES ----------------
line_y = 0
spawn_timer = 0
screen_shake = 0

# ---------------- LISTS ----------------
enemies = []
particles = []

# =========================================
# RESET GAME FUNCTION
# =========================================

def reset_game():
    global player_x, player_y
    global speed, score, game_over

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 170

    speed = 10
    score = 0

    enemies.clear()
    particles.clear()

    game_over = False

reset_game()

# =========================================
# GLOW RECT
# =========================================

def draw_glow_rect(surface, color, rect, glow=20):

    x, y, w, h = rect

    for i in range(glow, 0, -4):

        glow_surface = pygame.Surface(
            (w + i*2, h + i*2),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (*color, 10),
            (0, 0, w + i*2, h + i*2),
            border_radius=18
        )

        surface.blit(glow_surface, (x - i, y - i))

    pygame.draw.rect(surface, color, rect, border_radius=15)

# =========================================
# PLAYER
# =========================================

def draw_player():

    # car body
    draw_glow_rect(
        screen,
        CYAN,
        (player_x, player_y, player_width, player_height),
        30
    )

    # windows
    pygame.draw.rect(
        screen,
        BLACK,
        (player_x + 12, player_y + 15, 46, 40),
        border_radius=10
    )

    # headlights
    pygame.draw.circle(screen, YELLOW, (player_x + 15, player_y + 110), 6)
    pygame.draw.circle(screen, YELLOW, (player_x + 55, player_y + 110), 6)

# =========================================
# ENEMY
# =========================================

def create_enemy():

    lane = random.choice([260, 420, 580, 700])

    enemy = {
        "x": lane,
        "y": -150,
        "speed": random.randint(8, 16),
        "color": random.choice([RED, GREEN, PURPLE, BLUE])
    }

    enemies.append(enemy)

def draw_enemy(enemy):

    draw_glow_rect(
        screen,
        enemy["color"],
        (enemy["x"], enemy["y"], player_width, player_height),
        20
    )

# =========================================
# PARTICLES
# =========================================

def create_particles():

    for i in range(4):

        particles.append({
            "x": player_x + player_width // 2,
            "y": player_y + player_height,
            "vx": random.uniform(-2, 2),
            "vy": random.uniform(3, 8),
            "life": random.randint(20, 40),
            "size": random.randint(3, 7),
            "color": random.choice([RED, YELLOW, CYAN])
        })

def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= 1

        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )

        if particle["life"] <= 0:
            particles.remove(particle)

# =========================================
# ROAD
# =========================================

def draw_road():

    global line_y

    pygame.draw.rect(
        screen,
        ROAD,
        (road_x, 0, road_width, HEIGHT)
    )

    # side glow
    pygame.draw.rect(screen, (100,100,100), (road_x-5, 0, 5, HEIGHT))
    pygame.draw.rect(screen, (100,100,100), (road_x+road_width, 0, 5, HEIGHT))

    line_y += speed

    if line_y >= 100:
        line_y = 0

    for i in range(-1, 10):

        pygame.draw.rect(
            screen,
            WHITE,
            (WIDTH//2 - 7, i * 100 + line_y, 14, 60),
            border_radius=10
        )

# =========================================
# COLLISION
# =========================================

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# =========================================
# MAIN LOOP
# =========================================

while True:

    clock.tick(60)

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()

    # =====================================
    # GAME RUNNING
    # =====================================

    if not game_over:

        # movement
        if keys[pygame.K_LEFT]:
            player_x -= 9

        if keys[pygame.K_RIGHT]:
            player_x += 9

        # nitro
        nitro = False

        if keys[pygame.K_UP]:
            speed = 18
            nitro = True
        else:
            speed = 10

        # boundaries
        if player_x < road_x + 20:
            player_x = road_x + 20

        if player_x > road_x + road_width - player_width - 20:
            player_x = road_x + road_width - player_width - 20

        # background
        screen.fill((10, 10, 20))

        # stars
        for i in range(40):
            pygame.draw.circle(
                screen,
                WHITE,
                (
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT)
                ),
                1
            )

        draw_road()

        # enemy spawning
        spawn_timer += 1

        if spawn_timer > 25:
            create_enemy()
            spawn_timer = 0

        # player rect
        player_rect = pygame.Rect(
            player_x,
            player_y,
            player_width,
            player_height
        )

        # enemies
        for enemy in enemies[:]:

            enemy["y"] += enemy["speed"]

            draw_enemy(enemy)

            enemy_rect = pygame.Rect(
                enemy["x"],
                enemy["y"],
                player_width,
                player_height
            )

            # collision
            if check_collision(player_rect, enemy_rect):

                game_over = True
                screen_shake = 20

            # remove enemy
            if enemy["y"] > HEIGHT:

                enemies.remove(enemy)
                score += 1

        # particles
        create_particles()
        update_particles()

        # player
        draw_player()

        # nitro overlay
        if nitro:

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 255, 255, 20))
            screen.blit(overlay, (0, 0))

        # UI
        score_text = font.render(f"Score : {score}", True, WHITE)
        speed_text = font.render(f"Speed : {speed}", True, CYAN)

        screen.blit(score_text, (20, 20))
        screen.blit(speed_text, (20, 60))

    # =====================================
    # GAME OVER
    # =====================================

    else:

        screen.fill(BLACK)

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        score_text = font.render(
            f"FINAL SCORE : {score}",
            True,
            WHITE
        )

        restart_text = font.render(
            "PRESS R TO RESTART",
            True,
            CYAN
        )

        screen.blit(
            game_over_text,
            (
                WIDTH//2 - game_over_text.get_width()//2,
                240
            )
        )

        screen.blit(
            score_text,
            (
                WIDTH//2 - score_text.get_width()//2,
                350
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH//2 - restart_text.get_width()//2,
                430
            )
        )

        # restart
        if keys[pygame.K_r]:
            reset_game()

    # update
    pygame.display.update()