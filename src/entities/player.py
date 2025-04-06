from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.power import Power
from entities.character import Character


class Player(Character):
    def __init__(self, screen_pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), real_pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        super().__init__()

       # Carrega sprites
        self.idle_frames = [load_sprite("player/ozak_dead.png"),]
        self.moving_frames = [load_sprite(f"player/ozak_dead.png"),]
        self.moving_animation = Animation(self.moving_frames, speed=0.15)  # Velocidade da animação
        self.idle_animation = Animation(self.moving_frames, speed=0.15)  # Velocidade da animação

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
        self.max_cooldown=0.2
        self.cooldown = 0  

        # Sistema dos poderes
        self.current_power = Power("brown", 500, 10) # Poder inicial
        self.power_offset = pygame.math.Vector2(30, 0) # Posição relativa ao personagem

        # Atributos de movimento
        self.speed = 300
        self.direction = pygame.math.Vector2()

        # Sistema de vida
        self.health = 100
        self.is_dead = False

        # Sistema de estamina (barra azul do GDD)
        self.stamina = StaminaComponent(max_stamina=100, drain_rate=20, recover_rate=15)

        # Estado
        self.run_speed_multiplier = 1.8  # Velocidade ao correr
        self.base_speed = 300  # Velocidade normal
        self.is_running = False
        self.is_moving = False

    def update(self, dt):
        if self.health < 0:
            self.is_dead=True
            return 

        # Atualiza o estado da animação
        if  self.is_running and self.direction.magnitude() > 0:
            self.moving_animation.update(dt)
            self.current_sprite = self.moving_animation.current_image()
        else:
            self.idle_animation.update(dt)
            self.current_sprite = self.idle_animation.current_image()

        # Atualiza lógica
        self._handle_input()
        self.stamina.update(dt, self.is_running)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_power_position(pygame.mouse.get_pos())

    def _handle_input(self):


        keys = pygame.key.get_pressed()

        # Movimento básico (WASD)
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.is_moving = self.direction.magnitude() > 0

        # Normaliza diagonal
        if self.is_moving:
            self.direction = self.direction.normalize()

        # Corrida (Shift esquerdo) - Só corre se tiver estamina
        self.is_running = (keys[pygame.K_LSHIFT] or pygame.mouse.get_pressed()[2]) and (not self.stamina.is_exhausted) and self.is_moving

    def player_shift(self, dt):
        if self.stamina.is_exhausted:
            speed = self.base_speed * 0.7
        else: speed = self.base_speed * (self.run_speed_multiplier if self.is_running else 1)

        # Não corre se acabar a estamina
        if not self.stamina.is_exhausted or not self.is_running:
            
            shift_x=self.direction.x * speed * dt
            #if   -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_pos[0]+shift_x \
            #    or self.real_pos[0]+ shift_x + self.rect.width > (MAP_SCALE+1)*SCREEN_WIDTH/2:

            if   -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_rect.left+shift_x \
                or self.real_rect.right+ shift_x > (MAP_SCALE+1)*SCREEN_WIDTH/2:

                shift_x = 0

            shift_y = self.direction.y * speed * dt
            #if   -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_pos[1]+shift_y \
            #    or self.real_pos[1]+ shift_y + self.rect.height> (MAP_SCALE+1)*SCREEN_HEIGHT/2:

            if   -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_rect.top+shift_y \
                or self.real_rect.bottom+ shift_y > (MAP_SCALE+1)*SCREEN_HEIGHT/2:

                shift_y=0
        
            self.real_rect.x += shift_x
            self.real_rect.y += shift_y
            return (shift_x, shift_y)
        
        return (0,0)