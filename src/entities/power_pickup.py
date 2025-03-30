import pygame
from settings import load_sprite
from entities.power import *

class PowerPickup(pygame.sprite.Sprite):
    def __init__(self, pos, power_type="pink"):
        super().__init__()
        self.power_type = power_type
        self.image = load_sprite(f"powers\{power_type}.png")
        self.rect = self.image.get_rect(center=pos)
        self.interaction_radius = 50  # Distância para coleta

    def can_be_picked(self, player_pos):
        #Verifica se o jogador está dentro do raio de coleta
        return pygame.math.Vector2(self.rect.center).distance_to(player_pos) <= self.interaction_radius