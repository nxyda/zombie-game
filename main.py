import pygame
import sys
import random
import math
import time

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

player_img = pygame.image.load("data/player.png")
player_img = pygame.transform.scale(player_img, (int(player_img.get_width() * 1.3), int(player_img.get_height() * 1.3)))

player_size = player_img.get_rect().size
player_width = player_size[0]
player_height = player_size[1]

zombie_img = pygame.image.load("data/zombie.png")
zombie_img = pygame.transform.scale(zombie_img, (int(zombie_img.get_width() * 1.3), int(zombie_img.get_height() * 1.3)))
zombie_size = zombie_img.get_rect().size
zombie_width = zombie_size[0]
zombie_height = zombie_size[1]

heart_img = pygame.image.load("data/heart.png")
heart_img = pygame.transform.scale(heart_img, (30, 30))

player_pos = [screen_width / 2 - player_width / 2, screen_height / 2 - player_height / 2]
player_speed = 5

bullet_size = 5
bullet_speed = 10
bullets = []

zombie_speed = 1
zombies = []

BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

font = pygame.font.Font(None, 36)

score = 0
lives = 3

last_shot_time = 0
shoot_delay = 0.5

def create_zombie():
    x_pos = random.choice([0, screen_width - zombie_width])
    y_pos = random.choice([0, screen_height - zombie_height])
    if x_pos == 0 or x_pos == screen_width - zombie_width:
        y_pos = random.randint(0, screen_height - zombie_height)
    else:
        x_pos = random.randint(0, screen_width - zombie_width)
    zombies.append([x_pos, y_pos])

def draw_player(screen, player_pos):
    screen.blit(player_img, (player_pos[0], player_pos[1]))

def draw_bullets(screen, bullets):
    for bullet in bullets:
        pygame.draw.circle(screen, RED, (int(bullet[0][0]), int(bullet[0][1])), bullet_size)

def draw_zombies(screen, zombies):
    for zombie in zombies:
        screen.blit(zombie_img, (zombie[0], zombie[1]))

def move_zombies(zombies, player_pos):
    for zombie in zombies:
        direction = (player_pos[0] - zombie[0], player_pos[1] - zombie[1])
        length = math.hypot(*direction)
        direction = (direction[0] / length, direction[1] / length)
        zombie[0] += direction[0] * zombie_speed
        zombie[1] += direction[1] * zombie_speed

def check_collision(bullets, zombies):
    global score
    for bullet in bullets:
        bullet_pos = bullet[0]
        for zombie in zombies:
            if (zombie[0] < bullet_pos[0] < zombie[0] + zombie_width and
                zombie[1] < bullet_pos[1] < zombie[1] + zombie_height):
                bullets.remove(bullet)
                zombies.remove(zombie)
                score += 1
                return True

def check_player_collision(zombies, player_pos):
    global lives
    for zombie in zombies:
        if (player_pos[0] < zombie[0] < player_pos[0] + player_width and
            player_pos[1] < zombie[1] < player_pos[1] + player_height):
            zombies.remove(zombie)
            lives -= 1
            if lives <= 0:
                return True
    return False

def draw_score(screen, score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def draw_lives(screen, lives):
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 40, 50))

def game_over_screen():
    screen.fill(DARK_GRAY)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))
    pygame.display.flip()

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(LIGHT_GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                current_time = time.time()
                if current_time - last_shot_time >= shoot_delay:
                    mouse_pos = pygame.mouse.get_pos()
                    bullet_pos = [player_pos[0] + player_width // 2, player_pos[1] + player_height // 2]
                    bullet_direction = (mouse_pos[0] - bullet_pos[0], mouse_pos[1] - bullet_pos[1])
                    bullet_length = math.hypot(*bullet_direction)
                    bullet_direction = (bullet_direction[0] / bullet_length, bullet_direction[1] / bullet_length)
                    bullets.append([bullet_pos, bullet_direction])
                    last_shot_time = current_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed

    for bullet in bullets[:]:
        bullet[0][0] += bullet[1][0] * bullet_speed
        bullet[0][1] += bullet[1][1] * bullet_speed
        if bullet[0][0] < 0 or bullet[0][0] > screen_width or bullet[0][1] < 0 or bullet[0][1] > screen_height:
            bullets.remove(bullet)

    if score <= 10:
        if random.randint(1,40) == 1:
            create_zombie()
    elif score > 10 and score <= 20:
        if random.randint(1,30) == 1:
            create_zombie()
    elif score > 20 and score <= 30:
        if random.randint(1,20) == 1:
            create_zombie()
    elif score > 30:
        if random.randint(1,10) == 1:
            create_zombie()

    move_zombies(zombies, player_pos)

    if check_player_collision(zombies, player_pos):
        game_over_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    score = 0
                    lives = 3
                    zombies = []
                    bullets = []
                    player_pos = [screen_width / 2 - player_width / 2, screen_height / 2 - player_height / 2]
                    break
            else:
                continue
            break

    check_collision(bullets, zombies)

    draw_player(screen, player_pos)
    draw_bullets(screen, bullets)
    draw_zombies(screen, zombies)
    draw_score(screen, score)
    draw_lives(screen, lives)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
