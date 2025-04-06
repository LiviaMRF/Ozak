import pygame
from settings import *


class Boundary(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.rect = pygame.Rect( -(MAP_SCALE-1)*SCREEN_WIDTH/2, -(MAP_SCALE-1)*SCREEN_HEIGHT/2, \
                                    MAP_SCALE*SCREEN_WIDTH, MAP_SCALE*SCREEN_HEIGHT)
        
        self.real_rect = self.rect.copy()

        boundary_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Cor do contorno (vermelho no exemplo, mas você pode escolher qualquer cor)
        border_color = (255, 0, 0, 255)  # RGBA: Vermelho com alpha máximo

        # Desenhar o contorno do Rect na Surface
        # Primeiro criamos um Rect interno que representa a área dentro da borda
        border_width = 2
        inner_rect = self.rect.copy()  # Faz uma cópia
        inner_rect.inflate_ip(-2*border_width, -2*border_width)  # Reduz em ambas as direções

        # Ajustamos as coordenadas porque estamos desenhando na Surface, não na tela
        drawing_rect = pygame.Rect(
            border_width, 
            border_width, 
            self.rect.width - 2*border_width, 
            self.rect.height - 2*border_width
        )


        pygame.draw.rect(boundary_surface, border_color, drawing_rect, border_width)

        self.image = boundary_surface