from components.animation import *
from settings import *
from entities.power import Power, PowerBall
from entities.character import Character
import random

class AlterEgo(Character):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria referência ao personagem Ozak
        self.player = player
        self.cooldown=0.0002
        self.auto_timer=0
        self.random_speed_buffer=[0, 0]
        self.direction_sense=random.sample((-1, 1), k=1)[0]



    def update(self, dt):

        if self.health<0:
            self.kill()
        
        # Atualiza o estado da animação
        self.moving_animation.update(dt)
        self.image = self.moving_animation.current_image()

        self._move_alter_ego(dt)

        # Atualiza cooldown
        self.cooldown = max(0, self.cooldown - dt)

        # Atualiza posição do poder
        self._update_angular_position(PLAYER_POSITION)

    def unleash_power(self, obj_pos):
        if self.cooldown <= 0 and self.current_power.image:
            direction = pygame.math.Vector2(obj_pos) - pygame.math.Vector2(self.rect.center)
            if direction.length() > 0:
                random_angle=25*random.uniform(-1, 1)
                # Posição do cano da arma
                power_ball_pos = self.rect.center + self.power_offset.rotate(-direction.angle_to((1, 0)))
                real_power_ball_pos = self.real_rect.center + self.power_offset.rotate(-direction.angle_to((1, 0)))
                
                #add random angle to soon-to-be-shot ball
                direction=direction.rotate(random_angle)

                power_ball = PowerBall(self.current_power, power_ball_pos, real_power_ball_pos, direction)
    
                self.cooldown = self.max_cooldown
                return power_ball
        return None

    def _move_alter_ego(self, dt):

        '''# Movimento básico do alterego
        D=70.01
        self.auto_timer+=dt;
        # Movimento básico do médico
        self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        self.direction.y = self.player.rect.center[1] - self.rect.center[1]
        direction=self.direction.magnitude()

        if(direction-1.5*D < 0):

            self.random_speed_buffer=-self.speed*self.direction.normalize()
            self.direction=-self.direction.normalize()

        else:
            self.direction=self.direction*( (direction-D)/direction )
            self.direction = self.direction*0.15 + pygame.math.Vector2(-self.direction.y, self.direction.x)*self.direction_sense

        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()

        self._move_if_valid(dt)'''
        self.auto_timer+=dt
        if(self.auto_timer < 5):
            return

        self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        self.direction.y = self.player.rect.center[1] - self.rect.center[1]
        D=250
        
        if(self.direction.magnitude() < D):
            self.auto_timer=0
            return
        
        if self.direction.magnitude()>0:
            self.direction = self.direction.normalize()
        
        self._move_if_valid(dt)

    def _move_if_valid(self, dt):
        '''intervalo_tempo=0.5
        if(self.auto_timer > intervalo_tempo):#refinemos essa constante 1
            self.auto_timer=0
            self.direction_sense=random.sample((-1, 1), k=1)[0]
            #self.random_speed_buffer_current=self.random_speed_buffer_next
            #precisamos afinar essa constante v_random
            v_rand=self.speed*1
            x_rand=random.uniform(-1, 1)#escolhemos 2 floats aleatorios entre -1 e 1
            y_rand=random.uniform(-1, 1)

            #vamos normalizar o vetor (x_rand, y_rand)
            norma= pow(x_rand*x_rand + y_rand*y_rand, 0.5)
            x_rand=x_rand/norma
            y_rand=y_rand/norma
            self.random_speed_buffer[0]=x_rand*v_rand
            self.random_speed_buffer[1]=y_rand*v_rand'''


        shift_x = (self.direction.x*self.speed +self.random_speed_buffer[0]*0)*dt
        shift_y = (self.direction.y*self.speed +self.random_speed_buffer[1]*0)*dt

        if  -(MAP_SCALE-1)*SCREEN_WIDTH/2 <= self.real_rect.left+shift_x and self.real_rect.right+shift_x <= (MAP_SCALE+1)*SCREEN_WIDTH/2 :
            self.real_rect.x += shift_x
            self.rect.x += shift_x

        if (-(MAP_SCALE-1)*SCREEN_HEIGHT/2 <= self.real_rect.top+shift_y and self.real_rect.bottom+shift_y<= (MAP_SCALE+1)*SCREEN_HEIGHT/2):
            self.real_rect.y += shift_y
            self.rect.y += shift_y




        #self.direction.x = self.player.rect.center[0] - self.rect.center[0]
        #self.direction.y = self.player.rect.center[1] - self.rect.center[1]
        #
        #if self.direction.magnitude()>0:
        #    self.direction = self.direction.normalize()
        #
        #self._move_if_valid(dt)
