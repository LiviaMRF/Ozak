import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed=200, damage=10):
        super().__init__()

        # Carrega a imagem da bala
        self.image = load_sprite("bullets/basic.png", scale=0.5)
        self.rect = self.image.get_rect(center=pos)
        self.rect_without_shift = self.rect.copy()

        # Direção e movimento
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = damage

    def update(self, dt):
        self.rect.x += self.direction[0]*self.speed * dt 
        self.rect.y += self.direction[1]*self.speed * dt
        self.rect_without_shift.x += self.direction[0]*self.speed * dt 
        self.rect_without_shift.y += self.direction[1]*self.speed * dt

        print(self.rect_without_shift.x - PLAYER_POSITION[0])
        print(self.rect_without_shift.y - PLAYER_POSITION[1])
        # Remove se sair da tela
        if abs(self.rect_without_shift.x - PLAYER_POSITION[0]) > GAME_CLOUD_SIZE*SCREEN_WIDTH/2 or abs(self.rect_without_shift.y - PLAYER_POSITION[1]) > GAME_CLOUD_SIZE*SCREEN_HEIGHT/2:
            self.kill()
