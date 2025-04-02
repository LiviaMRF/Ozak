from components.animation import *
from settings import *
from entities.power import Power, PowerBall


class Character(pygame.sprite.Sprite):
    def __init__(self, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        super().__init__()

        # Carrega sprites
        self.idle_frames = [load_sprite("player/ozak_dead.png"),]
        self.moving_frames = [load_sprite(f"player/ozak_dead.png"),]
        self.moving_animation = Animation(self.moving_frames, speed=0.15)  # Velocidade da animação
        self.idle_animation = Animation(self.moving_frames, speed=0.15)  # Velocidade da animação

        # Configuração inicial
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=pos)

        # Sistema de animação
        self.current_animation = None
        self.current_sprite = None
        self.animation_speed = 0.15
        self.current_frame = 0

        # Cooldown para poder lançar poder
        self.cooldown = 0  

        # Sistema dos poderes
        self.current_power = Power() # Poder inicial
        self.power_offset = pygame.math.Vector2(30, 0) # Posição relativa ao personagem

        # Atributos de movimento
        self.speed = 300
        self.direction = pygame.math.Vector2()

        # Sistema de vida
        self.health = 100


    def update(self, dt):
        # Atualiza o estado da animação
        if  self.direction.magnitude() > 0:
            self.moving_animation.update(dt)
            self.current_sprite = self.moving_animation.current_image()
        else:
            self.idle_animation.update(dt)
            self.current_sprite = self.idle_animation.current_image()

        # Atualiza cooldown
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        if self.current_power.image:
            self._update_power_position()

    def unleash_power(self, obj_pos):
        if self.cooldown <= 0 and self.current_power.image:
            direction = pygame.math.Vector2(obj_pos) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                # Posição do cano da arma
                power_ball_pos = self.rect.center + self.power_offset.rotate(-direction.angle_to((1, 0)))
                real_power_ball_pos = self.real_pos + self.power_offset.rotate(-direction.angle_to((1, 0)))
                power_ball = PowerBall(self.current_power.power_type, power_ball_pos, real_power_ball_pos, direction)
                self.cooldown = 0.2
                return power_ball
        return None

    def _update_power_position(self, target_pos):
        # Calcula a direção do character até o cursor
        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(self.rect.center)

        if direction.length() > 0:
            direction = direction.normalize()

        # Rotaciona a imagem da arma conforme o ângulo da direção
        angle = -direction.angle_to(pygame.math.Vector2(1, 0))  # Calcula o ângulo correto

        # Define ponto de fixação (ajuste esses valores)
        pivot_offset = pygame.math.Vector2(0, 0)  # Relativo ao centro do player
        power_center = self.rect.center + pivot_offset

        # Ajusta a posição da arma em relação ao jogador
        rotated_offset = self.power_offset.rotate(angle)  # Aplica rotação ao offset
        power_pos = pygame.math.Vector2(power_center) + rotated_offset

        # Atualiza a posição e a rotação da arma
        self.current_power.image = pygame.transform.rotate(load_sprite(f"powers\{self.current_power.power_type}.png", scale=0.3), angle)
        self.current_power.rect = self.current_power.image.get_rect(center=power_pos)
