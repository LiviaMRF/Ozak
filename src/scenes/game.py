from entities.door import Door
from entities.player import Player
from settings import *
from components.hud import HUD
from entities.boundary import Boundary
from entities.bicho_papao import BichoPapao
from entities.medico import Medico
from entities.alter_ego import AlterEgo

class GameScene:
    def __init__(self, game, scene_name="scene1"):
        self.game = game
        self.bg_color = WHITE
        self.scene_time = 0

        self.boundary = Boundary()
        self.boundary_gp = pygame.sprite.GroupSingle()
        self.boundary_gp.add(self.boundary)

        # Cria os grupos de poderes
        self.power_player_gp = pygame.sprite.Group()
        self.power_enemy_gp = pygame.sprite.Group()

        # Cria o jogador e o seu grupo
        self.player = Player()
        self.player_gp = pygame.sprite.GroupSingle()
        self.player_gp.add(self.player)

        # Cria um grupo para os inimigos
        self.enemies_gp = pygame.sprite.Group()
        alterego = AlterEgo((200, 200), self.player)
        self.enemies_gp.add(alterego)

        # Cria a SpriteShift
        self.sprite_shift = (0,0)

        # Sistema de HUD
        self.hud = HUD(self.player)
        self.font = pygame.font.Font(None, 36)

        self.scene_name = scene_name

        # Grupo de portas
        self.doors = pygame.sprite.Group()

        # Cria portas específicas para cada cena
        self._setup_doors(scene_name)

    def _create_scene1(self):
        door_pos = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 50)
        self.doors.add(Door(door_pos, "scene2"))

    def _create_scene2(self):
        door_pos = (50, SCREEN_HEIGHT // 2 - 50)
        self.doors.add(Door(door_pos, "scene1"))

    def _try_enter_door(self):
        for door in self.doors:
            actual_pos = (
                door.rect.x - self.sprite_shift[0],
                door.rect.y - self.sprite_shift[1]
            )
            if pygame.math.Vector2(self.player.rect.center).distance_to(actual_pos) < door.interaction_radius:
                self._change_scene(door.target_scene)
                break

    def _change_scene(self, target_scene):
        # Efeito de fade out
        for alpha in range(0, 255, 15):
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(alpha)
            self.render(self.game.screen)
            self.game.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

        # Cria nova cena
        self.game.current_scene = GameScene(self.game, target_scene)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.current_scene = MenuScene(self.game)

        # Dispara ao clicar com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            power = self.player.unleash_power(pygame.mouse.get_pos())
            if power:
                self.power_player_gp.add(power)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self._try_enter_door()

    def handle_collisions(self):

        for enemy_power in self.power_enemy_gp:
            #if self.player.rect.colliderect(enemy_power.rect):
            if self.player.rect.colliderect(enemy_power.rect) \
            and pygame.sprite.collide_mask(self.player, enemy_power):
            
                self.player.lose_health_points(enemy_power.damage)
                enemy_power.kill()

        for player_power in self.power_player_gp:
            for enemy in self.enemies_gp:
                #if enemy.rect.colliderect(player_power.rect):
                if enemy.rect.colliderect(player_power.rect) \
                and pygame.sprite.collide_mask(enemy, player_power):

                    enemy.lose_health_points(player_power.damage)
                    player_power.kill()

    def update(self, dt):
        self.scene_time+=dt

        if not self.player.is_dead:
            # Atualiza todos os sprites
            self.doors.update()
            self.sprite_shift = self.player.player_shift(dt)
            self.player_gp.update(dt)
            self.enemies_gp.update(dt)
            self.power_player_gp.update(dt)
            self.power_enemy_gp.update(dt)
            self.handle_collisions()


    def _move_group_and_render(self, screen, group):
        for element in group:
            element.rect.x -= self.sprite_shift[0]  # Aplica o offset
            element.rect.y -= self.sprite_shift[1]
        group.draw(screen)    
    def _draw_with_offset(self, screen, group):
        for sprite in group:
            screen.blit(sprite.image, (sprite.rect.x - self.sprite_shift[0],
                                       sprite.rect.y - self.sprite_shift[1]))

    def _setup_doors(self, scene_name):
        if not hasattr(self, 'doors'):
            self.doors = pygame.sprite.Group()  # Cria o grupo se não existir

        self.doors.empty()  # Limpa portas existentes

        if scene_name == "scene1":
            # Porta à direita que leva para cena 2
            self.doors.add(Door(
                boundary=self.boundary,
                side="right",
                target_scene="scene2"
            ))
        elif scene_name == "scene2":
            # Porta à esquerda que leva para cena 1
            self.doors.add(Door(
                boundary=self.boundary,
                side="left",
                target_scene="scene1"
            ))

    def spawn_enemies(self):
        pass

    def render(self, screen):
        if not self.player.is_dead:
            screen.fill(self.bg_color)

            # Renderiza o player com a sprite atual (idle ou run)
            self.player_gp.draw(screen)

            for enemy in self.enemies_gp:
                power = enemy.unleash_power(PLAYER_POSITION)
                if power:
                    self.power_enemy_gp.add(power)
            
            self._move_group_and_render(screen, self.power_player_gp)
            self._move_group_and_render(screen, self.power_enemy_gp)
            self._move_group_and_render(screen, self.boundary_gp)
            self._move_group_and_render(screen, self.enemies_gp)

            self._draw_with_offset(screen, self.doors)
            self._draw_with_offset(screen, self.player_gp)

            self.hud.draw(screen)

            # self.doors.draw(screen)
            for door in self.doors:
                pygame.draw.circle(screen, (255, 255, 0), door.rect.center, door.interaction_radius, 1)

            # Desenha o poder na posição correta
            screen.blit(self.player.current_power.image, self.player.current_power.rect)
            
            for enemy in self.enemies_gp:
                screen.blit(enemy.current_power.image, enemy.current_power.rect)

