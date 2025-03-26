from entities.player import Player
from settings import *
from entities.weapon_pickup import WeaponPickup
from components.hud import HUD

class GameScene:
    def __init__(self, game):
        self.game = game
        self.bg_color = WHITE

        # Grupos de sprites
        self.player_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.weapon_pickups = pygame.sprite.Group()

        # Cria o jogador
        self.player = Player()
        self.player_sprites.add(self.player)

        # Sistema de HUD
        self.hud = HUD(self.player)
        self.font = pygame.font.Font(None, 36)


    def spawn_weapon(self, pos, weapon_type):
        # Adiciona uma arma coletável no cenário
        pickup = WeaponPickup(pos, weapon_type)
        self.weapon_pickups.add(pickup)
        self.player_sprites.add(pickup)


    def _pick_up_weapon(self):
        #Verifica colisão com E pressionado
        for pickup in self.weapon_pickups:
            if pygame.sprite.collide_rect(self.player, pickup):
                if pickup.weapon_type not in self.player.weapons:  # Evita duplicatas
                    self.player.weapons.append(pickup.weapon_type)
                    self.player.current_weapon = pickup.weapon_type  # Equipa automaticamente
                    self.player.load_weapon(pickup.weapon_type)  # Carrega o sprite
                pickup.kill()
                break


    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.game.current_scene = MenuScene(self.game)
            elif event.key == pygame.K_e:
                self._pick_up_weapon()

        # Dispara ao clicar com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullet = self.player.shoot(pygame.mouse.get_pos())
            if bullet:
                self.bullets.add(bullet)
                self.player_sprites.add(bullet)  # Adiciona a bala no grupo de sprites para ser desenhada


    def update(self, dt):
        # Atualiza todos os sprites
        self.player_sprites.update(dt)
        self.bullets.update(dt)

        for bullet in self.bullets.copy():
            if not (0 <= bullet.rect.x <= SCREEN_WIDTH and 0 <= bullet.rect.y <= SCREEN_HEIGHT):
                bullet.kill()


    def render(self, screen):
        screen.fill(self.bg_color)
        self.player_sprites.draw(screen)
        self.bullets.draw(screen)
        self.hud.draw(screen)

        # Desenha a arma na posição correta
        if self.player.weapon_image:
            screen.blit(self.player.weapon_image, self.player.weapon_rect.topleft)

