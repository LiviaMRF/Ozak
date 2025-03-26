import pygame
from entities.bullet import Bullet


def shoot(self, mouse_pos):
    if self.cooldown <= 0:
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            bullet = Bullet(self.rect.center, direction.normalize())
            self.cooldown = 0.2  # Valor fixo
            return bullet
    return None