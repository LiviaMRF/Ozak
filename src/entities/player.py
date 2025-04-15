from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.power import Power
from entities.character import Character

class Player(Character):
    def __init__(self, max_stamina = 100, drain_rate = 10, recover_rate = 15, run_speed_multiplier = 1.8, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sistema de estamina (barra azul do GDD)
        self.stamina = StaminaComponent(max_stamina, drain_rate, recover_rate)

        # Estado de movimento
        self.run_speed_multiplier = run_speed_multiplier # Velocidade ao correr
        self.is_running = False
        self.is_moving = False

        # Animação de corrida
        self.running_animation = Animation(self.moving_frames, self.moving_animation_speed/2)  


    def update(self, dt):
        if self.is_dead:
            return

        # Atualiza o estado da animação
        if  self.is_running:
            self.running_animation.update(dt)
            self.image = self.running_animation.current_image()
        elif self.is_moving:
            self.moving_animation.update(dt)
            self.image = self.moving_animation.current_image()
        else:
            self.idle_animation.update(dt)
            self.image = self.idle_animation.current_image()

        # Atualiza movimento com input
        self._handle_input()
        self.stamina.update(dt, self.is_running)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_angular_position(pygame.mouse.get_pos())

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
            self.speed = self.base_speed * 0.7
        else: self.speed = self.base_speed * (self.run_speed_multiplier if self.is_running else 1)

        # Não corre se acabar a estamina
        if not self.stamina.is_exhausted or not self.is_running:
            
            shift_x = self.direction.x * self.speed * dt

            if   -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_rect.left+shift_x \
                or self.real_rect.right+ shift_x > (MAP_SCALE+1)*SCREEN_WIDTH/2:

                shift_x = 0

            shift_y = self.direction.y * self.speed * dt
        
            if   -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_rect.top+shift_y \
                or self.real_rect.bottom+ shift_y > (MAP_SCALE+1)*SCREEN_HEIGHT/2:

                shift_y=0
        
            self.real_rect.x += shift_x
            self.real_rect.y += shift_y
            return (shift_x, shift_y)
        
        return (0,0)

    def lose_health_points(self, damage):
        # Chama o método da classe pai para reduzir a vida
        super().lose_health_points(damage)

        # Verifica se o jogador ainda está vivo após perder vida
        if self.health <= 0:
            self.health = 0  # Evita valores negativos
            self.is_dead = True

        # Efeito sonoro de dano
        sound_path = os.path.join("..", "assets", "music", "damage-sound.mp3")
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(0.1)
        sound.play(loops=0)

