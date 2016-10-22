import pygame
import random

pygame.init()
pygame.display.set_caption("FlapPyLadies")
screen = pygame.display.set_mode([700, 497])
clock = pygame.time.Clock()

font = pygame.font.Font('fonts/geo.ttf', 55)
img_player = pygame.image.load('img/player.png')
img_upper_wall = pygame.image.load('img/img_wallup.png')
img_lower_wall = pygame.image.load('img/img_walldown.png')
img_gameover = pygame.image.load('img/gameover.png')
img_bg = pygame.image.load('img/bg.jpg')
img_start = pygame.image.load('img/start.png')
img_logo = pygame.image.load('img/logoPython.png')
jump = pygame.mixer.Sound('sounds/jump.wav')
hit = pygame.mixer.Sound('sounds/explode.wav')
jump.set_volume(0.1)
hit.set_volume(0.1)


PLACEHOLDERS = False


def intro():
    screen.fill([255, 255, 255])
    screen.blit(img_logo, [40, 300])
    screen.blit(img_start, [170, 50])
    pygame.display.update()
    pygame.time.wait(2000)


def draw_player(player):
    if PLACEHOLDERS:
        pygame.draw.rect(screen, [255, 128, 128], player)
    else:
        screen.blit(img_player, player)


def draw_wall(upper_wall, lower_wall, wall_x, wall_height, wall_gap):
    if PLACEHOLDERS:
        pygame.draw.rect(screen, [128, 255, 128], upper_wall)
        pygame.draw.rect(screen, [128, 255, 128], lower_wall)
    else:
        screen.blit(img_upper_wall, [wall_x, wall_height - 500])
        screen.blit(img_lower_wall, [wall_x, wall_height + wall_gap])


def draw_score(score):
    if PLACEHOLDERS:
        text = font.render(str(score), True, [128, 128, 255])
    else:
        text = font.render(str(score), True, [255, 255, 255])
    screen.blit(text, [350, 20])


def game():
    player_x = 350
    player_y = 250
    player_speed = 0
    wall_x = 700
    wall_weight = 70
    wall_height = random.randint(0, 350)
    wall_speed = 4
    wall_gap = 150
    score = 0
    game_over = False
    background_size = 1320
    background_position = 0

    upper_border = 0
    lower_border = 450
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_speed = -5
                jump.play()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                player_speed = 5

            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                player_speed = -5
            if event.type == pygame.KEYUP and event.key == pygame.K_k:
                player_speed = 0
            if event.type == pygame.KEYUP and event.key == pygame.K_j:
                player_speed = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                player_speed = 5

        if PLACEHOLDERS:
            screen.fill([255, 255, 255])
        else:
            screen.blit(img_bg, [background_position, 0])
            screen.blit(img_bg, [background_position + background_size, 0])
            background_position -= 2
            if background_position * -1 == background_size:
                background_position = 0

        player = pygame.Rect(player_x, player_y, 45, 45)
        draw_player(player)
        player_y += player_speed

        upper_wall = pygame.Rect(wall_x, 0, wall_weight, wall_height)
        lower_wall = pygame.Rect(wall_x, (wall_height + wall_gap), wall_weight, wall_height + 500)
        draw_wall(upper_wall, lower_wall, wall_x, wall_height, wall_gap)
        wall_x -= wall_speed

        if wall_x < -wall_weight:
            wall_x = 700
            wall_height = random.randint(0, 350)

        draw_score(score)
        if player_x == wall_x + wall_weight:
            score += 1

        if (player_y > lower_border or player_y < upper_border or
                player.colliderect(upper_wall) or player.colliderect(lower_wall)):
            hit.play()
            player_speed = wall_speed = 0
            game_over = True

        pygame.display.flip()
        clock.tick(60)

        while game_over:
            pygame.time.wait(300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True

            screen.fill([255, 255, 255])
            screen.blit(img_gameover, (175, 20))
            font = pygame.font.Font('fonts/geo.ttf', 40)
            text = font.render(str(score), True, [238, 37, 79])
            screen.blit(text, [410, 43])
            pygame.display.flip()


intro()
while game():
    pass
pygame.quit()
