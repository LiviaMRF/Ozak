from entities.player import Player
from settings import *
from components.hud import HUD
from entities.boundary import Boundary

class GameScene:
    def __init__(self, game):
        self.game = game
        self.bg_color = WHITE

        self.boundary = Boundary()
        self.boundary_gp = pygame.sprite.GroupSingle()
        self.boundary_gp.add(self.boundary)


        self.powers_gp = pygame.sprite.Group()
        self.power_pickups = pygame.sprite.Group()

        # Cria o jogador e o seu grupo
        self.player = Player()
        self.player_gp = pygame.sprite.GroupSingle()
        self.player_gp.add(self.player)

        # Cria a SpriteShift
        self.sprite_shift = (0,0)

        # Sistema de HUD
        self.hud = HUD(self.player)
        self.font = pygame.font.Font(None, 36)



    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.current_scene = MenuScene(self.game)
            elif event.key == pygame.K_e:
                self._pick_up_power()

        # Dispara ao clicar com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            power = self.player.unleash_power(pygame.mouse.get_pos())
            if power:
                self.powers_gp.add(power)


    def update(self, dt):
        # Atualiza todos os sprites
        self.sprite_shift = self.player.player_shift(dt)
        self.player_gp.update(dt)
        self.powers_gp.update(dt)
        

    def _move_group_and_render(self, screen, group):
        for element in group:
            element.rect.x -= self.sprite_shift[0]  # Aplica o offset
            element.rect.y -= self.sprite_shift[1]
        group.draw(screen)    


    def render(self, screen):
        screen.fill(self.bg_color)

        # Renderiza o player com a sprite atual (idle ou run)
        self.player_gp.draw(screen)

        
        self._move_group_and_render(screen, self.powers_gp)
        self._move_group_and_render(screen, self.boundary_gp)


        self.hud.draw(screen)

        # Desenha o poder na posição correta
        if self.player.current_power:
            screen.blit(self.player.current_power.image, self.player.current_power.rect.topleft)

