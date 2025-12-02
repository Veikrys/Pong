
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
FPS = 60
clock = pygame.time.Clock()

#игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    screen.fill(BLACK)
    pygame.display.update()
    clock.tick(FPS)
