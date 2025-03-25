import os
import pygame
from pygame.image import load

def load_sprite(name, scale=1, convert_alpha=True):
    path = os.path.join(ASSETS_PATH, "images", name)
    sprite = load(path)
    sprite = sprite.convert_alpha() if convert_alpha else sprite.convert()
    return pygame.transform.scale_by(sprite, scale)



# Configurações da tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Caminhos de assets
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, 'assets')