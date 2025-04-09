from components.animation import *
from settings import *
from entities.character import Character
from entities.power import Power
import random


class Medico(Character):
    def __init__(self, player, ratio_radial_to_tangential_speed = 0.15, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria referência ao personagem Ozak
        self.player = player
        
        # Cria variáveis de movivento
        self.ratio_radial_to_tangential_speed = ratio_radial_to_tangential_speed

        
    def _move_if_valid(self, dt):
        #precisamos afinar essa constante v_random
        v_rand=self.speed*3
        x_rand=random.uniform(-1, 1)#escolhemos 2 floats aleatorios entre -1 e 1
        y_rand=random.uniform(-1, 1)

        #vamos normalizar o vetor (x_rand, y_rand)
        norma= pow(x_rand*x_rand + y_rand*y_rand, 0.5)
        x_rand=x_rand/norma
        y_rand=y_rand/norma

        shift_x = (self.direction.x*self.speed +x_rand*v_rand)*dt#Assim está muito ruim, precisamos aumentar o intervalo entre os sorteios
        shift_y = (self.direction.y*self.speed +y_rand*v_rand)*dt

        if  -(MAP_SCALE-1)*SCREEN_WIDTH/2 <= self.real_rect.left+shift_x and self.real_rect.right+shift_x <= (MAP_SCALE+1)*SCREEN_WIDTH/2 :
            self.real_rect.x += shift_x
            self.rect.x += shift_x

        if (-(MAP_SCALE-1)*SCREEN_HEIGHT/2 <= self.real_rect.top+shift_y and self.real_rect.bottom+shift_y<= (MAP_SCALE+1)*SCREEN_HEIGHT/2):
            self.real_rect.y += shift_y
            self.rect.y += shift_y

    def _move_medico(self, dt):

        # Movimento básico do médico
        self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        self.direction.y = self.player.rect.center[1] - self.rect.center[1]

        self.direction = self.direction*self.ratio_radial_to_tangential_speed + pygame.math.Vector2(-self.direction.y, self.direction.x)
        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        self._move_if_valid(dt)

        
    def update(self, dt):
        
        if self.health<0:
            self.kill()

        # Atualiza o estado da animação
        self.moving_animation.update(dt)
        self.image = self.moving_animation.current_image()

        # Atualiza dooldown e move o médico
        self._move_medico(dt)
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_angular_position(PLAYER_POSITION)

