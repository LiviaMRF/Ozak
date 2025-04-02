from settings import *

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("Arial", 20)
        self.health_bar = pygame.Surface((200, 20))
        self.stamina_bar = pygame.Surface((200, 20))

    def draw(self, screen):
        # Barra de Estamina (canto inferior esquerdo)
        stamina_width = int(200 * (self.player.stamina.current_stamina / 100))
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH - 224, SCREEN_HEIGHT - 60, 204, 24))
        pygame.draw.rect(screen, (0, 100, 255), (SCREEN_WIDTH - 222, SCREEN_HEIGHT - 58, stamina_width, 20))

        # Texto Estamina
        stamina_text = self.font.render(f"{int(self.player.stamina.current_stamina)}", True, (255, 255, 255))
        screen.blit(stamina_text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 60))

        # Barra de Vida (canto inferior direito)
        health_width = int(200 * (self.player.health / 100))
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH - 224, SCREEN_HEIGHT - 40, 204, 24))
        pygame.draw.rect(screen, (255, 50, 50), (SCREEN_WIDTH - 222, SCREEN_HEIGHT - 38, health_width, 20))

        # Texto Vida
        health_text = self.font.render(f"{max(0, int(self.player.health))}", True, (255, 255, 255))
        screen.blit(health_text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT -40))

        # Texto da arma
        #power_text = self.font.render(f"Arma: {self.player.current_power}", True, WHITE)
        #screen.blit(power_text, (10, 70))


        # Adiciona indicador de estado de corrida
        #run_status = "CORRENDO" if self.player.is_running else "ANDANDO"
        #tatus_color = (255, 0, 0) if self.player.stamina.is_exhausted else (0, 255, 0)

        #status_text = self.font.render(f"STATUS: {run_status}", True, status_color)
        #screen.blit(status_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 40))