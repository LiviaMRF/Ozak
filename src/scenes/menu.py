import pygame.font
from settings import *


class MenuScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 90)
        self.title_text = self.font.render("OZAK", True, WHITE)
        self.start_text = pygame.font.SysFont("Arial", 36).render("Pressione ESPAÇO para começar", True, WHITE)
        self.start_text_2 = pygame.font.SysFont("Arial", 36).render("Pressione Q para sair", True, WHITE)

        # Variáveis para controle da transição
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 3.5
        self.next_scene = None

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and not self.transitioning and event.key == pygame.K_SPACE:
            from .game import GameScene
            self.next_scene = GameScene
            self.transitioning = True

        if event.type == pygame.KEYDOWN and not self.transitioning and event.key == pygame.K_q:
            self.game.running = False


    def update(self, dt):
        if self.transitioning and self.transition_alpha < 255:
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.game.current_scene = self.next_scene(self.game, "scene1")
                self.game.current_scene.transitioning = True
                self.game.current_scene.transition_alpha = 255

    def render(self, screen):
        screen.fill(BLACK)
        # Centraliza textos na tela
        screen.blit(self.title_text, (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2, 200))
        screen.blit(self.start_text, (SCREEN_WIDTH // 2 - self.start_text.get_width() // 2, 400))
        screen.blit(self.start_text_2, (SCREEN_WIDTH // 2 - self.start_text.get_width() // 2, 500))

        # Renderiza overlay de transição se necessário
        if self.transitioning:
            transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            transition_surface.fill(BLACK)
            transition_surface.set_alpha(self.transition_alpha)
            screen.blit(transition_surface, (0, 0))