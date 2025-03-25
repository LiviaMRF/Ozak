import pygame

from entities.bullet import Bullet


def shoot(self, mouse_pos):
    if self.cooldown <= 0 and self.weapon_image:
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            # Posição do cano da arma
            barrel_pos = self.rect.center + self.weapon_offset.rotate(-direction.angle_to((1, 0)))
            bullet = Bullet(barrel_pos, direction)
            self.cooldown = 0.2
            return bullet
    return None