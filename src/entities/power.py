import pygame
from settings import *

class Power(pygame.sprite.Sprite):
    def __init__(self, power_type="pink", speed=500, damage=10):
        super().__init__()
        self.power_type=power_type
        self.speed = speed
        self.damage = damage

        # Carrega a imagem da poder
        self.image = load_sprite(f"powers/{power_type}.png", scale=0.3)
        self.rect = self.image.get_rect(center=(0,0))

class PowerBall(Power):

    def __init__(self, power, screen_pos, real_pos, direction):
        super().__init__(power.power_type, power.speed, power.damage)

        self.rect = self.image.get_rect(center=screen_pos)
        self.real_rect = self.image.get_rect(center=real_pos)

        # Direção e movimento
        self.direction = direction.normalize()
        

    def update(self, dt):
        self.rect.x += self.direction[0]*self.speed * dt 
        self.rect.y += self.direction[1]*self.speed * dt
        self.real_rect.x += self.direction[0]*self.speed * dt 
        self.real_rect.y += self.direction[1]*self.speed * dt 

        
        if -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_rect.left\
                or self.real_rect.right > (MAP_SCALE+1)*SCREEN_WIDTH/2\
                or  -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_rect.top \
               or self.real_rect.bottom> (MAP_SCALE+1)*SCREEN_HEIGHT/2:


            self.kill()