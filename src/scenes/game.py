
import pygame.font
import os
from abc import ABC, abstractmethod
from entities.door import Door
from entities.player import Player
from settings import *
from components.hud import HUD
from entities.boundary import Boundary
from entities.bicho_papao import BichoPapao
from entities.medico import Medico
from entities.alter_ego import AlterEgo
from scenes.menu import MenuScene
from scenes.musical_video import MusicalVideo
from entities.power import Power


class Entity(ABC):
    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def lose_health_points(self, damage):
        pass

    @abstractmethod
    def unleash_power(self, target):
        pass


class Enemy:
    @classmethod
    def create(cls, enemy_type, player, **kwargs, std_health=50, damage=2):
        if enemy_type == "bichopapao":
            return BichoPapao(
                player=player,
                idle_time=kwargs.get('idle_time', 3),
                running_time=kwargs.get('running_time', 2),
                screen_pos=kwargs.get('screen_pos'),
                real_pos=kwargs.get('real_pos'),
                idle_frames=[f"enemies{os.sep}bichopapao_parado_{idx}.png" for idx in range(0, 2)],
                idle_animation_speed=0.10,
                moving_frames=[f"enemies{os.sep}bichopapao_andando_{idx}.png" for idx in range(0, 4)],
                moving_animation_speed=0.20,
                max_cooldown=1,
                power_type="bichopapao",
                power_speed=500,
                power_damage=damage,
                base_speed=300,
                health=std_health,
                sprite_scale=1
            )
        elif enemy_type == "medico":
            return Medico(
                player=player,
                ratio_radial_to_tangential_speed=kwargs.get('ratio_radial_to_tangential_speed', 0.15),
                screen_pos=kwargs.get('screen_pos'),
                real_pos=kwargs.get('real_pos'),
                idle_frames=[],
                idle_animation_speed=0.10,
                moving_frames=[f"enemies{os.sep}medico_andando_{idx}.png" for idx in range(0, 4)],
                moving_animation_speed=0.20,
                max_cooldown=0.7,
                power_type="medico",
                power_speed=500,
                power_damage=damage,
                base_speed=250,
                health=std_health,
                sprite_scale=1
            )
        else:
            raise ValueError(f"Tipo de inimigo desconhecido: {enemy_type}")


