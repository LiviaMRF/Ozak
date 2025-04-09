import pygame
from components.animation import *
from settings import *

class Power(pygame.sprite.Sprite):
    def __init__(self, power_type="pink", speed=500, damage=10):
        super().__init__()
        self.power_type=power_type
        self.speed = speed
        self.damage = damage
        self.sprite_scale=0.7

        # Carrega a imagem da poder
        self.image = load_sprite(f"powers{os.sep}power_{power_type}_0.png", scale=self.sprite_scale)
        self.rect = self.image.get_rect(center=(0,0))

class PowerBall(Power):

    def __init__(self, power, screen_pos, real_pos, direction):
        super().__init__(power.power_type, power.speed, power.damage)

        self.rect = self.image.get_rect(center=screen_pos)
        self.real_rect = self.image.get_rect(center=real_pos)
        self.power_ball_frames = [load_sprite(f"powers{os.sep}power_{power.power_type}_{idx}.png", self.sprite_scale) for idx in range (0,2)]
        self.power_ball_animation = Animation(self.power_ball_frames, 0.15)  

        # Direção e movimento
        self.direction = direction.normalize()
        

    def update(self, dt):
        self.rect.x += self.direction[0]*self.speed * dt 
        self.rect.y += self.direction[1]*self.speed * dt
        self.real_rect.x += self.direction[0]*self.speed * dt 
        self.real_rect.y += self.direction[1]*self.speed * dt 

        self.power_ball_animation.update(dt)
        self.image = self.power_ball_animation.current_image()
        
        if -(MAP_SCALE-1)*SCREEN_WIDTH/2 > self.real_rect.left\
                or self.real_rect.right > (MAP_SCALE+1)*SCREEN_WIDTH/2\
                or  -(MAP_SCALE-1)*SCREEN_HEIGHT/2 > self.real_rect.top \
               or self.real_rect.bottom> (MAP_SCALE+1)*SCREEN_HEIGHT/2:


            self.kill()
