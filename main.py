
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
title_font = pygame.font.SysFont("Comic Sans MS", 88, bold=True)
menu_font = pygame.font.SysFont("Comic Sans MS", 50)

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

# Состояние игры
game_state = "MENU"  # Может быть: "MENU" или "GAME"

# Выбор в меню
menu_selection = 0  # 0: PvP, 1: PvE, 2: Выход
menu_options = ["Игрок против игрока", "Игрок против машины", "Выход"]

game_mode = "PVE"  # по умолчанию
key_down = False   # защита от повтора при удержании
key_up = False

# Инициализация микшера для звука
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

def draw_menu():
    screen.fill(BLACK)
    
    # Заголовок
    title = title_font.render("PONG 1972", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    # Кнопки
    for i, option in enumerate(menu_options):
        color = GREEN if i == menu_selection and i != 2 else WHITE
        if i == menu_selection and i == 2:
            color = RED
        outline = 5 if i == 2 else 0  # Красная рамка только у "Выход"
        button_text = menu_font.render(option, True, color)
        rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
        screen.blit(button_text, rect)
        
        # Окантовка для "Выход"
        # if i == 2:
        #     pygame.draw.rect(screen, RED, rect, outline)

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
menu_music = load_sound("menu.wav")

music_channel = pygame.mixer.Channel(0)

music_channel.play(menu_music, -1)
music_channel.set_volume(0.5)

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

    if game_state == "MENU":

        # Управление меню
        if keys[pygame.K_s] and not key_down:
            menu_selection = (menu_selection + 1) % len(menu_options)
            key_down = True
        if keys[pygame.K_w] and not key_up:
            menu_selection = (menu_selection - 1) % len(menu_options)
            key_up = True
        if not keys[pygame.K_s]:
            key_down = False
        if not keys[pygame.K_w]:
            key_up = False

        # Выбор
        if keys[pygame.K_RETURN]:
            if menu_selection == 0:  # PvP
                game_mode = "PVP"
                game_state = "GAME"
                music_channel.stop()
                player_score = 0
                cpu_score = 0
                game_over = False
                victory_sound_played = True
                ball.center = (WIDTH // 2, HEIGHT // 2)
            elif menu_selection == 1:  # PvE
                game_mode = "PVE"
                game_state = "GAME"
                music_channel.stop()
                player_score = 0
                cpu_score = 0
                game_over = False
                victory_sound_played = True
                ball.center = (WIDTH // 2, HEIGHT // 2)
            elif menu_selection == 2:  # Выход
                pygame.quit()
                sys.exit()

        draw_menu()

    elif game_state == "GAME":

        if keys[pygame.K_w] and player_paddle.top > 0:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
            player_paddle.y += PADDLE_SPEED
        if keys[pygame.K_ESCAPE]:
            game_state = "MENU"
            player_score = 0
            cpu_score = 0
            game_over = False
            ball.center = (WIDTH // 2, HEIGHT // 2)
            # ball_speed_x = 0
            # ball_speed_y = 0
            music_channel.play(menu_music, -1)
            music_channel.set_volume(0.5)

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

        if game_mode == "PVE" and not game_over:
                # ИИ управляет правой ракеткой
                if cpu_paddle.centery < ball.centery and cpu_paddle.bottom < HEIGHT:
                    cpu_paddle.y += PADDLE_SPEED * 0.85
                if cpu_paddle.centery > ball.centery and cpu_paddle.top > 0:
                    cpu_paddle.y -= PADDLE_SPEED * 0.85

        elif game_mode == "PVP" and not game_over:
                # Игрок 2 управляет правой ракеткой: W и S
                if keys[pygame.K_UP] and cpu_paddle.top > 0:
                    cpu_paddle.y -= PADDLE_SPEED
                if keys[pygame.K_DOWN] and cpu_paddle.bottom < HEIGHT:
                    cpu_paddle.y += PADDLE_SPEED
                lose_sound = victory_sound
        
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
        
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_paddle, 5)
        pygame.draw.rect(screen, WHITE, cpu_paddle, 5)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), True)

        score_text = font.render(f"| {player_score} : {cpu_score} |", True, WHITE, GREY)
        screen.blit(score_text, (window_center[0] - score_text.get_width() // 2, window_center[1] // 10))

        pygame.draw.ellipse(screen, WHITE, ball, 5)
    
    # victory_sound_played = False

    if game_over:
        status_winner = True
        ball.center = (WIDTH // 2, HEIGHT // 2)
        # ball_speed_x = 0
        # ball_speed_y = 0
        if game_mode == "PVP":
            winner = "Победил игрок слева!" if player_score >= winning_score else "Победил игрок справа!"
        else:
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

