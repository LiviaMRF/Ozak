import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, pos_shifted, direction, speed=500, damage=10):
        super().__init__()

        # Carrega a imagem da bala
        self.image = load_sprite("bullets/basic.png", scale=0.5)
        self.rect = self.image.get_rect(center=pos)
        self.pos_without_shift = pos_shifted.copy()

        # Direção e movimento
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = damage

    def update(self, dt):
        self.rect.x += self.direction[0]*self.speed * dt 
        self.rect.y += self.direction[1]*self.speed * dt
        self.pos_without_shift[0] += self.direction[0]*self.speed * dt 
        self.pos_without_shift[1] += self.direction[1]*self.speed * dt
        print(self.pos_without_shift)

        # Remove se sair da tela
        if -(GAME_CLOUD_SIZE-1)*SCREEN_WIDTH/2 > self.pos_without_shift[0]\
                or self.pos_without_shift[0] > (GAME_CLOUD_SIZE+1)*SCREEN_WIDTH/2\
                or  -(GAME_CLOUD_SIZE-1)*SCREEN_HEIGHT/2 > self.pos_without_shift[1] \
                or self.pos_without_shift[1]> (GAME_CLOUD_SIZE+1)*SCREEN_HEIGHT/2:
                
            self.kill()
