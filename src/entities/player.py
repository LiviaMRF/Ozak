from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.power import Power
from entities.character import Character

class Player(Character):
    def __init__(self, max_stamina=100, drain_rate=20, recover_rate=15, run_speed_multiplier = 1.8, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sistema de estamina (barra azul do GDD)
        self.stamina = StaminaComponent(max_stamina, drain_rate, recover_rate)

        # Estado de movimento
        self.run_speed_multiplier = run_speed_multiplier # Velocidade ao correr
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

        # Atualiza movimento com input
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
    

