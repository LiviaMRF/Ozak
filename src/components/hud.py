import pygame
from settings import *

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 24)
        self.health_bar = pygame.Surface((200, 20))
        self.stamina_bar = pygame.Surface((200, 20))

    def draw(self, screen):
        # Barra de Estamina (canto inferior esquerdo)
        stamina_width = int(200 * (self.player.stamina.current_stamina / 100))
        pygame.draw.rect(screen, (50, 50, 50), (20, SCREEN_HEIGHT - 40, 204, 24))
        pygame.draw.rect(screen, (0, 100, 255), (22, SCREEN_HEIGHT - 38, stamina_width, 20))

        # Texto Estamina
        stamina_text = self.font.render(f"STA: {int(self.player.stamina.current_stamina)}", True, (255, 255, 255))
        screen.blit(stamina_text, (25, SCREEN_HEIGHT - 38))

        # Barra de Vida (canto inferior direito)
        health_width = int(200 * (self.player.health / 100))
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH - 224, SCREEN_HEIGHT - 40, 204, 24))
        pygame.draw.rect(screen, (255, 50, 50), (SCREEN_WIDTH - 222, SCREEN_HEIGHT - 38, health_width, 20))

        # Texto Vida
        health_text = self.font.render(f"HP: {int(self.player.health)}", True, (255, 255, 255))
        screen.blit(health_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 38))

        # Texto da arma
        weapon_text = self.font.render(f"Arma: {self.player.current_weapon}", True, WHITE)
        screen.blit(weapon_text, (10, 70))