from components.animation import *
from settings import *
from entities.character import Character
from entities.power import Power

class BichoPapao(Character):
    def __init__(self, screen_pos, real_pos, player):
        super().__init__()

        # Cria referência ao personagem Ozak
        self.player = player

       # Carrega sprites
        self.idle_frames = [load_sprite(f"enemies/doctor_0.png"),]
        self.moving_frames = [load_sprite(f"enemies/doctor_0.png"),]
        self.moving_animation = Animation(self.moving_frames, speed=0.20)  # Velocidade da animação
        self.idle_animation = Animation(self.moving_frames, speed=0.10)  # Velocidade da animação

        # Configuração inicial
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=screen_pos)
        self.real_rect = self.image.get_rect(center=real_pos)


        # Sistema de animação
        self.current_animation = None
        self.current_sprite = None
        self.animation_speed = 0.15
        self.current_frame = 0

        # Cooldown para poder lançar poder
        self.max_cooldown = 15
        self.cooldown = 0  

        # Sistema dos poderes
        self.current_power = Power("brown", 500, 1) # Poder inicial
        self.power_offset = pygame.math.Vector2(30, 0) # Posição relativa ao personagem

        # Atributos de movimento
        self.time = 0
        self.idle_time = 5
        self.running_time = 1
        self.speed = 10
        self.is_running = False
        self.direction = pygame.math.Vector2()
        

        # Sistema de vida
        self.health = 30
        
        
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

    def _update_moving(self, dt):
        self.time += dt
        if self.is_running and self.time > self.running_time:
            self.is_running=False
            self.time=0
        if not self.is_running and self.time > self.idle_time:
            self.is_running=True
            self.time=0
        
    def _move_bicho_papao(self, dt):

        self._update_moving(dt)

        if self.is_running:

            # Movimento básico do inimigo
            self.direction.x = self.player.rect.center[0] - self.rect.center[0]
            self.direction.y = self.player.rect.center[1] - self.rect.center[1]

            if self.direction.magnitude()>0:
                self.direction = self.direction.normalize()

            self._move_if_valid(dt)


