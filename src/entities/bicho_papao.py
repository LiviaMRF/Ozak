from components.animation import *
from settings import *
from entities.character import Character
from entities.power import Power


class BichoPapao(Character):
    def __init__(self, player, idle_time=3, running_time=2, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria referência ao personagem Ozak
        self.player = player
        
        # Atributos extras de movimento
        self.auto_timer = 0
        self.idle_time = idle_time
        self.running_time = running_time
        self.is_running = False
        self.direction = pygame.math.Vector2()
        

    def _update_moving(self, dt):
        self.auto_timer += dt
        if self.is_running and self.auto_timer > self.running_time:
            self.is_running=False
            self.auto_timer=0
        if not self.is_running and self.auto_timer > self.idle_time:
            self.is_running=True
            self.auto_timer=0
    
    def _move_bicho_papao(self, dt):

        self._update_moving(dt)

        if self.is_running:

            # Movimento básico do inimigo
            self.direction.x = self.player.rect.center[0] - self.rect.center[0]
            self.direction.y = self.player.rect.center[1] - self.rect.center[1]

            if self.direction.magnitude()>0:
                self.direction = self.direction.normalize()

            self._move_if_valid(dt)
        
    def update(self, dt):
        
        if self.health<0:
            self.kill()

        # Atualiza o estado da animação
        if  self.is_running:
            self.moving_animation.update(dt)
            self.current_sprite = self.moving_animation.current_image()
        else:
            self.idle_animation.update(dt)
            self.current_sprite = self.idle_animation.current_image()

        # Atualiza lógica
        self._move_bicho_papao(dt)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_power_position(PLAYER_POSITION)




