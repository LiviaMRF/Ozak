import pygame
from settings import *

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, target_scene):
        super().__init__()
        self.image = pygame.Surface((60, 100))  # Tamanho da porta
        self.image.fill((150, 75, 0))  # Cor marrom para a porta
        self.target_scene = target_scene  # Cena destino
        self.interaction_radius = 70  # Distância para interagir

        self.rect = self.image.get_rect(topleft=pos)

