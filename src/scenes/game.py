from entities.player import Player
from settings import *
from entities.weapon_pickup import WeaponPickup
from components.hud import HUD
from entities.boundary import Boundary

class GameScene:
    def __init__(self, game):
        self.game = game
        self.bg_color = WHITE

        self.boundary = Boundary()
        self.boundary_gp = pygame.sprite.GroupSingle()
        self.boundary_gp.add(self.boundary)


        self.bullets_gp = pygame.sprite.Group()
        self.weapon_pickups = pygame.sprite.Group()

        # Cria o jogador e o seu grupo
        self.player = Player()
        self.player_gp = pygame.sprite.GroupSingle()
        self.player_gp.add(self.player)

        # Cria a SpriteShift
        self.sprite_shift = (0,0)

        # Sistema de HUD
        self.hud = HUD(self.player)
        self.font = pygame.font.Font(None, 36)


    def spawn_weapon(self, pos, weapon_type):
        # Adiciona uma arma coletável no cenário
        pickup = WeaponPickup(pos, weapon_type)
        self.weapon_pickups.add(pickup)
        self.player_gp.add(pickup)


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
                self.bullets_gp.add(bullet)


    def update(self, dt):
        # Atualiza todos os sprites
        self.sprite_shift = self.player.player_shift(dt)
        self.player_gp.update(dt)
        self.bullets_gp.update(dt)
        

        #for bullet in self.bullets_gp.copy():
        #    if not (0 <= bullet.rect.x <= SCREEN_WIDTH and 0 <= bullet.rect.y <= SCREEN_HEIGHT):
        #        bullet.kill()

    def _move_group_render(self, screen, group):
        for element in group:
            element.rect.x -= self.sprite_shift[0]  # Aplica o offset
            element.rect.y -= self.sprite_shift[1]
        group.draw(screen)    


    def render(self, screen):
        screen.fill(self.bg_color)

        # Renderiza o player com a sprite atual (idle ou run)
        self.player_gp.draw(screen)

        
        self._move_group_render(screen, self.bullets_gp)
        self._move_group_render(screen, self.boundary_gp)



        self.hud.draw(screen)

        # Desenha a arma na posição correta
        if self.player.weapon_image:
            screen.blit(self.player.weapon_image, self.player.weapon_rect.topleft)

