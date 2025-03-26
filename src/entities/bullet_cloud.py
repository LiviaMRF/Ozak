from components.animation import *
from settings import *
from components.stamina import StaminaComponent
from entities.bullet import Bullet



class BulletCloud(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        # Configuração inicial
        self.width = GAME_CLOUD_SIZE*SCREEN_WIDTH
        self.height = GAME_CLOUD_SIZE*SCREEN_HEIGHT
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=PLAYER_POSITION)
        
        # Referência ao jogador
        self.player=player
 
    def _move(self, dt):
        if self.player.stamina.is_exhausted:
            speed = self.player.base_speed * 0.7
        else: speed = self.player.base_speed * (self.player.run_speed_multiplier if self.player.is_running else 1)

        # Não corre se acabar a estamina
        if not self.player.stamina.is_exhausted or not self.player.is_running:
            self.rect.x -= self.player.direction.x * speed * dt
            self.rect.y -= self.player.direction.y * speed * dt

        # Limites da tela
        if self.rect.left > PLAYER_POSITION[0]: self.rect.left = PLAYER_POSITION[0]
        elif self.rect.right < PLAYER_POSITION[0]: self.rect.right = PLAYER_POSITION[0]
        
        if self.rect.top<PLAYER_POSITION[1]: self.rect.top=PLAYER_POSITION[1]
        elif self.rect.bottom>PLAYER_POSITION[1]: self.rect.bottom>PLAYER_POSITION[1]
    
    def update(self, dt):
        # Atualiza posição do jogador dentro da bullet_cloud
        self.player._handle_input()
        self._move(dt)


    def _handle_input(self):
        keys = pygame.key.get_pressed()

        # Movimento básico (WASD)
        self.player.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.player.direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        # Normaliza diagonal
        if self.player.direction.magnitude() > 0:
            self.player.direction = self.player.direction.normalize()

            # Corrida (Shift esquerdo) - Só corre se tiver estamina
        self.player.is_running = (keys[pygame.K_LSHIFT] or pygame.mouse.get_pressed()[2]) and not self.player.stamina.is_exhausted

    


    