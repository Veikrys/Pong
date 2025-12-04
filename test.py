import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

blink = True

# Загружаем пиксельный шрифт
try:
    font = pygame.font.Font(".\PressStart2P.ttf", 24)
except:
    font = pygame.font.SysFont("Arial", 24)  # запасной вариант

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.time.get_ticks() % 1000 < 100:  # каждые 0.1 сек
        blink = not blink

    screen.fill((0, 0, 0))  # тёмно‑синий фон
    
    # Рисуем текст
    text = font.render("ARCADE GAME", True, (255, 255, 0))
    screen.blit(text, (250, 100))

    # Основной текст
    text_main = font.render("1UP", True, (255, 255, 0))
    # Обводка (смещаем и рисуем другим цветом)
    text_outline = font.render("1UP", True, (0, 0, 255))
    if blink:
        screen.blit(text_outline, (102, 102))  # чуть ниже и правее
        screen.blit(text_main, (100, 100))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()