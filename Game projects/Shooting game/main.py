import pygame
import random
pygame.init()

font = pygame.font.Font("Fonts/pixeltype.ttf", 36)
big_font = pygame.font.Font("Fonts/pixeltype.ttf", 72)

# Screen settings
WIDTH = 480
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# == Assets == #
player_img = pygame.image.load("Assets/Playership1.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("Assets/Enemyship.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bullet_img = pygame.image.load("Assets/Bullet1.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

health_images = [
    pygame.image.load("Assets/Health_0.png"),
    pygame.image.load("Assets/Health_1.png"),
    pygame.image.load("Assets/Health_2.png"),
    pygame.image.load("Assets/Health_3.png"),
    pygame.image.load("Assets/Health_4.png"),
    pygame.image.load("Assets/Health_5.png")
]

# Resize health bar
health_images = [pygame.transform.scale(img, (200, 70)) for img in health_images]

title_img = pygame.image.load("Assets/title.png")
play_img = pygame.image.load("Assets/play.png")
options_img = pygame.image.load("Assets/options.png")
exit_img = pygame.image.load("Assets/exit.png")

title_img = pygame.transform.scale(title_img, (350, 120))
play_img = pygame.transform.scale(play_img, (250, 80))
options_img = pygame.transform.scale(options_img, (250, 80))
exit_img = pygame.transform.scale(exit_img, (250, 80))

# Game State
game_state = "menu"  

# Menu buttons
play_rect = play_img.get_rect(center=(WIDTH//2, 300))
options_rect = options_img.get_rect(center=(WIDTH//2, 400))
exit_rect = exit_img.get_rect(center=(WIDTH//2, 500))

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

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 80
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

# Health settings
player_health = 5
max_health = 5
game_over = False

# Score settings
score = 0

reset_game()  # Initialize the game state


# == Game loop == #

running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Menu events
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if play_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "game"

                elif options_rect.collidepoint(mouse_pos):
                    game_state = "options"

                elif exit_rect.collidepoint(mouse_pos):
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
                    player_health = 0
                    game_over = True

            # Respawn enemy if it goes off screen
            if enemy[1] > HEIGHT:
                enemy[1] = random.randint(-200, 0)
                enemy[0] = random.randint(0, WIDTH - enemy_width)
            
        # Move bullets
        for bullet in bullets[:]:
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
        screen.blit(health_images[player_health], (10, 50))

        # 🎮 SCORE (with shadow)
        if not game_over:
            score_main = font.render(f"Score: {score}", True, (255, 255, 0)) 
            score_shadow = font.render(f"Score: {score}", True, (0, 0, 0))

            screen.blit(score_shadow, (12, 12))
            screen.blit(score_main, (10, 10))

        # 💀 GAME OVER SCREEN
        else:
            game_over_text = big_font.render("GAME OVER", True, (255, 50, 50))
            restart_text = font.render("Press R to Restart", True, (255, 255, 255))

            # Center text
            go_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
            rs_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))

            # Shadows
            go_shadow = big_font.render("GAME OVER", True, (0, 0, 0))
            rs_shadow = font.render("Press R to Restart", True, (0, 0, 0))

            screen.blit(go_shadow, (go_rect.x + 3, go_rect.y + 3))
            screen.blit(rs_shadow, (rs_rect.x + 2, rs_rect.y + 2))

            # Main text
            screen.blit(game_over_text, go_rect)
            screen.blit(restart_text, rs_rect)
        
        pygame.display.update()


pygame.quit()