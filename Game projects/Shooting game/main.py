import pygame
import random
pygame.init()
pygame.font.init()

font = pygame.font.Font("Fonts/pixeltype.ttf", 36)
big_font = pygame.font.Font("Fonts/pixeltype.ttf", 72)

# Screen settings
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("X Hunter")

fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))

# FPS control
clock = pygame.time.Clock()

## == Assets == ##

# Player, Enemy, Bullet assets and sizes
player_img = pygame.image.load("Assets/Playership1.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("Assets/Enemyship.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bullet_img = pygame.image.load("Assets/Bullet1.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Health bar assets
health_images = [
    pygame.image.load("Assets/health_0.png"),
    pygame.image.load("Assets/health_1.png"),
    pygame.image.load("Assets/health_2.png"),
    pygame.image.load("Assets/health_3.png"),
    pygame.image.load("Assets/health_4.png"),
    pygame.image.load("Assets/health_5.png")
]

explosion_frames = []

for i in range(1, 9):
    img = pygame.image.load(f"Assets/explosion_{i}.png")
    img = pygame.transform.scale(img, (70, 70))
    explosion_frames.append(img)

# Resize health bar
health_images = [pygame.transform.scale(img, (200, 70)) for img in health_images]

# Menu assets
title_img = pygame.image.load("Assets/title.png")
play_img = pygame.image.load("Assets/play.png")
options_img = pygame.image.load("Assets/options.png")
exit_img = pygame.image.load("Assets/exit.png")
pause_img = pygame.image.load("Assets/menu.png")
continue_img = pygame.image.load("Assets/continue.png")
quit_img = pygame.image.load("Assets/quit.png")
restart_img = pygame.image.load("Assets/restart.png")
quit_gameover_img = pygame.image.load("Assets/quitt.png")

# Resize Menu assets
title_img = pygame.transform.scale(title_img, (350, 120))
play_img = pygame.transform.scale(play_img, (250, 80))
options_img = pygame.transform.scale(options_img, (250, 80))
exit_img = pygame.transform.scale(exit_img, (250, 80))
pause_img = pygame.transform.scale(pause_img, (400, 100))
continue_img = pygame.transform.scale(continue_img, (250, 80))
quit_img = pygame.transform.scale(quit_img, (250, 72))
restart_img = pygame.transform.scale(restart_img, (250, 80))
quit_gameover_img = pygame.transform.scale(quit_gameover_img, (250, 80))

# Game State
game_state = "menu"  

# Menu buttons
play_rect = play_img.get_rect(center=(WIDTH//2, 300))
options_rect = options_img.get_rect(center=(WIDTH//2, 400))
exit_rect = exit_img.get_rect(center=(WIDTH//2, 500))
continue_rect = continue_img.get_rect(center=(WIDTH//2, 350))
quit_rect = quit_img.get_rect(center=(WIDTH//2, 450))
pause_rect = pause_img.get_rect(center=(WIDTH//2, 200))
restart_rect = restart_img.get_rect(center=(WIDTH//2, 350))
quit_gameover_rect = quit_gameover_img.get_rect(center=(WIDTH//2, 450))

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 5

# Bullet settings
bullets = []
bullet_speed = 10

# Explosion settings
explosions = []

# Enemy settings
enemy_width = 40
enemy_height = 40
enemy_speed = 5

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

# Player explosion
player_dead = False
player_explosion = None

# Score settings
score = 0

# Fade animation
fade_alpha = 255
fade_speed = 15
fading_in = True
fading_out = False
next_state = None


## == Functions == ##

# Start fade function
def start_fade(target_state):
    global fading_out, fading_in, next_state, fade_alpha

    fading_out = True
    fading_in = False

    next_state = target_state
    
    fade_alpha = 0

# Reset game function
def reset_game():
    global player_x, player_y
    global bullets, enemies
    global score, player_health
    global player_dead, player_explosion
    global explosions, shake_timer, damage_flash

    player_x = WIDTH // 2
    bullets = []
    enemies = []

    for i in range(5):
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-600, 0)
        enemies.append([x, y])

    score = 0
    player_health = 5

    shake_timer = 0
    damage_flash = 0

    player_x = WIDTH // 2
    player_y = HEIGHT - 80

    player_dead = False
    player_explosion = None

    explosions.clear()

## == Game loop == ##


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
                    start_fade("game")

                elif options_rect.collidepoint(mouse_pos):
                    start_fade("options")

                elif exit_rect.collidepoint(mouse_pos):
                    running = False
        
        # Pause menu events
        if game_state == "pause":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if continue_rect.collidepoint(mouse_pos):
                    start_fade("game")
                
                elif quit_rect.collidepoint(mouse_pos):
                    start_fade("menu")

        # Game over events
        if game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:

                if restart_rect.collidepoint(mouse_pos):
                    reset_game()
                    start_fade("game")
                
                elif quit_gameover_rect.collidepoint(mouse_pos):
                    start_fade("menu")

        # Pause menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == "game":
                start_fade("pause")
            elif event.key == pygame.K_ESCAPE and game_state == "pause":
                start_fade("game")

        # options back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == "options":
                start_fade("menu")
        
        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "game":
                bullets.append([player_x + player_width // 2, player_y])


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
        if not player_dead:
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
            if not player_dead and (
                enemy[0] < player_x + player_width and
                enemy[0] + enemy_width > player_x and
                enemy[1] < player_y + player_height and
                enemy[1] + enemy_height > player_y):

                player_health -= 1

                shake_timer = 40
                damage_flash = 25

                # Reset enemy after hit
                enemy[1] = random.randint(-200, 0)
                enemy[0] = random.randint(0, WIDTH - enemy_width)

                if player_health <= 0:
                    player_health = 0

                    # Create player explosion
                    player_explosion = {
                        "x": player_x - 10,
                        "y": player_y - 10,
                        "frame": 0,
                        "timer": 0
                    }

                    player_x = -1000
                    player_y = -1000

                    player_dead = True

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
        
        shake_x = 0
        shake_y = 0
    
        if shake_timer > 0:
            shake_x = random.randint(-shake_strength, shake_strength)
            shake_y = random.randint(-shake_strength, shake_strength)
            shake_timer -= 1

        # Draw player
        if not player_dead:
            screen.blit(player_img, (player_x + shake_x, player_y + shake_y))

        # Draw enemy
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0] + shake_x, enemy[1] + shake_y))

        # Draw bullets
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0] + shake_x, bullet[1] + shake_y))

        # Draw health bar
        screen.blit(health_images[player_health], (10, 50))

        # Damage flash
        if damage_flash > 0:

            flash = pygame.Surface((WIDTH, HEIGHT))
            flash.set_alpha(80)
            flash.fill((255, 0, 0))

            screen.blit(flash, (0, 0))

            damage_flash -= 1

        # Draw explosion animations
        for explosion in explosions[:]:

            frame = explosion["frame"]

            if frame < len(explosion_frames):

                screen.blit(
                    explosion_frames[frame],
                    (explosion["x"] + shake_x, explosion["y"] + shake_y)
                )

                explosion["timer"] += 1

                # speed control
                if explosion["timer"] >= 3:
                    explosion['frame'] += 1
                    explosion["timer"] = 0

            else:
                explosions.remove(explosion)

        # Player explosion
        if player_dead and player_explosion:

            frame = player_explosion["frame"]

            if frame < len(explosion_frames):

                screen.blit(
                    explosion_frames[frame],
                    (player_explosion["x"], player_explosion["y"])
                )

                player_explosion["timer"] += 1

                if player_explosion["timer"] >= 5:
                    player_explosion["frame"] += 1
                    player_explosion["timer"] = 0

            else:
                player_dead = False
                start_fade("game_over")
                player_explosion = None


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
        go_rect = game_over_text.get_rect(center=(WIDTH//2, 200))

        go_shadow = big_font.render("GAME OVER", True, (0, 0, 0))

        # Draw shadow for "GAME OVER" text
        screen.blit(go_shadow, (go_rect.x + 5, go_rect.y + 5))
        screen.blit(game_over_text, go_rect)
        
        # Main text
        screen.blit(game_over_text, go_rect)

        # Restart button
        if restart_rect.collidepoint(mouse_pos):
            screen.blit(restart_img, (restart_rect.x, restart_rect.y + 5))
        else:
            screen.blit(restart_img, restart_rect)

        # Quit button
        if quit_gameover_rect.collidepoint(mouse_pos):
            screen.blit(quit_gameover_img, (quit_gameover_rect.x, quit_gameover_rect.y + 5))
        else:
            screen.blit(quit_gameover_img, quit_gameover_rect)


    # Fade animation system

    if fading_in:

        fade_alpha -= fade_speed

        if fade_alpha <= 0:
            fade_alpha = 0
            fading_in = False

    # Fade out
    if fading_out:

        fade_alpha += fade_speed

        if fade_alpha >= 255:

            fade_alpha = 255

            fading_out = False

            # Change game screen
            game_state = next_state

            # Start fade in
            fading_in = True

    # Draw fade layer
    fade_surface.set_alpha(fade_alpha)
    screen.blit(fade_surface, (0, 0)) 


    pygame.display.update()    
    clock.tick(60)

pygame.quit()