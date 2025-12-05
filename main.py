
import pygame
import sys
import math

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
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (148, 0, 211)
ORANGE = (247, 94, 37)

#шрифты
font = pygame.font.Font(".\PressStart2P.ttf", 40)
title_font = pygame.font.Font(".\PressStart2P.ttf", 76)
menu_font = pygame.font.Font(".\PressStart2P.ttf", 44)

#частота обновления экрана
FPS = 60
clock = pygame.time.Clock()

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200
PADDLE_SPEED = 15

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
cpu_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

BALL_SIZE = 40
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 5
ball_speed_y = 5
# ball_speed = math.hypot(ball_speed_x, ball_speed_y)

# Отслеживание движения ракеток
player_paddle_last_y = player_paddle.y
cpu_paddle_last_y = cpu_paddle.y

# Хвост мяча
ball_trail = []          # Список позиций
max_trail_length = 10    # Максимальная длина шлейфа
trail_decay = 1          # Насколько быстро "гаснет" хвост

# Хвост ракетки
paddle_trail = []
paddle_trail_cpu = []
# max_trail_length = 10
# trail_decay = 1

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

blink_timer = 0
blink = True

# Инициализация микшера для звука
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# def draw_tail(trail, color_main, color_edge=None):
    # """
    # Рисует шлейф из кругов вдоль траектории.
    # Если передан color_edge — рисует кольцо (обводку).
    # trail: список кортежей ('up'/'down', (x, y))
    # """
    # if not trail:
    #     return

    # for i, (direction, pos) in enumerate(trail):
    #     alpha = int(255 * (i / len(trail)))
    #     radius = int(PADDLE_WIDTH * 1.5 * (i / len(trail)))
    #     if radius < 2:
    #         continue

    #     surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        
    #     # Основной цвет с прозрачностью
    #     main_color = (*color_main, alpha)
    #     pygame.draw.circle(surface, main_color, (radius, radius), radius)
        
    #     # Край (если нужен)
    #     if color_edge:
    #         edge_color = (*color_edge, int(alpha * 0.7))
    #         pygame.draw.circle(surface, edge_color, (radius, radius), radius, 2)
        
    #     # Сдвигаем позицию в зависимости от направления
    #     offset = radius
    #     if direction == 'up':
    #         blit_pos = (pos[0] - radius, pos[1] - offset)
    #     else:  # 'down'
    #         blit_pos = (pos[0] - radius, pos[1] - radius)

    #     screen.blit(surface, blit_pos)

def draw_ball_trail(trail, color):
    if not trail:
        return
    for i, pos in enumerate(trail):
        alpha = int(255 * (i / len(trail)))
        radius = int(BALL_SIZE // 2 * (i / len(trail)))
        if radius < 1:
            continue
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
        screen.blit(surface, (pos[0] - radius, pos[1] - radius))


def draw_paddle_trail(trail, color_main, key, color_edge=None):
    if not trail:
        return
    for i, (direction, pos) in enumerate(trail):
        if key == direction:
            alpha = int(255 * (i / len(trail)))
            radius = int(PADDLE_WIDTH * 0.8 * (i / len(trail)))
            if radius < 2:
                continue
            surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*color_main, alpha), (radius, radius), radius)
            if color_edge:
                pygame.draw.circle(surface, (*color_edge, int(alpha * 0.7)), (radius, radius), radius, 2)
        
            blit_pos = (pos[0] - radius, pos[1] - radius)
            screen.blit(surface, blit_pos)

def draw_cpu_paddle_trail(trail, color_main, color_edge=None):
    """
    Отрисовывает шлейф для cpu_paddle — все точки, независимо от направления.
    """
    if not trail:
        return
    for i, (direction, pos) in enumerate(trail):
        alpha = int(255 * (i / len(trail)))
        radius = int(PADDLE_WIDTH * 0.8 * (i / len(trail)))
        if radius < 2:
            continue
        surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color_main, alpha), (radius, radius), radius)
        if color_edge:
            pygame.draw.circle(surface, (*color_edge, int(alpha * 0.7)), (radius, radius), radius, 2)
        blit_pos = (pos[0] - radius, pos[1] - radius)
        screen.blit(surface, blit_pos)

