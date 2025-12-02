
import pygame
import sys

pygame.init()

#размеры экрана
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong 1972")

#цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#частота обновления экрана
FPS = 45
clock = pygame.time.Clock()

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200
PADDLE_SPEED = 10

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
cpu_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

BALL_SIZE = 20
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 10
ball_speed_y = 10

#игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    # screen.fill(BLACK)

    # pygame.display.update()
    # clock.tick(FPS)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1.1

    if ball.colliderect(player_paddle) or ball.colliderect(cpu_paddle):
        ball_speed_x *= -1.1

    if ball.left <= 0:
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 10
        ball_speed_y = 10
        ball_speed_x *= +1.5
    
    if ball.right >= WIDTH:
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 10
        ball_speed_y = 10
        ball_speed_x *= -1.5

    if cpu_paddle.centery < ball.centery and cpu_paddle.bottom < HEIGHT:
        cpu_paddle.y += PADDLE_SPEED * 0.85 

    if cpu_paddle.centery > ball.centery and cpu_paddle.top > 0:
        cpu_paddle.y -= PADDLE_SPEED * 0.85
    
    

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle, 5)
    pygame.draw.rect(screen, WHITE, cpu_paddle, 5)
    pygame.draw.ellipse(screen, WHITE, ball, 5)

    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), True)

    pygame.display.update()
    clock.tick(FPS)

