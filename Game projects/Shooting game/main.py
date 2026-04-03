import pygame
import random

pygame.init()

# Assets
player_img = pygame.image.load("Assets/Playership1.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("Assets/Enemyship.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bullet_img = pygame.image.load("Assets/Bullet1.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Function to reset the game
def reset_game():
    global player_x, bullets, enemies, score, player_health, game_over

    player_x = WIDTH // 2
    bullets = []

    enemies = []
    for i in range(5):
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-600, 0)
        enemies.append([x, y])

    score = 0
    player_health = 5
    game_over = False

# Score settings
score = 0
font = pygame.font.SysFont(None, 36)

# Health settings
player_health = 5
max_health = 5
game_over = False

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 0.5

# Bullet settings
bullets = []
bullet_speed = 1

# Enemy settings
enemy_width = 40
enemy_height = 40
enemy_speed = 0.1

# Create multiple enemies
enemies = []
num_enemies = 4

reset_game()  # Initialize the game state

for _ in range(num_enemies):
    enemy_x = random.randint(0, WIDTH - enemy_width)
    enemy_y = random.randint(-150, -40)
    enemies.append([enemy_x, enemy_y])

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

            # RESTART GAME
            if event.key == pygame.K_r and game_over:
                reset_game()
    if not game_over:
        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        
        # Keep player within screen
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

        # Enemy Movement
        for enemy in enemies:
            enemy[1] += enemy_speed

            # Collision with player
            if (enemy[0] < player_x + player_width and
                enemy[0] + enemy_width > player_x and
                enemy[1] < player_y + player_height and
                enemy[1] + enemy_height > player_y):

                player_health -= 1

                # Reset enemy after hit
                enemy[1] = random.randint(-200, 0)
                enemy[0] = random.randint(0, WIDTH - enemy_width)

                if player_health <= 0:
                    game_over = True

            # Respawn enemy if it goes off screen
            if enemy[1] > HEIGHT:
                enemy[1] = random.randint(-200, 0)
                enemy[0] = random.randint(0, WIDTH - enemy_width)
            
        # Move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
            # Collision check
            for enemy in enemies:
                if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_width and
                    bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_height):

                    if bullet in bullets:
                        bullets.remove(bullet)

                    enemy[1] = random.randint(-200, 0)
                    enemy[0] = random.randint(0, WIDTH - enemy_width)

                    score += 1
                    break

        # Draw player
        screen.blit(player_img, (player_x, player_y))

        # Draw enemy
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))
        
        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 50, 200, 20))
        health_width = (player_health / max_health) * 200
        pygame.draw.rect(screen, (0, 255, 0), (10, 50, health_width, 20))

        # Score / Game Over
        if not game_over:
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
        else:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press R to Restart", True, (255, 255, 255))

            screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2 - 20))
            screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 20))
        
        pygame.display.update()


pygame.quit()