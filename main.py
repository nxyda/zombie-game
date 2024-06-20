import pygame
import sys
import random
import math


pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


player_img = pygame.image.load("data/player.png")
player_size = player_img.get_rect().size
player_width = player_size[0]
player_height = player_size[1]

zombie_img = pygame.image.load("data/zombie.png")
zombie_size = zombie_img.get_rect().size
zombie_width = zombie_size[0]
zombie_height = zombie_size[1]


player_pos = [screen_width / 2 - player_width / 2, screen_height / 2 - player_height / 2]
player_speed = 5


bullet_size = 5
bullet_speed = 10
bullets = []


zombie_speed = 1
zombies = []

BLACK = (0, 0, 0)

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
        pygame.draw.circle(screen, (255, 0, 0), (int(bullet[0][0]), int(bullet[0][1])), bullet_size)

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
    for bullet in bullets:
        bullet_pos = bullet[0]
        for zombie in zombies:
            if (zombie[0] < bullet_pos[0] < zombie[0] + zombie_width and
                zombie[1] < bullet_pos[1] < zombie[1] + zombie_height):
                bullets.remove(bullet)
                zombies.remove(zombie)
                return True

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_pos = pygame.mouse.get_pos()
                bullet_pos = [player_pos[0] + player_width // 2, player_pos[1] + player_height // 2]
                bullet_direction = (mouse_pos[0] - bullet_pos[0], mouse_pos[1] - bullet_pos[1])
                bullet_length = math.hypot(*bullet_direction)
                bullet_direction = (bullet_direction[0] / bullet_length, bullet_direction[1] / bullet_length)
                bullets.append([bullet_pos, bullet_direction])

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

    if random.randint(1, 50) == 1:
        create_zombie()

    move_zombies(zombies, player_pos)

    check_collision(bullets, zombies)

    draw_player(screen, player_pos)
    draw_bullets(screen, bullets)
    draw_zombies(screen, zombies)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
