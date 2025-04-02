import pygame
from settings import *

class Power(pygame.sprite.Sprite):
    def __init__(self, power_type="pink", pos=(0,0)):
        super().__init__()
        self.power_type=power_type
        # Carrega a imagem da poder
        self.image = load_sprite(f"powers/{power_type}.png", scale=0.3)
        self.rect = self.image.get_rect(center=pos)

class PowerBall(Power):

    def __init__(self, power_type, power_ball_pos, real_power_ball_pos, direction, speed=500, damage=10):
        super().__init__(power_type, power_ball_pos)

        self.real_power_ball_pos = list(real_power_ball_pos)
        # Direção e movimento
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = damage


    def update(self, dt):
        self.rect.x += self.direction[0]*self.speed * dt 
        self.rect.y += self.direction[1]*self.speed * dt
        self.real_power_ball_pos[0] += self.direction[0]*self.speed * dt 
        self.real_power_ball_pos[1] += self.direction[1]*self.speed * dt

        # Remove se sair da tela
        if -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_power_ball_pos[0]\
                or self.real_power_ball_pos[0] > (MAP_SCALE+1)*SCREEN_WIDTH/2\
                or  -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_power_ball_pos[1] \
                or self.real_power_ball_pos[1]> (MAP_SCALE+1)*SCREEN_HEIGHT/2:
                
            self.kill()