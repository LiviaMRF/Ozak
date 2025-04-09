from components.animation import *
from settings import *
from entities.power import Power
from entities.character import Character

class AlterEgo(Character):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria referência ao personagem Ozak
        self.player = player


    def update(self, dt):

        if self.health<0:
            self.kill()
        
        # Atualiza o estado da animação
        self.moving_animation.update(dt)
        self.current_sprite = self.moving_animation.current_image()

        self._move_alter_ego(dt)

        # Atualiza cooldown
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_power_position(PLAYER_POSITION)


    def _move_alter_ego(self, dt):

        # Movimento básico do alterego
        self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        self.direction.y = self.player.rect.center[1] - self.rect.center[1]

        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        self._move_if_valid(dt)