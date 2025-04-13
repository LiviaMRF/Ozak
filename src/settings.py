import pygame
from pygame.image import load

# Cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

def load_sprite(name, scale=1, convert_alpha=True):
    path = os.path.join(ASSETS_PATH, "images", name)#isso aqui tá fazendo o join com \ ao invés de / e isso 
    sprite = load(path)                             #da erro pra usuarios de linux
    sprite = sprite.convert_alpha() if convert_alpha else sprite.convert()
    return pygame.transform.scale_by(sprite, scale)



# Configurações da tela
SCREEN_WIDTH = 1008
SCREEN_HEIGHT = 720
PLAYER_POSITION=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
MAP_SCALE=5
FPS = 30

# Caminhos de assets
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, 'assets')
