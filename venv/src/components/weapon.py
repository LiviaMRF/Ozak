import pygame

from entities.bullet import Bullet


def shoot(self, mouse_pos):
    """Cria um novo projétil na direção do mouse"""
    if self.cooldown <= 0 and self.weapon_image:  # Verifica cooldown e se há arma equipada
        # Calcula direção do mouse
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)

        if direction.length() > 0:  # Evita divisão por zero
            direction = direction.normalize()

            # Calcula posição do cano (offset da arma)
            angle = direction.angle_to(pygame.math.Vector2(1, 0))
            barrel_offset = self.weapon_offset.rotate(-angle)
            spawn_pos = self.rect.center + barrel_offset

            # Cria a bala com tipo da arma atual (se seu sistema tiver tipos)
            bullet = Bullet(
                pos=spawn_pos,
                direction=direction,
                bullet_type=getattr(self, 'current_weapon', 'basic')  # Usa 'basic' se não houver tipo
            )

            # Configura cooldown baseado na arma
            self.cooldown = getattr(self, 'weapon_cooldowns', {}).get(self.current_weapon, 0.2)

            return bullet

    return None