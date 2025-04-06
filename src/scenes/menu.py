import pygame
from settings import *

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 74)
        self.title_text = self.font.render("OZAK", True, WHITE)
        self.start_text = pygame.font.Font(None, 36).render("Pressione ESPAÇO para começar", True, WHITE)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                from .game import GameScene
                self.game.current_scene = GameScene(self.game)# Transição para o jogo
                #self.game.current_scene = GameScene(self.game, "scene1")

    def update(self, dt):
        pass  # Lógica de atualização do menu (animações, etc.)

    def render(self, screen):
        screen.fill(BLACK)
        screen.blit(self.title_text, (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2, 200))
        screen.blit(self.start_text, (SCREEN_WIDTH // 2 - self.start_text.get_width() // 2, 400))