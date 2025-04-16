import pygame.font
import math
import random

from settings import *


class IntroScene:
    def __init__(self, game):
        self.game = game

        try:
            self.message_font = pygame.font.SysFont("Courier New", 24)
            self.small_font = pygame.font.SysFont("Courier New", 16)
        except:
            self.message_font = pygame.font.SysFont(None, 24)
            self.small_font = pygame.font.SysFont(None, 16)

        # Cores
        self.dirty_white = (180, 180, 160)
        self.blood_red = (120, 0, 0)
        self.shadow_color = (15, 15, 20)
        self.wall_color = (60, 60, 55)
        self.floor_color = (40, 38, 35)

        # Estado da cena
        self.scene_phase = 0  # Fases da animação
        self.phase_timer = 0
        self.typing_index = 0
        self.current_message = ""
        self.message_complete = False

        self.messages = [
            "Bem-vindo ao Hospital Psiquiátrico St. Daemon...",
            "Paciente #1372, seu tratamento hoje será... especial.",
            "Ninguém pode ouvir seus gritos aqui...",
            "O doutor estará com você em breve...",
            "Não resista, apenas aceite o tratamento..."
        ]

        # Elementos do quarto
        self.room_elements = self.create_room_elements()

        # Efeitos visuais
        self.flickering = 0
        self.flicker_intensity = 0

        # Manchas nas paredes/chão
        self.stains = []
        for _ in range(25):
            self.stains.append({
                'pos': (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                'size': random.randint(5, 40),
                'color': (
                    random.randint(60, 100),
                    random.randint(0, 20),
                    random.randint(0, 20),
                    random.randint(20, 80)
                ),
                'type': random.choice(['circle', 'rect', 'splatter'])
            })

        # Arranhões nas paredes
        self.scratches = []
        for _ in range(15):
            start_x = random.randint(100, SCREEN_WIDTH - 100)
            start_y = random.randint(100, 400)
            length = random.randint(30, 100)
            self.scratches.append({
                'start': (start_x, start_y),
                'end': (start_x + random.randint(-length, length),
                        start_y + random.randint(10, length)),
                'width': random.randint(1, 3),
                'color': (random.randint(20, 50), random.randint(10, 30), random.randint(10, 30))
            })

        # Escritos na parede (rabiscos)
        self.wall_writings = []
        wall_messages = ["SOCORRO", "SAIA", "ELE ESTÁ AQUI", "1372", "MORTE", "AJUDA"]
        for _ in range(4):
            message = random.choice(wall_messages)
            self.wall_writings.append({
                'text': message,
                'pos': (random.randint(50, SCREEN_WIDTH - 100), random.randint(100, 400)),
                'size': random.randint(30, 48),
                'color': (random.randint(60, 120), 0, 0),
                'angle': random.randint(-30, 30)
            })

        # Elementos de UI
        self.typing_sound_timer = 0

        # Efeito de respiração
        self.breathing = 0
        self.breath_speed = 1.0

        # Variáveis para controle da transição
        self.transitioning = False
        self.transition_alpha = 0
        self.transition_speed = 3
        self.next_scene = None

        # Variáveis para fade inicial
        self.fade_in = True
        self.fade_alpha = 255

        # Variáveis para a sombra móvel
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        shadow_path = os.path.join(BASE_DIR, "assets", "images", "player", "shadow.png")
        # Carrega a imagem
        self.shadow_sprite = pygame.image.load(shadow_path).convert_alpha()
        self.shadow_sprite = pygame.transform.scale(self.shadow_sprite, (90, 120))

        # self.shadow_sprite = pygame.transform.scale(self.shadow_sprite, (70, 80))
        self.shadow_position_y = 121
        self.shadow_position_x = SCREEN_WIDTH // 2 - 35
        self.shadow_range = 35  # distância máxima para esquerda/direita
        self.shadow_speed = 10  # pixels por segundo
        self.shadow_direction = 1  # 1 = direita, -1 = esquerda
        self.shadow_offset = 0
        self.shadow_appears = False

        # Para o efeito de piscar os olhos
        self.blink_timer = 0
        self.blink_state = False

        # Iniciar efeito de fade in
        self.fade_in = True
        self.fade_alpha = 255

        # Inicializar música da porta
        sound_path = os.path.join("..", "assets", "music", "door-music.mp3")
        self.door_sound= pygame.mixer.Sound(sound_path)
        self.door_sound.set_volume(0.5)
        self.door_sound.play(loops=-1)

    def create_room_elements(self):
        """Cria os elementos do quarto psiquiátrico"""
        elements = []

        # Cama de hospital
        bed_frame = {
            'type': 'rect',
            'rect': pygame.Rect(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 180, 180, 90),
            'color': (80, 80, 90),
            'outline': True,
            'outline_color': (40, 40, 50),
            'outline_width': 2,
            'z_index': 1
        }
        elements.append(bed_frame)

        # Colchão
        mattress = {
            'type': 'rect',
            'rect': pygame.Rect(SCREEN_WIDTH - 270, SCREEN_HEIGHT - 175, 160, 80),
            'color': (160, 160, 140),
            'outline': False,
            'z_index': 2
        }
        elements.append(mattress)

        # Manchas no colchão
        for _ in range(5):
            stain = {
                'type': 'circle',
                'center': (
                    SCREEN_WIDTH - 270 + random.randint(10, 150),
                    SCREEN_HEIGHT - 175 + random.randint(10, 70)
                ),
                'radius': random.randint(5, 15),
                'color': (random.randint(60, 100), random.randint(0, 20), random.randint(0, 20)),
                'z_index': 3
            }
            elements.append(stain)

        # Mesa de metal
        table = {
            'type': 'rect',
            'rect': pygame.Rect(100, SCREEN_HEIGHT - 150, 120, 70),
            'color': (100, 100, 110),
            'outline': True,
            'outline_color': (70, 70, 80),
            'outline_width': 2,
            'z_index': 1
        }
        elements.append(table)

        # Instrumentos médicos na mesa
        for _ in range(3):
            inst = {
                'type': 'rect',
                'rect': pygame.Rect(
                    110 + random.randint(0, 80),
                    SCREEN_HEIGHT - 145 + random.randint(0, 50),
                    random.randint(10, 30),
                    random.randint(5, 15)
                ),
                'color': (200, 200, 210),
                'outline': True,
                'outline_color': (150, 150, 160),
                'outline_width': 1,
                'z_index': 2
            }
            elements.append(inst)

        # Janela com barras
        window_frame = {
            'type': 'rect',
            'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, 80, 200, 140),
            'color': BLACK,
            'outline': True,
            'outline_color': (80, 80, 90),
            'outline_width': 3,
            'z_index': 1
        }
        elements.append(window_frame)
        # Porta (aumentada)
        door = {
            'type': 'rect',
            'rect': pygame.Rect(50, SCREEN_HEIGHT - 420, 160, 320),
            'color': (60, 55, 50),
            'outline': True,
            'outline_color': (40, 35, 30),
            'outline_width': 3,
            'z_index': 1
        }
        elements.append(door)

        # Maçaneta (reposicionada proporcionalmente)
        doorknob = {
            'type': 'circle',
            'center': (50 + 160 - 20, SCREEN_HEIGHT - 260),
            'radius': 10,
            'color': (120, 120, 100),
            'z_index': 2
        }
        elements.append(doorknob)

        # Janela na porta (aumentada e centralizada proporcionalmente)
        door_window = {
            'type': 'rect',
            'rect': pygame.Rect(70, SCREEN_HEIGHT - 390, 120, 60),
            'color': (20, 20, 35),
            'outline': True,
            'outline_color': (100, 100, 90),
            'outline_width': 2,
            'z_index': 2
        }
        elements.append(door_window)

        # Grade na janela da porta (atualizada para nova janela)
        for _ in range(4):
            door_bar_v = {
                'type': 'rect',
                'rect': pygame.Rect(85 + _ * 25, SCREEN_HEIGHT - 390, 3, 60),
                'color': (100, 100, 90),
                'outline': False,
                'z_index': 3
            }
            elements.append(door_bar_v)

        for _ in range(3):
            door_bar_h = {
                'type': 'rect',
                'rect': pygame.Rect(70, SCREEN_HEIGHT - 375 + _ * 20, 120, 3),
                'color': (100, 100, 90),
                'outline': False,
                'z_index': 3
            }
            elements.append(door_bar_h)

        # Luz no teto
        light = {
            'type': 'rect',
            'rect': pygame.Rect(SCREEN_WIDTH // 2 - 50, 40, 100, 20),
            'color': (180, 180, 150),
            'outline': True,
            'outline_color': (150, 150, 120),
            'outline_width': 2,
            'z_index': 1
        }
        elements.append(light)

        # Balde no canto
        bucket = {
            'type': 'circle',
            'center': (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 60),
            'radius': 25,
            'color': (80, 75, 70),
            'z_index': 1
        }
        elements.append(bucket)

        return elements

    def handle_events(self, event):
        # Se apertar qualquer tecla, avança a cena mais rapidamente
        if event.type == pygame.KEYDOWN and event.key != pygame.K_q:
            if self.message_complete:
                # Avança para próxima fase
                self.scene_phase += 1
                self.typing_index = 0
                self.message_complete = False
                # Se estiver na última fase, inicia transição
                if self.scene_phase >= len(self.messages):
                    self.transitioning = True

            else:
                # Completa a mensagem atual imediatamente
                if  self.typing_index >= len(self.messages):
                    self.typing_index += 1
                self.message_complete = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.game.running = False

    def update(self, dt):
        # Atualiza o fade in inicial
        if self.fade_in and self.fade_alpha > 0:
            self.fade_alpha -= 2
            if self.fade_alpha <= 0:
                self.fade_in = False

        # Atualiza o efeito de piscar
        self.blink_timer += dt
        if self.blink_timer > 5:  # A cada 5 segundos
            self.blink_state = True
            if self.blink_timer > 5.15:  # Duração do piscar: 0.15 segundos
                self.blink_state = False
                self.blink_timer = 0

        # Atualiza o efeito de sombra móvel
        if self.scene_phase > 1:  # Depois da segunda mensagem
            self.shadow_appears = True
            if self.shadow_appears:
                self.shadow_offset += self.shadow_direction * self.shadow_speed * dt
                if abs(self.shadow_offset) >= self.shadow_range:
                    self.shadow_offset = self.shadow_range * self.shadow_direction
                    self.shadow_direction *= -1  # Inverte a direção

                self.shadow_position_x = self.shadow_position_x = SCREEN_WIDTH // 2 - 35 + self.shadow_offset

        # Atualiza o efeito de digitação de texto
        if not self.message_complete and self.scene_phase < len(self.messages):
            self.typing_index += 0.5
            if self.typing_index >= len(self.messages[self.scene_phase]):
                self.typing_index = len(self.messages[self.scene_phase])
                self.message_complete = True
                # Reproduzir som de finalização de texto aqui
            else:
                # Reproduzir som de digitação a cada caractere
                self.typing_sound_timer += dt
                if self.typing_sound_timer > 0.05:  # Som a cada 0.05 segundos durante digitação
                    self.typing_sound_timer = 0
                    # Reproduzir typing_sound aqui

        # Atualiza o efeito de respiração
        self.breathing += dt * self.breath_speed
        if self.breathing > 2 * math.pi:
            self.breathing = 0

        # Atualiza o efeito de flicker da luz
        self.flickering += dt
        if self.flickering > 0.1:
            self.flickering = 0
            if random.random() < 0.2:  # 20% de chance de piscar
                self.flicker_intensity = random.uniform(0.5, 1.0)
            else:
                self.flicker_intensity = 0

        # Lógica de transição
        if self.transitioning:
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                from .menu import MenuScene
                self.game.current_scene = MenuScene(self.game, self.door_sound)
                self.game.current_scene.transitioning = False
                self.game.current_scene.transition_alpha = 0

    def render(self, screen):

        # Desenha o chão
        pygame.draw.rect(screen, self.floor_color, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

        # Linha de junção parede/chão
        pygame.draw.line(screen, (30, 30, 25), (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 3)

        # Desenha a parede
        pygame.draw.rect(screen, self.wall_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100))

        # Adiciona textura à parede (manchas)
        for stain in self.stains:
            if stain['pos'][1] < SCREEN_HEIGHT - 100:  # Apenas manchas na parede
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
                    for _ in range(3):
                        offset_x = random.randint(-stain['size'] // 2, stain['size'] // 2)
                        offset_y = random.randint(-stain['size'] // 2, stain['size'] // 2)
                        size = stain['size'] // random.randint(2, 4)
                        pygame.draw.circle(
                            screen,
                            stain['color'],
                            (stain['pos'][0] + offset_x, stain['pos'][1] + offset_y),
                            size
                        )

        # Arranhões nas paredes
        for scratch in self.scratches:
            pygame.draw.line(
                screen,
                scratch['color'],
                scratch['start'],
                scratch['end'],
                scratch['width']
            )

        # Escritos na parede
        for writing in self.wall_writings:

            # Carregar as fontes dos arquivos
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            chiller_path = os.path.join(BASE_DIR, "assets", "fonts", "Chiller.TTF")

            scribble_font = pygame.font.Font(chiller_path, writing['size'])
            # Renderizar o texto
            text_surf = scribble_font.render(writing['text'], True, writing['color'])
            # Rotacionar o texto
            text_surf = pygame.transform.rotate(text_surf, writing['angle'])
            # Posicionar o texto
            screen.blit(text_surf, writing['pos'])

        # Desenha os elementos do quarto em ordem de z-index
        sorted_elements = sorted(self.room_elements, key=lambda x: x.get('z_index', 0))
        for element in sorted_elements:
            if element['type'] == 'rect':
                pygame.draw.rect(screen, element['color'], element['rect'])
                if element.get('outline', False):
                    pygame.draw.rect(screen, element['outline_color'], element['rect'],
                                     element['outline_width'])
            elif element['type'] == 'circle':
                pygame.draw.circle(screen, element['color'], element['center'], element['radius'])

        # Desenha uma sombra móvel (figura sombria passando pela janela)

        if self.shadow_appears:
            screen.blit(self.shadow_sprite, (self.shadow_position_x, self.shadow_position_y))

        for i in range(5):
            bar_x = SCREEN_WIDTH // 2 - 90 + i * 42
            pygame.draw.rect(screen, (70, 70, 80), pygame.Rect(bar_x, 83, 10, 135))

        # Efeito de luz piscando
        if self.flicker_intensity > 0:
            flicker_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flicker_overlay.fill((0, 0, 0, int(100 * self.flicker_intensity)))
            screen.blit(flicker_overlay, (0, 0))

        # Mensagem atual
        if self.scene_phase < len(self.messages):
            current_display = self.messages[self.scene_phase][:int(self.typing_index)]
            message_surf = self.message_font.render(current_display, True, self.dirty_white)

            # Fundo escuro para o texto
            text_bg = pygame.Surface((message_surf.get_width() + 20, message_surf.get_height() + 10))
            text_bg.fill((0, 0, 0))
            text_bg.set_alpha(180)
            screen.blit(text_bg, (SCREEN_WIDTH // 2 - message_surf.get_width() // 2 - 10,
                                  SCREEN_HEIGHT - 180))

            # Texto
            screen.blit(message_surf, (SCREEN_WIDTH // 2 - message_surf.get_width() // 2,
                                       SCREEN_HEIGHT - 175))

            # Indicador de "pressione qualquer tecla" quando mensagem completa
            if self.message_complete:
                continue_text = self.small_font.render("Pressione qualquer tecla para continuar...",
                                                       True, self.dirty_white)
                screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                            SCREEN_HEIGHT - 130))

        # Efeito de "piscar os olhos"
        if self.blink_state:
            blink_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            blink_surface.fill((0, 0, 0))
            screen.blit(blink_surface, (0, 0))

        # Fade in no início
        if self.fade_in:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0))

        # Renderiza overlay de transição se necessário
        if self.transitioning:
            transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            transition_surface.fill((0, 0, 0))

            # Adiciona linhas horizontais distorcidas
            line_count = int(self.transition_alpha / 10)
            for _ in range(line_count):
                y_pos = int((_ / line_count) * SCREEN_HEIGHT)
                line_width = random.randint(1, 3)
                line_offset = random.randint(-10, 10) if random.random() < 0.3 else 0
                pygame.draw.line(
                    transition_surface,
                    (100, 0, 0),  # Linha vermelha
                    (0 + line_offset, y_pos),
                    (SCREEN_WIDTH + line_offset, y_pos),
                    line_width
                )

            # Adiciona estática na transição
            for _ in range(int(self.transition_alpha * 30)):
                x = random.randint(0, SCREEN_WIDTH - 1)
                y = random.randint(0, SCREEN_HEIGHT - 1)
                color = random.randint(0, 100)
                transition_surface.set_at((x, y), (color, 0, 0))  # Estática vermelha

            transition_surface.set_alpha(self.transition_alpha)
            screen.blit(transition_surface, (0, 0))