class GameScene:
    def __init__(self, game, scene_name, change_status = True):
        self.game = game
        self.scene_time = 0
        self.musical_video = MusicalVideo()
        self.scene_name = scene_name
        self.sprite_shift = (0, 0)
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 3.5
        felf.spawn_list=create_spawn_list()

        # Inicializa elementos do jogo
        self._init_boundary(change_status)
        self._init_power_groups()
        self._init_player(change_status)
        self._init_enemies(change_status)
        self._init_hud()
        self._init_doors(scene_name)
        self._init_death_menu()

        self.change_status = change_status

    def _init_boundary(self, change_status):
        self.boundary = Boundary() if change_status else self.game.current_scene.boundary
        self.boundary_gp = pygame.sprite.GroupSingle()
        self.boundary_gp.add(self.boundary)

    def _init_power_groups(self):
        self.power_player_gp = pygame.sprite.Group()
        self.power_enemy_gp = pygame.sprite.Group()

    def _init_player(self, change_status):
        if change_status:
            self.player = Player(
                max_stamina=100, drain_rate=20, recover_rate=15, run_speed_multiplier=1.8,
                screen_pos=PLAYER_POSITION, real_pos=PLAYER_POSITION,
                idle_frames=[f"player{os.sep}ozak_parado_{idx}.png" for idx in range(0, 2)],
                idle_animation_speed=0.3,
                moving_frames=[f"player{os.sep}ozak_andando_{idx}.png" for idx in range(0, 4)],
                moving_animation_speed=0.25,
                max_cooldown=0.2, power_type="ozak", power_speed=500, power_damage=10,
                base_speed=300, health=100, sprite_scale=1
            )
        else:
            self.player = self.game.current_scene.player

        self.player_gp = pygame.sprite.GroupSingle()
        self.player_gp.add(self.player)

    def _init_enemies(self, change_status):
        self.enemies_gp = pygame.sprite.Group() if change_status else self.game.current_scene.enemies_gp

        if change_status:
            self._spawn_enemies()

    def _spawn_enemies(self):
        # Bicho Papão
        self._create_enemy("bichopapao", [200, 200])

        # Três Médicos
        for _ in range(3):
            self._create_enemy("medico", [200, 200])

    def _create_enemy(self, enemy_type, screen_pos_spawn, health=50, damage=2):
        real_pos_spawn = [
            screen_pos_spawn[0]  + self.player.real_rect.center[0],
            screen_pos_spawn[1]  + self.player.real_rect.center[1]
        ]
        enemy = Enemy.create(
            enemy_type,
            player=self.player,
            health,
            damage,
            screen_pos=tuple(screen_pos_spawn),
            real_pos=tuple(real_pos_spawn)
        )
        self.enemies_gp.add(enemy)

    def _init_hud(self):
        self.hud = HUD(self.player)

    def _init_death_menu(self):
        self.death_timer = 2.0
        self.death_animation_complete = False
        self.show_death_menu = False

        # Fontes
        self.font_large = pygame.font.SysFont('Arial', 72)
        self.font_medium = pygame.font.SysFont('Arial', 48)
        self.font_small = pygame.font.SysFont('Arial', 36)

        # Botões
        button_width = 500
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2

        self.retry_button = pygame.Rect(button_x, SCREEN_HEIGHT // 2 + 20, button_width, button_height)
        self.menu_button = pygame.Rect(button_x, SCREEN_HEIGHT // 2 + 100, button_width, button_height)

    def _init_doors(self, scene_name):
        self.doors = pygame.sprite.Group()
        self._setup_doors(scene_name)

    def _setup_doors(self, scene_name):
        self.doors.empty()  # Limpa portas existentes

        if scene_name == "scene1":
            # Porta à direita que leva para cena 2
            self.doors.add(Door(self.boundary, "right", "scene2"))
        # elif scene_name == "scene2":
        #     # Porta à esquerda que leva para cena 1
        #     self.doors.add(Door(self.boundary, "left", "scene1"))


    def _try_enter_door(self):
        for door in self.doors:
            actual_pos = (
                door.rect.x - self.sprite_shift[0],
                door.rect.y - self.sprite_shift[1]
            )
            if pygame.math.Vector2(self.player.rect.center).distance_to(actual_pos) < door.interaction_radius \
                    and not self.player.is_moving:
                self._change_scene(door.target_scene)
                break

    def _change_scene(self, target_scene):
        # Efeito de fade out
        self._perform_scene_transition()

        self.sprite_shift = (0, 0)
        self.game.current_scene = GameScene(self.game, target_scene, change_status=False)
        self.game.current_scene.sprite_shift = (0, 0)

    def _perform_scene_transition(self):
        for alpha in range(0, 255, 15):
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(alpha)
            self.render(self.game.screen)
            self.game.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(30)

    def handle_events(self, event):
        if self.show_death_menu:
            self._handle_death_menu_events(event)
            return

        # Processamento normal de eventos durante o jogo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_scene = MenuScene(self.game)
            elif event.key == pygame.K_e:
                self._try_enter_door()

        # Dispara ao clicar com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            power = self.player.unleash_power(pygame.mouse.get_pos())
            if power:
                self.power_player_gp.add(power)

    def _handle_death_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            # Botão "Tentar Novamente"
            if self.retry_button.collidepoint(mouse_pos):
                self.game.current_scene = GameScene(self.game, "scene1")

    def handle_collisions(self):
        # Verifica colisões entre poderes inimigos e jogador
        for enemy_power in self.power_enemy_gp:
            if self.player.rect.colliderect(enemy_power.rect) \
                    and pygame.sprite.collide_mask(self.player, enemy_power):
                self.player.lose_health_points(enemy_power.damage)
                enemy_power.kill()

        # Verifica colisões entre poderes do jogador e inimigos
        for player_power in self.power_player_gp:
            for enemy in self.enemies_gp:
                if enemy.rect.colliderect(player_power.rect) \
                        and pygame.sprite.collide_mask(enemy, player_power):
                    enemy.lose_health_points(player_power.damage)
                    player_power.kill()

    def update(self, dt):
        self._update_transition(dt)
        self.scene_time += dt

        if not self.player.is_dead:
            self._update_game_state(dt)
        else:
            self._update_death_sequence(dt)

    def _update_transition(self, dt):
        if self.transitioning:
            if self.transition_alpha > 0:
                self.transition_alpha -= self.transition_speed
                if self.transition_alpha <= 0:
                    self.transitioning = False

    def _update_game_state(self, dt):
        # Atualiza todos os sprites
        self.doors.update()
        self.sprite_shift = self.player.player_shift(dt)
        self.player_gp.update(dt)
        self.update_spawn_list()
        self.enemies_gp.update(dt)
        self.power_player_gp.update(dt)
        self.power_enemy_gp.update(dt)
        self.handle_collisions()

    def update_spawn_list(self):
        if(self.spawn_list[0][0]<self.scene_time):
            self.create_enemy(self, self.spawn_list[0][1], [self.spawn_list[0][2][0], self.spawn_list[0][2][1]], 50, 2)

    def _update_death_sequence(self, dt):
        # Gerencia animação de morte e exibição do menu
        if not self.death_animation_complete:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.death_animation_complete = True
                self.show_death_menu = True

    def _move_group_and_render(self, screen, group, apply_offset=True):
        for element in group:
            if apply_offset:
                element.rect.x -= self.sprite_shift[0]
                element.rect.y -= self.sprite_shift[1]
        group.draw(screen)

    def _draw_with_offset(self, screen, group):
        for sprite in group:
            screen.blit(sprite.image, (sprite.rect.x - self.sprite_shift[0],
                                       sprite.rect.y - self.sprite_shift[1]))

    def _render_death_menu(self, screen):
        # Escurece a tela para o menu
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparente
        screen.blit(overlay, (0, 0))

        # Título "Você Morreu"
        text = self.font_large.render("Você Morreu", True, RED)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

        # Botão "Tentar Novamente"
        pygame.draw.rect(screen, BLACK, self.retry_button)
        pygame.draw.rect(screen, WHITE, self.retry_button, 3)
        retry_text = self.font_medium.render("Tentar Novamente", True, WHITE)
        screen.blit(retry_text, (self.retry_button.centerx - retry_text.get_width() // 2,
                                 self.retry_button.centery - retry_text.get_height() // 2))

    def _render_game(self, screen):
        # Renderiza os poderes dos inimigos
        for enemy in self.enemies_gp:
            power = enemy.unleash_power(self.player.rect.center)
            if power:
                self.power_enemy_gp.add(power)

        # Renderiza todos os componentes do jogo
        self._move_group_and_render(screen, self.power_player_gp)
        self._move_group_and_render(screen, self.power_enemy_gp)
        self._move_group_and_render(screen, self.boundary_gp)
        self._move_group_and_render(screen, self.enemies_gp)

        if self.scene_name == "scene1":
            self._draw_with_offset(screen, self.doors)
            for door in self.doors:
                door_center = (door.rect.centerx - self.sprite_shift[0],
                               door.rect.centery - self.sprite_shift[1])
                # pygame.draw.circle(screen, (255, 255, 0), door_center, door.interaction_radius, 1)

        self.hud.draw(screen)
        self._move_group_and_render(screen, self.player_gp, apply_offset=False)

        # Desenha os poderes
        screen.blit(self.player.current_power.image, self.player.current_power.rect)
        for enemy in self.enemies_gp:
            screen.blit(enemy.current_power.image, enemy.current_power.rect)

    def _render_death_animation(self, screen):
        # Animação de morte (efeito fade)
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Aplica efeito de escurecimento progressivo
        alpha = min(255, int((1 - self.death_timer / 2.0) * 255))
        darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        darken.fill((100, 0, 0))  # Vermelho escuro
        darken.set_alpha(alpha)

        screen.blit(temp_surface, (0, 0))
        screen.blit(darken, (0, 0))

        # Texto "Você Morreu" durante a animação
        font = self.font_large
        text = font.render("Você Morreu", True, RED)
        text_alpha = min(255, int(alpha * 1.5))  # Texto aparece mais rápido que o fundo
        text.set_alpha(text_alpha)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                           SCREEN_HEIGHT // 2 - text.get_height() // 2))

        self.hud.draw(screen)

    def _render_death_menu_screen(self, screen):
        # Depois da animação, mostra o menu de morte
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Aplicar um efeito de desfoque/escurecimento
        darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        darken.fill((50, 0, 0))  # Vermelho muito escuro
        darken.set_alpha(200)  # Bastante opaco

        screen.blit(temp_surface, (0, 0))
        screen.blit(darken, (0, 0))

        # Renderiza o menu de morte
        self._render_death_menu(screen)

    def render(self, screen):
        # Renderiza o vídeo musical de fundo
        self.musical_video.update(screen)

        # Renderiza transição se necessário
        if self.transitioning:
            transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            transition_surface.fill(BLACK)
            transition_surface.set_alpha(self.transition_alpha)
            screen.blit(transition_surface, (0, 0))

        if not self.player.is_dead:
            # Renderização normal do jogo
            self._render_game(screen)
        else:
            # Renderização durante a morte do jogador
            if not self.death_animation_complete:
                self._render_death_animation(screen)
            elif self.show_death_menu:
                self._render_death_menu_screen(screen)
