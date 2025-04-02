from components.animation import *
from settings import *
from entities.power import Power
from entities.character import Character


class AlterEgo(Character):
    def __init__(self, pos, player):
        super().__init__()

        # Cria referência ao personagem Ozak
        self.player = player

       # Carrega sprites
        self.idle_frames = [load_sprite("player/ozak_dead.png", 2.5),]
        self.moving_frames = [load_sprite(f"player/ozak_dead.png", 2.5),]
        self.moving_animation = Animation(self.moving_frames, speed=0.15)  # Velocidade da animação
        self.idle_animation = Animation(self.moving_frames, speed=0.15)  # Velocidade da animação

        # Configuração inicial
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.real_pos = list(self.rect.topleft)

        # Sistema de animação
        self.current_animation = None
        self.current_sprite = None
        self.animation_speed = 0.15
        self.current_frame = 0

        # Cooldown para poder lançar poder
        self.max_cooldown=0.5
        self.cooldown = 0  

        # Sistema dos poderes
        self.current_power = Power("brown", 550, 40) # Poder inicial
        self.power_offset = pygame.math.Vector2(70, 0) # Posição relativa ao personagem

        # Atributos de movimento
        self.speed = 300
        self.direction = pygame.math.Vector2()

        # Sistema de vida
        self.health = 1000

    def update(self, dt):

        # Atualiza o estado da animação
        self.moving_animation.update(dt)
        self.current_sprite = self.moving_animation.current_image()
        
        #self.idle_animation.update(dt)
        #self.current_sprite = self.idle_animation.current_image()

        self._move_alter_ego(dt)

        # Atualiza cooldown
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_power_position(PLAYER_POSITION)

    def _move_alter_ego(self, dt):

        # Movimento básico do inimigo
        self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        self.direction.y = self.player.rect.center[1] - self.rect.center[1]

        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        self._move_if_valid(dt)