from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        super().__init__()

        run_frames = [load_sprite(f"player/run_{i}.png") for i in range(4)]
        self.run_animation = Animation(run_frames, speed=0.1)

        # Carrega sprites
        self.idle_sprite = load_sprite("player/ozak_idle.png")
        self.weapon_anchor = pygame.math.Vector2(15, 5)  # Ponto de fixação da arma

        # Configuração inicial
        self.image = self.idle_sprite
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.15
        self.current_frame = 0
        self.cooldown = 0

        self.current_weapon = "pistol"
        self.weapons = ["pistol"]

        # Configuração de sprites
        self.original_idle = load_sprite("player/ozak_idle.png")
        self.original_run_frames = [load_sprite(f"player/run_{i}.png") for i in range(4)]
        self.run_animation = Animation(self.original_run_frames, speed=0.1)

        # Imagem base atual
        self.base_image = self.original_idle
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=pos)

        # Sistema de armas
        self.weapon_image = None
        self.weapon_offset = pygame.math.Vector2(25, -10)
        self.load_weapon("pistol")

        # Atributos de movimento
        self.speed = 300
        self.direction = pygame.math.Vector2()
        #self.width = 1000
        #self.height = 100
        #self.x = 0
        #self.y = 0

        # Sistema de estamina (barra azul do GDD)
        self.stamina = StaminaComponent(max_stamina=100, drain_rate=20, recover_rate=15)

        # Estado
        self.run_speed_multiplier = 1.8  # Velocidade ao correr
        self.base_speed = 300  # Velocidade normal
        self.is_running = False

        self.weapon_image = None  # Sprite da arma
        self.weapon_offset = pygame.math.Vector2(25, -10)  # Posição relativa ao personagem
        self.load_weapon("pistol")  # Arma inicial

        self.health = 100

        self.weapon_cooldowns = {
            'pistol': 0.2,
            'shotgun': 0.8,
            'rifle': 0.15
        }


    def load_weapon(self, weapon_type):
        # Carrega a sprite da arma equipada
        self.weapon_image = load_sprite(f"weapons/{weapon_type}_hand.png")

    def update(self, dt):
        # Atualiza animação
        if self.direction.magnitude() > 0:
            self.run_animation.update(dt)
            self.base_image = self.run_animation.current_image()
        else:
            self.base_image = self.original_idle

        # Atualiza lógica
        self._handle_input()
        self._move(dt)
        self.stamina.update(dt, self.is_running)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza arma
        if self.weapon_image:
            self._update_weapon_position()


    def _handle_input(self):
        keys = pygame.key.get_pressed()

        # Movimento básico (WASD)
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        # Normaliza diagonal
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

            # Corrida (Shift esquerdo) - Só corre se tiver estamina
        self.is_running = (keys[pygame.K_LSHIFT] or pygame.mouse.get_pressed()[2]) and not self.stamina.is_exhausted

    def _move(self, dt):
        if self.stamina.is_exhausted:
            speed = self.base_speed * 0.7
        else: speed = self.base_speed * (self.run_speed_multiplier if self.is_running else 1)

        # Não corre se acabar a estamina
        if not self.stamina.is_exhausted or not self.is_running:
            self.rect.x += self.direction.x * speed * dt
            self.rect.y += self.direction.y * speed * dt

        # Limites da tela
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.h, self.rect.y))

    def shoot(self, mouse_pos):
        if self.cooldown <= 0 and self.weapon_image:
            direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                # Posição do cano da arma
                barrel_pos = self.rect.center + self.weapon_offset.rotate(-direction.angle_to((1, 0)))
                bullet = Bullet(barrel_pos, direction)
                self.cooldown = 0.2
                return bullet
        return None

    def _update_weapon_position(self):
        # Obtém a posição do cursor do mouse
        mouse_pos = pygame.mouse.get_pos()

        # Calcula a direção do jogador até o cursor
        direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)

        if direction.length() > 0:
            direction = direction.normalize()

        # Rotaciona a imagem da arma conforme o ângulo da direção
        angle = -direction.angle_to(pygame.math.Vector2(1, 0))  # Calcula o ângulo correto

        # Define ponto de fixação (ajuste esses valores)
        pivot_offset = pygame.math.Vector2(100, 0)  # Relativo ao centro do player
        weapon_center = self.rect.center + pivot_offset

        # Ajusta a posição da arma em relação ao jogador
        rotated_offset = self.weapon_offset.rotate(angle)  # Aplica rotação ao offset
        weapon_pos = pygame.math.Vector2(weapon_center) + rotated_offset

        # Atualiza a posição e a rotação da arma
        self.weapon_image = pygame.transform.rotate(load_sprite(f"weapons/{self.current_weapon}_hand.png"), angle)
        self.weapon_rect = self.weapon_image.get_rect(center=weapon_pos)
