import pygame

from settings import load_sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type="doctor"):
        super().__init__()
        self.image = load_sprite(f"enemies/{enemy_type}_1.png")
        self.rect = self.image.get_rect()