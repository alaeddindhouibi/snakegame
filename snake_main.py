import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Screen dimension
WIDTH, HEIGHT = 800, 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Icons")

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(0, WIDTH // 10) * 10,
            random.randrange(0, HEIGHT // 10) * 10]
food_spawn = True
poison_pos = [random.randrange(0, WIDTH // 10) * 10,
              random.randrange(0, HEIGHT // 10) * 10]
poison_spawn = True
extrafood_pos = None
extrafood_spawn = False
extrafood_exist = False
extra_spawn_time = None
last_extrafood_score = 0
direction = "RIGHT"
score = 0
clock = pygame.time.Clock()

# Fonts for icons
font = pygame.font.SysFont("Segoe UI Emoji", 20)  # supports emojis
snake_icon = font.render("🟩", True, WHITE)       # Snake body
food_icon = font.render("🍎", True, WHITE)        # Normal food
poison_icon = font.render("☠️", True, WHITE)      # Poison
extrafood_icon = font.render("🍌", True, WHITE)   # Extra food

# Game over function
def game_over():
    font_big = pygame.font.SysFont("Arial", 40)
    game_over_surface = font_big.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_surface, rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Update snake position
    if direction == "UP":
        snake_pos[1] -= 10
    elif direction == "DOWN":
        snake_pos[1] += 10
    elif direction == "LEFT":
        snake_pos[0] -= 10
    elif direction == "RIGHT":
        snake_pos[0] += 10

    # Snake body growing
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(0, WIDTH // 10) * 10,
                    random.randrange(0, HEIGHT // 10) * 10]
        food_spawn = True

    # Poison
    if snake_pos == poison_pos:
        score -= 1
        if len(snake_body) > 1:
            snake_body.pop()
        poison_spawn = False

    if not poison_spawn:
        poison_pos = [random.randrange(0, WIDTH // 10) * 10,
                      random.randrange(0, HEIGHT // 10) * 10]
        poison_spawn = True

    # Extra food
    if score % 5 == 0 and score != 0 and score != last_extrafood_score:
        extrafood_spawn = True
        extrafood_exist = True
        last_extrafood_score = score

    if extrafood_spawn:
        extrafood_pos = [random.randrange(0, WIDTH // 10) * 10,
                         random.randrange(0, HEIGHT // 10) * 10]
        extrafood_spawn = False
        extra_spawn_time = time.time()

    if extrafood_exist and extra_spawn_time is not None:
        if time.time() - extra_spawn_time > 5:
            extrafood_exist = False
            extrafood_pos = None

    if extrafood_exist and snake_pos == extrafood_pos:
        score += 5
        extrafood_exist = False
        extrafood_pos = None

    # Game over conditions
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        game_over()
    if score < 0:
        game_over()

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Update screen
    screen.fill(BLACK)

    # Draw snake
    for pos in snake_body:
        screen.blit(snake_icon, (pos[0], pos[1]))

    # Draw food & poison
    screen.blit(food_icon, (food_pos[0], food_pos[1]))
    screen.blit(poison_icon, (poison_pos[0], poison_pos[1]))
    if extrafood_exist and extrafood_pos is not None:
        screen.blit(extrafood_icon, (extrafood_pos[0], extrafood_pos[1]))

    # Show score
    score_surface = pygame.font.SysFont("Arial", 20).render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

    pygame.display.update()

    # Control game speed
    vitesse = 10 + score
    clock.tick(vitesse)
