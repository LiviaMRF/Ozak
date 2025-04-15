import pygame.font
import math
import random
from settings import *

class MenuScene:
    def __init__(self, game):
        self.game = game
        # try:
        #Carregar as fontes dos arquivos
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        chiller_path = os.path.join(BASE_DIR, "assets", "fonts", "Chiller.TTF")
        arial_path = os.path.join(BASE_DIR, "assets", "fonts", "Arial.ttf")

        self.title_font = pygame.font.Font(chiller_path, 120)
        self.option_font = pygame.font.Font(arial_path, 36)

        # Cores estilo hospital psiquiátrico abandonado
        self.blood_red = (120, 0, 0)
        self.dirty_white = (180, 180, 160)
        self.sick_black = BLACK
        self.dark_shadow = (15, 15, 20)

        # Texto com aparência danificada
        self.title_text = self.title_font.render("OZAK", True, self.blood_red)
        self.start_text = self.option_font.render("Pressione ESPAÇO para começar", True, self.dirty_white)
        self.quit_text = self.option_font.render("Pressione Q para sair", True, self.dirty_white)

        # Elementos de ambiente
        self.flickering = 0
        self.static_alpha = 0
        self.static_direction = 1
        self.heartbeat_timer = 0
        self.heartbeat_state = 0

        # Manchas e marcas
        self.stains = []
        for _ in range(15):
            self.stains.append({
                'pos': (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                'size': random.randint(5, 80),
                'color': (
                    random.randint(80, 130),
                    random.randint(0, 30),
                    random.randint(0, 30),
                    random.randint(30, 120)
                ),
                'type': random.choice(['circle', 'rect', 'splatter'])
            })

        # Cria efeito de papel na parede rasgado
        self.wall_tears = []
        for _ in range(8):
            self.wall_tears.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'width': random.randint(10, 100),
                'height': random.randint(50, 200),
                'color': self.dark_shadow
            })

        # Marcas de arranhões
        self.scratches = []
        for _ in range(12):
            start_x = random.randint(0, SCREEN_WIDTH)
            start_y = random.randint(0, SCREEN_HEIGHT)
            self.scratches.append({
                'start': (start_x, start_y),
                'lines': [
                    (start_x + random.randint(-50, 50), start_y + random.randint(10, 70)),
                    (start_x + random.randint(-50, 50), start_y + random.randint(10, 70)),
                    (start_x + random.randint(-50, 50), start_y + random.randint(10, 70))
                ],
                'width': random.randint(1, 3),
                'color': (random.randint(60, 100), 0, 0, random.randint(50, 180))
            })

        # Efeito de piscar texto
        self.text_visible = True
        self.blink_timer = 0
        self.blink_speed = random.uniform(0.5, 2.0)
        self.blink_duration = random.uniform(0.05, 0.2)

        # Variáveis para controle da transição
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 5
        # self.next_scene = None

        # Efeito de respiração
        self.breathing = 0

        # Cria textura de estática
        self.static_texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.update_static_texture()

        # Sons (apenas definidos aqui, precisariam ser carregados e inicializados)
        self.ambient_sound = None
        self.heartbeat_sound = None
        self.static_sound = None

    def update_static_texture(self):
        """Atualiza a textura de estática"""
        self.static_texture.fill((0, 0, 0, 0))
        for _ in range(5000):
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
            color = random.randint(0, 255)
            alpha = random.randint(5, 30)
            self.static_texture.set_at((x, y), (color, color, color, alpha))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and not self.transitioning:
            if event.key == pygame.K_SPACE:
                # Som de porta de hospital batendo poderia ser adicionado aqui
                self.transitioning = True
            elif event.key == pygame.K_q:
                self.game.running = False

    def update(self, dt):
        # Atualiza o efeito de piscar da luz
        self.flickering += dt
        if self.flickering > 0.1:
            self.flickering = 0
            if random.random() < 0.2:  # 20% chance de piscar
                self.text_visible = not self.text_visible

        # Efeito de respiração nas opções do menu
        self.breathing += dt * 1.5
        if self.breathing > 2 * math.pi:
            self.breathing = 0

        # Atualiza o temporizador de piscar
        self.blink_timer += dt
        if self.blink_timer > self.blink_speed:
            self.blink_timer = 0
            self.text_visible = not self.text_visible
            self.blink_speed = random.uniform(0.5, 3.0)

        # Atualiza o efeito de batimento cardíaco
        self.heartbeat_timer += dt
        if self.heartbeat_state == 0 and self.heartbeat_timer > 0.8:
            self.heartbeat_state = 1
            self.heartbeat_timer = 0
            # Tocar primeiro som de batida cardíaca aqui
        elif self.heartbeat_state == 1 and self.heartbeat_timer > 0.2:
            self.heartbeat_state = 0
            self.heartbeat_timer = 0
            # Tocar segundo som de batida cardíaca aqui

        # Atualiza a estática
        self.static_alpha += dt * 60 * self.static_direction
        if self.static_alpha > 40:
            self.static_direction = -1
        elif self.static_alpha < 5:
            self.static_direction = 1
            self.update_static_texture()

        # Lógica de transição
        if self.transitioning:
            self.transition_alpha += self.transition_speed
            self.game.door_sound.set_volume(0.5 - 0.5*self.transition_alpha/255)
            if self.transition_alpha >= 255:
                self.game.door_sound.set_volume(0)
                from .game import GameScene

                self.game.current_scene = GameScene(self.game, "scene1")
                self.game.current_scene.transitioning = True
                self.game.current_scene.transition_alpha = 255

    def render(self, screen):
        # Fundo de hospital sujo
        screen.fill(self.sick_black)

        # Renderiza os rasgos na parede
        for tear in self.wall_tears:
            pygame.draw.rect(screen, tear['color'],
                             (tear['x'], tear['y'], tear['width'], tear['height']))

        # Renderiza as manchas de "sangue" e sujeira
        for stain in self.stains:
            if stain['type'] == 'circle':
                pygame.draw.circle(
                    screen,
                    stain['color'],
                    stain['pos'],
                    stain['size']
                )
            elif stain['type'] == 'rect':
                pygame.draw.rect(
                    screen,
                    stain['color'],
                    (stain['pos'][0], stain['pos'][1], stain['size'], stain['size'])
                )
            else:  # splatter
                for _ in range(5):
                    offset_x = random.randint(-stain['size'] // 2, stain['size'] // 2)
                    offset_y = random.randint(-stain['size'] // 2, stain['size'] // 2)
                    size = stain['size'] // random.randint(2, 6)
                    pygame.draw.circle(
                        screen,
                        stain['color'],
                        (stain['pos'][0] + offset_x, stain['pos'][1] + offset_y),
                        size
                    )

        # Renderiza os arranhões
        for scratch in self.scratches:
            for line_end in scratch['lines']:
                pygame.draw.line(
                    screen,
                    scratch['color'],
                    scratch['start'],
                    line_end,
                    scratch['width']
                )

        # Adiciona padrão de azulejos de hospital
        # tile_size = 40
        # for x in range(0, SCREEN_WIDTH, tile_size):
        #     pygame.draw.line(screen, (100, 100, 90), (x, 0), (x, SCREEN_HEIGHT), 1)
        # for y in range(0, SCREEN_HEIGHT, tile_size):
        #     pygame.draw.line(screen, (100, 100, 90), (0, y), (SCREEN_WIDTH, y), 1)

        # Efeito de respiração para o título
        breathing_scale = 1 + math.sin(self.breathing) * 0.03
        # Efeito de heartbeat
        if self.heartbeat_state == 1:
            breathing_scale += 0.05

        # Cria uma versão "sangrando" do título
        bleeding_title = self.title_text.copy()
        blood_drips = pygame.Surface((bleeding_title.get_width(), bleeding_title.get_height() + 30), pygame.SRCALPHA)

        # Adiciona "sangue escorrendo"
        for x in range(0, bleeding_title.get_width(), 4):
            if random.random() < 0.3:  # 30% de chance de gota de sangue
                drip_length = random.randint(5, 30)
                drip_width = random.randint(2, 5)

                start_y = random.randint(bleeding_title.get_height() - 10, bleeding_title.get_height())
                pygame.draw.rect(
                    blood_drips,
                    (120, 0, 0, random.randint(100, 200)),
                    (x, start_y, drip_width, drip_length)
                )

                # Adiciona gota na ponta
                if random.random() < 0.5:
                    pygame.draw.circle(
                        blood_drips,
                        (120, 0, 0, random.randint(100, 200)),
                        (x + drip_width // 2, start_y + drip_length),
                        drip_width
                    )

        # Combina o título com o sangue
        combined_title = pygame.Surface((bleeding_title.get_width(), bleeding_title.get_height() + 30), pygame.SRCALPHA)
        combined_title.blit(bleeding_title, (0, 0))
        combined_title.blit(blood_drips, (0, 0))

        # Redimensiona o título com efeito de respiração
        scaled_title = pygame.transform.scale(
            combined_title,
            (int(combined_title.get_width() * breathing_scale),
             int(combined_title.get_height() * breathing_scale))
        )

        # Centraliza textos na tela
        title_x = SCREEN_WIDTH // 2 - scaled_title.get_width() // 2
        title_y = 150

        # Sombra do título
        shadow_offset = 3
        screen.blit(
            pygame.transform.scale(combined_title, (scaled_title.get_width(), scaled_title.get_height())),
            (title_x + shadow_offset, title_y + shadow_offset)
        )

        # Renderiza o título
        screen.blit(scaled_title, (title_x, title_y))

        # Só mostra o texto quando visível (efeito de piscar)
        if self.text_visible:
            # Estilo de botão de hospital desgastado para opções
            start_y = 400
            quit_y = 500

            # Botões com aparência de placas de hospital antigas
            for text, y in [(self.start_text, start_y), (self.quit_text, quit_y)]:
                button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - text.get_width() // 2 - 20,
                    y - 10,
                    text.get_width() + 40,
                    text.get_height() + 20
                )

                # Fundo do botão (placa velha)
                pygame.draw.rect(screen, (80, 80, 70), button_rect)

                # Borda enferrujada
                pygame.draw.rect(screen, (120, 60, 30), button_rect, 2)

                # Adiciona alguns "parafusos" nos cantos
                for corner in [
                    (button_rect.left + 5, button_rect.top + 5),
                    (button_rect.right - 5, button_rect.top + 5),
                    (button_rect.left + 5, button_rect.bottom - 5),
                    (button_rect.right - 5, button_rect.bottom - 5)
                ]:
                    pygame.draw.circle(screen, (60, 60, 50), corner, 3)

                # Adiciona rachaduras aleatórias na placa
                for _ in range(3):
                    start_x = random.randint(button_rect.left, button_rect.right)
                    start_y = random.randint(button_rect.top, button_rect.bottom)
                    end_x = start_x + random.randint(-30, 30)
                    end_y = start_y + random.randint(-20, 20)
                    pygame.draw.line(screen, (40, 40, 30), (start_x, start_y), (end_x, end_y), 1)

            # Renderiza texto
            screen.blit(self.start_text, (SCREEN_WIDTH // 2 - self.start_text.get_width() // 2, start_y))
            screen.blit(self.quit_text, (SCREEN_WIDTH // 2 - self.quit_text.get_width() // 2, quit_y))

        # Adiciona um texto de advertência psiquiátrica
        warning_font = pygame.font.SysFont("Courier New", 28)
        warning_text = warning_font.render("PACIENTE #1372 - TRATAMENTO RESTRITO", True, GRAY)
        screen.blit(warning_text, (20, SCREEN_HEIGHT - 30))

        date_text = warning_font.render("ADMISSÃO: 13/06/1973 - CASO: SEVERO", True, GRAY)
        screen.blit(date_text, (SCREEN_WIDTH - date_text.get_width() - 20, 20))

        # Sobreposição de estática
        static_overlay = self.static_texture.copy()
        static_overlay.set_alpha(int(self.static_alpha))
        screen.blit(static_overlay, (0, 0))

        # Efeito de vinheta (escurecimento nas bordas)
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Cria gradiente circular para vinheta
        for i in range(12):
            radius = int(max(SCREEN_WIDTH, SCREEN_HEIGHT) * (i / 10))
            pygame.draw.circle(
                vignette,
                (0, 0, 0, i * 5),
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                radius
            )

        screen.blit(vignette, (0, 0))

        # Renderiza overlay de transição se necessário
        if self.transitioning:
            # Transição estilo filmagem antiga de hospital
            transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

            # Adiciona linhas horizontais distorcidas
            line_count = int(self.transition_alpha / 10)
            for i in range(line_count):
                y_pos = int((i / line_count) * SCREEN_HEIGHT)
                line_width = random.randint(1, 3)
                line_offset = random.randint(-10, 10) if random.random() < 0.3 else 0
                pygame.draw.line(
                    transition_surface,
                    (0, 0, 0),
                    (0 + line_offset, y_pos),
                    (SCREEN_WIDTH + line_offset, y_pos),
                    line_width
                )

            # Adiciona estática na transição
            for _ in range(int(self.transition_alpha * 30)):
                x = random.randint(0, SCREEN_WIDTH - 1)
                y = random.randint(0, SCREEN_HEIGHT - 1)
                color = random.randint(0, 255)
                transition_surface.set_at((x, y), (color, color, color))

            transition_surface.set_alpha(self.transition_alpha)
            screen.blit(transition_surface, (0, 0))