import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=500, damage=10):
        super().__init__()

        # Carrega a imagem da bala
        self.image = load_sprite("bullets/basic.png", scale=0.5)
        self.rect = self.image.get_rect(center=pos)

        # Direção e movimento
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = damage

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        # Remove se sair da tela
        if not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT):
            self.kill()
