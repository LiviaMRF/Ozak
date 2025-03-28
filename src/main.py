import pygame
from settings import *
from scenes.menu import MenuScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = MenuScene(self)  # Começa com o menu

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time em segundos

            # Trata eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_scene.handle_events(event)

            # Atualiza e renderizada a cena atual
            self.current_scene.update(dt)
            self.current_scene.render(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()