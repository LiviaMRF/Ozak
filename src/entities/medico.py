from components.animation import *
from settings import *
from entities.character import Character
from entities.power import Power


class Medico(Character):
    def __init__(self, player, ratio_radial_to_tangential_speed = 0.15, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria referência ao personagem Ozak
        self.player = player
        
        # Cria variáveis de movivento
        self.ratio_radial_to_tangential_speed = ratio_radial_to_tangential_speed

        
    def _move_medico(self, dt):

        # Movimento básico do médico
        self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        self.direction.y = self.player.rect.center[1] - self.rect.center[1]

        self.direction = self.direction*self.ratio_radial_to_tangential_speed + pygame.math.Vector2(-self.direction.y, self.direction.x)
        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        self._move_if_valid(dt)

        
    def update(self, dt):
        
        if self.health<0:
            self.kill()

        # Atualiza o estado da animação
        self.moving_animation.update(dt)
        self.current_sprite = self.moving_animation.current_image()

        # Atualiza dooldown e move o médico
        self._move_medico(dt)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_power_position(PLAYER_POSITION)

