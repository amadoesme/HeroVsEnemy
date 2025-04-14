import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display window size and title
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero vs Enemy")

# Load sound effects for shooting and explosions
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Define basic colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
BLUE = (0, 128, 255)

# Game state constants
MENU = 0
PLAYING = 1
GAME_OVER = 2  # New game state for game over screen
game_state = MENU  # Start at the main menu

# Create player spaceship as a rectangle
spaceship = pygame.Rect(WIDTH//2, HEIGHT - 60, 60, 60)

# Ball fired by spaceship, initially hidden
ball = pygame.Rect(spaceship.x + 20, spaceship.y - 20, 10, 20)
ball_visible = False  # Ball only appears when fired
ball_speed = 10       # Speed at which the ball moves upward

# Set up multiple enemies
NUM_ENEMIES = 3
# Create enemy rectangles at varying vertical positions
enemies = [pygame.Rect(random.randint(0, WIDTH - 60), 100 + i * 80, 60, 60) for i in range(NUM_ENEMIES)]
# Create explosion placeholders for each enemy
explosions = [pygame.Rect(0, 0, 60, 60) for _ in range(NUM_ENEMIES)]
explosion_visible = [False] * NUM_ENEMIES  # Explosion visibility flags
explosion_timer = [0] * NUM_ENEMIES        # Explosion timing for each enemy
EXPLOSION_DELAY = 1000                     # Delay in milliseconds before enemy reappears

# Score and high score tracking
score = 0
high_score = 0  # Persistent highest score in a single run

# Life system
lives = 3  # Start with 3 lives
max_lives = 3  # Max lives for drawing hearts

# Load font and setup clock
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()  # Used to control FPS

# Buttons
reset_button = pygame.Rect(WIDTH - 110, 10, 100, 40)
start_button = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 - 25, 150, 50)
retry_button = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 + 40, 150, 50)  # New retry button

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Track mouse position
    now = pygame.time.get_ticks()  # Track current time

    # Event loop for handling user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the game

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == MENU:
                # Start game if start button is clicked
                if start_button.collidepoint(event.pos):
                    game_state = PLAYING
                    score = 0
                    lives = 3

            elif game_state == PLAYING:
                # Fire ball when spaceship is clicked
                if spaceship.collidepoint(event.pos):
                    ball.x = spaceship.x + 25
                    ball.y = spaceship.y - 20
                    ball_visible = True
                    shoot_sound.play()  # Play shooting sound
                else:
                    # Move spaceship to tap/click location
                    spaceship.x = event.pos[0] - spaceship.width // 2

                # Reset score and lives if reset button is clicked
                if reset_button.collidepoint(event.pos):
                    score = 0
                    lives = max_lives

            elif game_state == GAME_OVER:
                # Try again button on game over screen
                if retry_button.collidepoint(event.pos):
                    game_state = PLAYING
                    score = 0
                    lives = 3
                    # Reset enemies
                    for i in range(NUM_ENEMIES):
                        enemies[i].x = random.randint(0, WIDTH - 60)
                        enemies[i].y = 100 + i * 80

    # Display main menu screen
    if game_state == MENU:
        pygame.draw.rect(screen, BLUE, start_button)
        screen.blit(font.render("Start Game", True, WHITE), (start_button.x + 20, start_button.y + 10))
        screen.blit(font.render(f"High Score: {high_score}", True, BLACK), (WIDTH//2 - 80, HEIGHT//2 + 40))

    # Main gameplay screen
    elif game_state == PLAYING:
        # Move ball if visible
        if ball_visible:
            ball.y -= ball_speed
            if ball.y < 0:
                ball_visible = False  # Hide ball if it goes off screen

        # Check collision between ball and enemies
        for i in range(NUM_ENEMIES):
            if ball_visible and ball.colliderect(enemies[i]):
                # Trigger explosion animation
                explosions[i].x, explosions[i].y = enemies[i].x, enemies[i].y
                explosion_visible[i] = True
                explosion_timer[i] = now
                enemies[i].x = -100  # Temporarily hide enemy
                ball_visible = False
                score += 1  # Increase score
                explosion_sound.play()  # Play explosion sound

            # Enemy reaches bottom (simulate losing a life)
            if enemies[i].y > HEIGHT:
                enemies[i].x = random.randint(0, WIDTH - 60)
                enemies[i].y = 100 + i * 80
                lives -= 1  # Lose a life
                if lives <= 0:
                    game_state = GAME_OVER
                    if score > high_score:
                        high_score = score

            # Reposition enemy after explosion delay
            if explosion_visible[i] and now - explosion_timer[i] > EXPLOSION_DELAY:
                explosion_visible[i] = False
                enemies[i].x = random.randint(0, WIDTH - 60)

        # Draw spaceship
        pygame.draw.rect(screen, BLACK, spaceship)

        # Draw fired ball if visible
        if ball_visible:
            pygame.draw.rect(screen, RED, ball)

        # Draw enemies and explosion effects
        for i in range(NUM_ENEMIES):
            pygame.draw.rect(screen, GREEN, enemies[i])
            if explosion_visible[i]:
                pygame.draw.rect(screen, ORANGE, explosions[i])

        # Draw reset button
        pygame.draw.rect(screen, GRAY, reset_button)
        screen.blit(font.render("Reset", True, BLACK), (reset_button.x + 15, reset_button.y + 10))

        # Display current score
        screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))

        # Display hearts/lives as red circles
        for i in range(lives):
            pygame.draw.circle(screen, RED, (WIDTH - 30 - i * 30, 60), 10)

    # Game Over screen
    elif game_state == GAME_OVER:
        screen.blit(font.render("Game Over!", True, RED), (WIDTH//2 - 80, HEIGHT//2 - 60))
        screen.blit(font.render(f"Final Score: {score}", True, BLACK), (WIDTH//2 - 80, HEIGHT//2 - 20))
        screen.blit(font.render(f"High Score: {high_score}", True, BLACK), (WIDTH//2 - 80, HEIGHT//2 + 10))
        pygame.draw.rect(screen, BLUE, retry_button)
        screen.blit(font.render("Try Again", True, WHITE), (retry_button.x + 20, retry_button.y + 10))

    # Update the screen and tick the clock
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

# Quit pygame once the game loop ends
pygame.quit()