def draw_menu():
    global blink_timer

    # Обновляем таймер (плавно увеличивается)
    blink_timer += 0.15  # Скорость анимации
    if blink_timer > 2 * math.pi:
        blink_timer -= 2 * math.pi

    # Мигающий цвет
    blink_value = int((math.sin(blink_timer) + 1) * 127.5)  # От 0 до 255
    blink_color = (blink_value, 255, blink_value)  # Цвет "светодиодного" свечения
    blink_color_red = (255, blink_value, blink_value)

    screen.fill(BLACK)

    # Заголовок
    if blink:
        title = title_font.render("PONG 1972", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        title_outline = title_font.render("PONG 1972", True, BLUE)
        screen.blit(title_outline, ((WIDTH // 2 - title.get_width() // 2) + 2, (HEIGHT // 4) + 2))

    # Кнопки
    for i, option in enumerate(menu_options):
        if i == menu_selection and i != 2:
            # Выбранная кнопка — мигает
            color = GREEN
            color = blink_color
        elif i == menu_selection and i == 2:
            # Кнопка "Выход" — всегда красная
            color = RED
            color = blink_color_red
        else:
            # Остальные — обычные
            color = WHITE

        # if blink:
        button_text = menu_font.render(option, True, color)
        rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
        screen.blit(button_text, rect)

        # Добавим лёгкую "окантовку" для выделенной кнопки
        # if i == menu_selection:
        #     outline_rect = rect.inflate(20, 10)  # Увеличиваем рамку
        #     pygame.draw.rect(screen, blink_color, outline_rect, 3, border_radius=12)
        # # Красная окантовка у "Выход"
        # if i == 2:
        #     outline_rect = rect.inflate(15, 8)
        #     pygame.draw.rect(screen, RED, outline_rect, 3, border_radius=10)

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
click_sound = load_sound("click.wav")

music_channel = pygame.mixer.Channel(0)

music_channel.play(menu_music, -1)
music_channel.set_volume(0.2)

#игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.time.get_ticks() % 0.5 == 0:  # каждые 0.1 сек
        blink = not blink
    
    # screen.fill(BLACK)

    # pygame.display.update()
    # clock.tick(FPS)

    keys = pygame.key.get_pressed()

    if game_state == "MENU":

        # Управление меню
        if keys[pygame.K_s] and not key_down:
            menu_selection = (menu_selection + 1) % len(menu_options)
            click_sound.play()
            key_down = True
        if keys[pygame.K_w] and not key_up:
            menu_selection = (menu_selection - 1) % len(menu_options)
            click_sound.play()
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

        if game_mode == "PVE" and not game_over:
                # ИИ управляет правой ракеткой
                if cpu_paddle.centery < ball.centery and cpu_paddle.bottom < HEIGHT:
                    cpu_paddle.y += PADDLE_SPEED * 0.85
                if cpu_paddle.centery > ball.centery and cpu_paddle.top > 0:
                    cpu_paddle.y -= PADDLE_SPEED * 0.85

        elif game_mode == "PVP" and not game_over:
                # Игрок 2 управляет правой ракеткой
                if keys[pygame.K_UP] and cpu_paddle.top > 0:
                    cpu_paddle.y -= PADDLE_SPEED
                if keys[pygame.K_DOWN] and cpu_paddle.bottom < HEIGHT:
                    cpu_paddle.y += PADDLE_SPEED
                lose_sound = victory_sound

        # Рассчитываем текущую скорость
        ball_speed = math.hypot(ball_speed_x, ball_speed_y)  # sqrt(dx² + dy²)
        current_trail_length = int(min(15, ball_speed * 1.5))

        # === Хвосты объектов при высокой скорости мяча ===
        if ball_speed > 12:
            ball_trail.append((ball.centerx, ball.centery))

            if player_paddle.y < player_paddle_last_y:
                paddle_trail.append(('up', player_paddle.midbottom))
            elif player_paddle.y > player_paddle_last_y:
                paddle_trail.append(('down', player_paddle.midtop))

            if cpu_paddle.y < cpu_paddle_last_y:
                paddle_trail_cpu.append(('up', cpu_paddle.midbottom))
            elif cpu_paddle.y > cpu_paddle_last_y:
                paddle_trail_cpu.append(('down', cpu_paddle.midtop))

            # Ограничиваем длину
            if len(ball_trail) > max_trail_length:
                ball_trail.pop(0)
            if len(paddle_trail) > max_trail_length:
                paddle_trail.pop(0)
            if len(paddle_trail_cpu) > max_trail_length:
                paddle_trail_cpu.pop(0)
        else:
            ball_trail.clear()
            paddle_trail.clear()
            paddle_trail_cpu.clear()

        # Движение мяча
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            if ball_speed_y < 7:
                ball_speed_y *= -1.1
            else:
                ball_speed_y *= -1             
            if bounce_wall_sound:
                bounce_wall_sound.play()    

        if ball.colliderect(player_paddle) or ball.colliderect(cpu_paddle):
            if ball_speed_x < 7:
                ball_speed_x *= -1.1
            else:
                ball_speed_x *= -1
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

        # Рисуем шлейфы
        draw_ball_trail(ball_trail, YELLOW)

        if game_mode == "PVE":
            player_color, cpu_color = (63, 211, 0), (148, 0, 211)
            if keys[pygame.K_s]:
                draw_paddle_trail(paddle_trail, player_color, "down", BLACK)
            if keys[pygame.K_w]:
                draw_paddle_trail(paddle_trail, player_color, "up", BLACK)
            draw_cpu_paddle_trail(paddle_trail_cpu, cpu_color, BLACK)
        else:
            player_color = cpu_color = BLUE
            if keys[pygame.K_UP]:
                draw_paddle_trail(paddle_trail_cpu, cpu_color, "up", WHITE)
            if keys[pygame.K_DOWN]:
                draw_paddle_trail(paddle_trail_cpu, cpu_color, "down", WHITE)
            if keys[pygame.K_s]:
                draw_paddle_trail(paddle_trail, player_color, "down", WHITE)
            if keys[pygame.K_w]:
                draw_paddle_trail(paddle_trail, player_color, "up", WHITE)

        pygame.draw.rect(screen, WHITE, player_paddle, 5)
        pygame.draw.rect(screen, WHITE, cpu_paddle, 5)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Счёт
        score_text = font.render(f"| {player_score} : {cpu_score} |", True, WHITE, BLACK)
        screen.blit(score_text, (window_center[0] - score_text.get_width() // 2, window_center[1] // 10))

        # Мяч
        pygame.draw.ellipse(screen, WHITE, ball, 5)

        # === ЭКРАН ПОБЕДЫ — НАКЛАДЫВАЕТСЯ ПОВЕРХ ===
        if game_over:
            status_winner = True
            ball.center = (WIDTH // 2, HEIGHT // 2)  # можно убрать, если не нужно
            winner = " Победил игрок слева! " if player_score >= winning_score else " Победил игрок справа! "
            if game_mode == "PVE":
                winner = " Ты выиграл! " if player_score >= winning_score else " Скайнет победил! "

            status_winner = (player_score >= winning_score)
            over_text = font.render(winner, True, BLACK, GREEN if status_winner or game_mode == "PVP" else RED)
            restart_text = font.render(" Нажми R чтобы начать заново ", True, WHITE, GREY)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

            if keys[pygame.K_r]:
                player_score = 0
                cpu_score = 0
                game_over = False
                ball_speed_x = 5
                ball_speed_y = 5
                victory_sound_played = True
                paddle_trail.clear()
                paddle_trail_cpu.clear()
                ball_trail.clear()

    # Обновляем предыдущие позиции для определения направления
    player_paddle_last_y = player_paddle.y
    cpu_paddle_last_y = cpu_paddle.y

    pygame.display.update()
    clock.tick(FPS)

