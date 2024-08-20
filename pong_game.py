import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background_color = BLACK

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Ball dimensions
BALL_SIZE = 20

# Paddle positions
paddle1_x, paddle1_y = 50, (HEIGHT // 2) - (PADDLE_HEIGHT // 2)
paddle2_x, paddle2_y = WIDTH - 50 - PADDLE_WIDTH, (HEIGHT // 2) - (PADDLE_HEIGHT // 2)

# Ball position and speed
ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball_speed_x = random.choice([5, -5])
ball_speed_y = random.choice([5, -5])
ball_speed_increment = 0.5

# Paddle speed
paddle_speed = 7

# Scoring
score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)
game_over_font = pygame.font.Font(None, 100)

# Sound effects
paddle_hit_sound = pygame.mixer.Sound('paddle_hit.wav')
score_sound = pygame.mixer.Sound('score.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# Clock
clock = pygame.time.Clock()

# Winning score
winning_score = 2

# Game loop
def game_loop():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score1, score2, background_color

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < HEIGHT - PADDLE_HEIGHT:
            paddle1_y += paddle_speed
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - PADDLE_HEIGHT:
            paddle2_y += paddle_speed

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with top and bottom walls
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddles, increase speed, play sound, and change background color
        if (ball_x <= paddle1_x + PADDLE_WIDTH and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT) or \
           (ball_x >= paddle2_x - BALL_SIZE and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT):
            ball_speed_x = -ball_speed_x
            ball_speed_x += ball_speed_increment if ball_speed_x > 0 else -ball_speed_increment
            ball_speed_y += ball_speed_increment if ball_speed_y > 0 else -ball_speed_increment
            paddle_hit_sound.play()

            # Change background color
            background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Ball passes left paddle (Player 2 scores)
        if ball_x <= 0:
            score2 += 1
            score_sound.play()
            ball_x = WIDTH // 2 - BALL_SIZE // 2
            ball_y = HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = random.choice([5, -5])
            ball_speed_y = random.choice([5, -5])

        # Ball passes right paddle (Player 1 scores)
        if ball_x >= WIDTH - BALL_SIZE:
            score1 += 1
            score_sound.play()
            ball_x = WIDTH // 2 - BALL_SIZE // 2
            ball_y = HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = random.choice([5, -5])
            ball_speed_y = random.choice([5, -5])

        # Check for game over
        if score1 == winning_score or score2 == winning_score:
            game_over_screen()

        # Fill the screen with the current background color
        screen.fill(background_color)

        # Draw paddles
        pygame.draw.rect(screen, WHITE, (paddle1_x, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        # Draw ball
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

        # Draw scores
        score_text = font.render(f"{score1}", True, WHITE)
        screen.blit(score_text, (WIDTH // 4, 20))
        score_text = font.render(f"{score2}", True, WHITE)
        screen.blit(score_text, (3 * WIDTH // 4, 20))

        # Update display
        pygame.display.flip()

        # Frame rate
        clock.tick(60)

def game_over_screen():
    global score1, score2
    screen.fill(BLACK)
    if score1 == winning_score:
        game_over_text = game_over_font.render("Player 1 Wins!", True, WHITE)
    else:
        game_over_text = game_over_font.render("Player 2 Wins!", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    game_over_sound.play()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
