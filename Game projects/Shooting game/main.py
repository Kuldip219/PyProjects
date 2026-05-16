import pygame
import random
pygame.init()

font = pygame.font.Font("Fonts/pixeltype.ttf", 36)
big_font = pygame.font.Font("Fonts/pixeltype.ttf", 72)

# Screen settings
WIDTH = 480
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("X Hunter")

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

explosion_frames = []

for i in range(1, 9):
    img = pygame.image.load(f"Assets/explosion_{i}.png")
    img = pygame.transform.scale(img, (70, 70))
    explosion_frames.append(img)

# Resize health bar
health_images = [pygame.transform.scale(img, (200, 70)) for img in health_images]

title_img = pygame.image.load("Assets/title.png")
play_img = pygame.image.load("Assets/play.png")
options_img = pygame.image.load("Assets/options.png")
exit_img = pygame.image.load("Assets/exit.png")
pause_img = pygame.image.load("Assets/menu.png")
continue_img = pygame.image.load("Assets/continue.png")
quit_img = pygame.image.load("Assets/quit.png")

title_img = pygame.transform.scale(title_img, (350, 120))
play_img = pygame.transform.scale(play_img, (250, 80))
options_img = pygame.transform.scale(options_img, (250, 80))
exit_img = pygame.transform.scale(exit_img, (250, 80))
pause_img = pygame.transform.scale(pause_img, (400, 100))
continue_img = pygame.transform.scale(continue_img, (250, 80))
quit_img = pygame.transform.scale(quit_img, (250, 72))

# Game State
game_state = "menu"  

# Menu buttons
play_rect = play_img.get_rect(center=(WIDTH//2, 300))
options_rect = options_img.get_rect(center=(WIDTH//2, 400))
exit_rect = exit_img.get_rect(center=(WIDTH//2, 500))
continue_rect = continue_img.get_rect(center=(WIDTH//2, 350))
quit_rect = quit_img.get_rect(center=(WIDTH//2, 450))
pause_rect = pause_img.get_rect(center=(WIDTH//2, 200))

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 0.5

# Bullet settings
bullets = []
bullet_speed = 1

# Explosion settings
explosions = []

# Enemy settings
enemy_width = 40
enemy_height = 40
enemy_speed = 0.1

# Create multiple enemies
enemies = []
num_enemies = 4

# Health settings
player_health = 5

# Screen shake
shake_timer = 0
shake_strength = 8

# Damage flash
damage_flash = 0

# Score settings
score = 0

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

# == Game loop == #

running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black background
    mouse_pos = pygame.mouse.get_pos()

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
        
        # Pause menu events
        if game_state == "pause":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if continue_rect.collidepoint(mouse_pos):
                    game_state = "game"
                
                elif quit_rect.collidepoint(mouse_pos):
                    game_state = "menu"

        # Pause menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == "game":
                game_state = "pause"
            elif event.key == pygame.K_ESCAPE and game_state == "pause":
                game_state = "game"

        # options back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == "options":
                game_state = "menu"
        
        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "game":
                bullets.append([player_x + player_width // 2, player_y])

            # RESTART GAME
            if event.key == pygame.K_r and game_state == "game_over":
                reset_game()
                game_state = "game"


    # menu screen
    if game_state == "menu":
        screen.fill((30, 30, 30))  # Dark background for menu

        title_rect = title_img.get_rect(center=(WIDTH//2, 150))
        screen.blit(title_img, title_rect)

        #play
        if play_rect.collidepoint(mouse_pos):
            screen.blit(play_img, (play_rect.x, play_rect.y + 5))
        else:
            screen.blit(play_img, play_rect)

        #options
        if options_rect.collidepoint(mouse_pos):
            screen.blit(options_img, (options_rect.x, options_rect.y + 5))
        else:
            screen.blit(options_img, options_rect)
        
        #exit
        if exit_rect.collidepoint(mouse_pos):
            screen.blit(exit_img, (exit_rect.x, exit_rect.y + 5))
        else:
            screen.blit(exit_img, exit_rect)


    elif game_state == "game":

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        player_x = max(0, min(WIDTH - player_width, player_x))

        # Bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < -20:
                bullets.remove(bullet)

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
                    game_state = "game_over"

            # Respawn enemy if it goes off screen
            if enemy[1] > HEIGHT:
                enemy[1] = random.randint(-200, 0)
                enemy[0] = random.randint(0, WIDTH - enemy_width)
            
        # Move bullets
        for bullet in bullets[:]:
            # Collision check
            for enemy in enemies:
                if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_width and
                    bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_height):

                    # Create explosion
                    explosions.append({
                        "x": enemy[0],
                        "y": enemy[1],
                        "frame": 0,
                        "timer": 0
                    })

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

        # Draw explosion animations
        for explosion in explosions[:]:

            frame = explosion["frame"]

            if frame < len(explosion_frames):

                screen.blit(
                    explosion_frames[frame],
                    (explosion["x"], explosion["y"])
                )

                explosion["timer"] += 1

                # speed control
                if explosion["timer"] >= 60:
                    explosion['frame'] += 1
                    explosion["timer"] = 0

            else:
                explosions.remove(explosion)

        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

        # Draw health bar
        screen.blit(health_images[player_health], (10, 50))

        # Score
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        screen.blit(score_text, (10, 10))

    elif game_state == "options":
        text = font.render("It's under construction", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)

        back_text = font.render("Press ESC to go back", True, (200, 200, 200))
        back_rect = back_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(back_text, back_rect)

    elif game_state == "pause":
        # Dark overlay effect
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)  # Set transparency
        overlay.fill((30, 30, 30))  # Black color
        screen.blit(overlay, (0, 0))

        # Title
        screen.blit(pause_img, pause_rect)

        # Continue button
        if continue_rect.collidepoint(mouse_pos):
            screen.blit(continue_img, (continue_rect.x, continue_rect.y + 5))
        else:
            screen.blit(continue_img, continue_rect)

        # Quit button
        if quit_rect.collidepoint(mouse_pos):
            screen.blit(quit_img, (quit_rect.x, quit_rect.y + 5))
        else:
            screen.blit(quit_img, quit_rect)

    # 💀 GAME OVER SCREEN
    elif game_state == "game_over":    
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