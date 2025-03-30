from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.power import Power, PowerBall


class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        super().__init__()

        # Carrega sprites
        self.idle_sprite = load_sprite("player/ozak_dead.png")
        self.run_frames = [load_sprite(f"player/ozak_dead.png"),]
        self.run_animation = Animation(self.run_frames, speed=0.15)  # Velocidade da animação


        # Configuração inicial
        self.image = self.idle_sprite
        self.rect = self.image.get_rect(center=pos)
        self.real_pos = list(self.rect.topleft)

        # Sistema de animação
        self.current_animation = None
        self.current_sprite = None

        # Configuração inicial
        self.animation_speed = 0.15
        self.current_frame = 0
        self.cooldown = 0  #cooldown para poder atirar

        # Sistema dos poderes
        self.current_power = Power() # Poder inicial
        self.power_offset = pygame.math.Vector2(30, 0) # Posição relativa ao personagem

        # Atributos de movimento
        self.speed = 300
        self.direction = pygame.math.Vector2()

        # Sistema de estamina (barra azul do GDD)
        self.stamina = StaminaComponent(max_stamina=100, drain_rate=20, recover_rate=15)
        self.health = 100

        # Estado
        self.run_speed_multiplier = 1.8  # Velocidade ao correr
        self.base_speed = 300  # Velocidade normal
        self.is_running = False


    def update(self, dt):
        # Atualiza o estado da animação
        if self.is_running and self.direction.magnitude() > 0:
            self.run_animation.update(dt)
            self.current_sprite = self.run_animation.current_image()
        else:
            self.current_sprite = self.idle_sprite

        # Atualiza lógica
        self._handle_input()
        self.stamina.update(dt, self.is_running)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza arma
        if self.current_power.image:
            self._update_power_position()

    def _handle_input(self):
        keys = pygame.key.get_pressed()

        # Movimento básico (WASD)
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        is_moving = self.direction.magnitude() > 0

        # Normaliza diagonal
        if is_moving:
            self.direction = self.direction.normalize()

        # Corrida (Shift esquerdo) - Só corre se tiver estamina
        self.is_running = (keys[pygame.K_LSHIFT] or pygame.mouse.get_pressed()[2]) and (not self.stamina.is_exhausted) and is_moving

    def player_shift(self, dt):
        if self.stamina.is_exhausted:
            speed = self.base_speed * 0.7
        else: speed = self.base_speed * (self.run_speed_multiplier if self.is_running else 1)

        # Não corre se acabar a estamina
        if not self.stamina.is_exhausted or not self.is_running:
            
            shift_x=self.direction.x * speed * dt
            if   -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_pos[0]+shift_x \
                or self.real_pos[0]+ shift_x + self.rect.width > (MAP_SCALE+1)*SCREEN_WIDTH/2:

                shift_x=0

            shift_y = self.direction.y * speed * dt
            if   -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_pos[1]+shift_y \
                or self.real_pos[1]+ shift_y + self.rect.height> (MAP_SCALE+1)*SCREEN_HEIGHT/2:
                
                shift_y=0
        
            self.real_pos[0] += shift_x
            self.real_pos[1] += shift_y
            return (shift_x, shift_y)
        
        return (0,0)

    def unleash_power(self, mouse_pos):
        if self.cooldown <= 0 and self.current_power.image:
            direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                # Posição do cano da arma
                power_ball_pos = self.rect.center + self.power_offset.rotate(-direction.angle_to((1, 0)))
                real_power_ball_pos = self.real_pos + self.power_offset.rotate(-direction.angle_to((1, 0)))
                power_ball = PowerBall(self.current_power.power_type, power_ball_pos, real_power_ball_pos, direction)
                self.cooldown = 0.2
                return power_ball
        return None

    def _update_power_position(self):
        # Obtém a posição do cursor do mouse
        mouse_pos = pygame.mouse.get_pos()

        # Calcula a direção do jogador até o cursor
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)

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
