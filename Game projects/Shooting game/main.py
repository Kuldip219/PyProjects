import pygame

pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5

# Game loop
running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Black background
    pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_width, player_height))
    pygame.display.update()

pygame.quit()