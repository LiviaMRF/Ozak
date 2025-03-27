from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        super().__init__()

        # Carrega sprites
        self.idle_sprite = load_sprite("player/ozak_idle.png")
        self.run_frames = [load_sprite(f"player/ozak_run_1.png"),]
        self.run_animation = Animation(self.run_frames, speed=0.15)  # Velocidade da animação


        self.weapon_anchor = pygame.math.Vector2(15, 5)  # Ponto de fixação da arma

        # Configuração inicial
        self.image = self.idle_sprite
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.rect_shifted = self.rect.copy()

        # Sistema de animação
        self.current_animation = None
        self.current_sprite = None

        # Configuração inicial
        self.animation_speed = 0.15
        self.current_frame = 0
        self.cooldown = 0  #cooldown para poder atirar


        self.current_weapon = "pistol"
        self.weapons = ["pistol"]


        # Sistema de armas
        self.weapon_image = None
        self.weapon_offset = pygame.math.Vector2(25, -10)
        self.load_weapon("pistol")

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

        self.weapon_image = None  # Sprite da arma
        self.weapon_offset = pygame.math.Vector2(25, -10)  # Posição relativa ao personagem
        self.load_weapon("pistol")  # Arma inicial


    def load_weapon(self, weapon_type):
        # Carrega a sprite da arma equipada
        self.weapon_image = load_sprite(f"weapons/{weapon_type}_hand.png")

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

    def player_shift(self, dt):
        if self.stamina.is_exhausted:
            speed = self.base_speed * 0.7
        else: speed = self.base_speed * (self.run_speed_multiplier if self.is_running else 1)

        # Não corre se acabar a estamina
        if not self.stamina.is_exhausted or not self.is_running:
            self.rect_shifted.move((self.direction.x * speed * dt, self.direction.y * speed * dt))
            return (self.direction.x * speed * dt, self.direction.y * speed * dt)
        return (0,0)

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
