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

def get_words(lines):
    index=0
    limit=len(lines)
    word=""
    words=[]
    while(index<limit):
        while(index<limit and lines[index]!=" " and lines[index]!="\n" ):
            word=word+lines[index]
            index=index+1
        if(index>=limit):
            continue
        if(word!=""):
            words.append(word)
        if(lines[index] =="\\"):
            index=index+2
        else:
            index=index+1
        word=""
    return words
    
def create_spawn_list():
    f=open("spawn_list.txt", "r")
    lines=f.read()
    f.close()
    spawn_list=[]#convention is: time name position_x(absolute) position_y(absolute) health damage
    unit_size=6 #bc we r using 5 inputs to spawn an enemy
    
    words=get_words(lines)
    limit=unit_size*int(len(words)/unit_size)
    
    index=0
    while(index<limit):
        spawn_list.append( ( float(words[index+0]), words[index+1], float(words[index+2]), float(words[index+3]), float(words[index+4]), float(words[index+5]) ) )
        index=index+unit_size
    return spawn_list
    
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
