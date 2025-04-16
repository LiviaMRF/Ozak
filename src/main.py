from settings import *
from scenes.intro import IntroScene
from scenes.game import GameScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
<<<<<<< HEAD
        self.current_scene = IntroScene(self)  # Começa com o menu
=======

        #sound_path = os.path.join("..", "assets", "music", "door-music.mp3")
        #self.door_sound= pygame.mixer.Sound(sound_path)
        #self.door_sound.set_volume(0.5)
        #self.door_sound.play(loops=-1)

        #self.current_scene = IntroScene(self)  # Começa com o menu
        self.current_scene = GameScene(self, "scene1")
>>>>>>> dd20c286444996b4249933401d212ec2b8e3ebdb

 
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
