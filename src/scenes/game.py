from entities.door import Door
from entities.player import Player
from settings import *
from components.hud import HUD
from entities.boundary import Boundary

class GameScene:
    def __init__(self, game, scene_name="default"):
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


        self.scene_name = scene_name

        # Grupo de portas
        self.doors = pygame.sprite.Group()

        # Cria portas específicas para cada cena
        if scene_name == "scene1":
            self._create_scene1()
        elif scene_name == "scene2":
            self._create_scene2()

    def _create_scene1(self):
        door_pos = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 50)
        self.doors.add(Door(door_pos, "scene2"))

    def _create_scene2(self):
        door_pos = (50, SCREEN_HEIGHT // 2 - 50)
        self.doors.add(Door(door_pos, "scene1"))

    def _try_enter_door(self):
        for door in self.doors:
            # Calcula distância entre player e porta
            distance = pygame.math.Vector2(self.player.rect.center).distance_to(door.rect.center)

            if distance < door.interaction_radius:
                from game import Game  # Importe circular
                self.game.current_scene = GameScene(self.game, door.target_scene)
                break

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self._try_enter_door()


    def update(self, dt):
        # Atualiza todos os sprites
        self.sprite_shift = self.player.player_shift(dt)
        self.player_gp.update(dt)
        self.powers_gp.update(dt)

        self.doors.update(dt)
        

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


        self.doors.draw(screen)
        for door in self.doors:
            pygame.draw.circle(screen, (255, 255, 0), door.rect.center, door.interaction_radius, 1)

        # Desenha o poder na posição correta
        if self.player.current_power:
            screen.blit(self.player.current_power.image, self.player.current_power.rect.topleft)

