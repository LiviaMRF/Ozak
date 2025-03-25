import pygame
from settings import *

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ozak")

# Cores
WHITE = (255, 255, 255)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preenche a tela com branco (como o quarto do jogo)
    screen.fill(WHITE)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()