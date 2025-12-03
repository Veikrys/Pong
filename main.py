
import pygame
import sys

pygame.init()

#размеры экрана
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong 1972")
window_center = pygame.display.get_surface().get_rect().center

#цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont("Comic Sans MS", 64)

#частота обновления экрана
FPS = 60
clock = pygame.time.Clock()

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200
PADDLE_SPEED = 15

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
cpu_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

BALL_SIZE = 20
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 5
ball_speed_y = 5

player_score = 0
cpu_score = 0
winning_score = 1
game_over = False
victory_sound_played = True

# Инициализация микшера для звука
pygame.mixer.init()

def load_sound(name):
    try:
        sound = pygame.mixer.Sound(f"sounds/{name}")
        return sound
    except pygame.error as e:
        print(f"Не удалось загрузить звук {name}: {e}")
        return None

bounce_paddle_sound = load_sound("paddle.wav")
bounce_wall_sound = load_sound("wall.wav")
score_sound = load_sound("score.wav")
victory_sound = load_sound("victory.mp3")
lose_sound = load_sound("lose.wav")

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
        if bounce_wall_sound:
            bounce_wall_sound.play()    

    if ball.colliderect(player_paddle) or ball.colliderect(cpu_paddle):
        ball_speed_x *= -1.1
        if bounce_paddle_sound:
            bounce_paddle_sound.play()

    if ball.left <= 0:
        cpu_score += 1
        if score_sound:
            score_sound.play()
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 5
        ball_speed_y = 5
        ball_speed_x *= +1.5
    
    if ball.right >= WIDTH:
        player_score += 1
        if score_sound:
            score_sound.play()
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 5
        ball_speed_y = 5
        ball_speed_x *= -1.5

    if cpu_paddle.centery < ball.centery and cpu_paddle.bottom < HEIGHT:
        cpu_paddle.y += PADDLE_SPEED * 0.85 

    if cpu_paddle.centery > ball.centery and cpu_paddle.top > 0:
        cpu_paddle.y -= PADDLE_SPEED * 0.85
    
    if player_score >= winning_score or cpu_score >= winning_score:
        game_over = True
        # victory_sound_played = True if victory_sound_played != True else False

    if victory_sound_played:
            if player_score >= winning_score:
                if victory_sound:
                    victory_sound.play()
                    victory_sound_played = False

            if cpu_score >= winning_score:
                if lose_sound:
                    lose_sound.play()
                    victory_sound_played = False
    
    # victory_sound_played = False

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle, 5)
    pygame.draw.rect(screen, WHITE, cpu_paddle, 5)

    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), True)

    score_text = font.render(f"| {player_score} : {cpu_score} |", True, WHITE, GREY)
    screen.blit(score_text, (window_center[0] - score_text.get_width() // 2, window_center[1] // 10))

    pygame.draw.ellipse(screen, WHITE, ball, 5)

    if game_over:
        status_winner = True
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 0
        ball_speed_y = 0
        winner = "Ты выиграл!" if player_score >= winning_score else "Скайнет победил!" 
        status_winner = False if winner == "Скайнет победил!" else True
        over_text = font.render(winner, True, BLACK, GREEN if status_winner == True else RED)
        restart_text = font.render("Нажми R чтобы начать заново", True, WHITE, GREY)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        # Перезапуск
        if keys[pygame.K_r]:
            player_score = 0
            cpu_score = 0
            game_over = False
            ball_speed_x = 5
            ball_speed_y = 5
            victory_sound_played = True

    pygame.display.update()
    clock.tick(FPS)

