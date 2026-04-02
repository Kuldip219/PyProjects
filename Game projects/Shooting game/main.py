import pygame

pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 1

# Bullet settings
bullets = []
bullet_speed = 1

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width
        
    # Draw player
    pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_width, player_height))
    
    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], 5, 10))
    
    pygame.display.update()


pygame.quit()