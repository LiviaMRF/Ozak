import pygame
from settings import load_sprite
from components.weapon import shoot

class WeaponPickup(pygame.sprite.Sprite):
    def __init__(self, pos, weapon_type="pistol"):
        super().__init__()
        self.weapon_type = weapon_type
        self.image = load_sprite(f"weapons/{weapon_type}.png")
        self.rect = self.image.get_rect(center=pos)
        self.interaction_radius = 50  # Distância para coleta

    def can_be_picked(self, player_pos):
        #Verifica se o jogador está dentro do raio de coleta
        return pygame.math.Vector2(self.rect.center).distance_to(player_pos) <= self.interaction_radius