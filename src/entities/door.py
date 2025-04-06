from settings import *


class Door(pygame.sprite.Sprite):
    def __init__(self, boundary, side, target_scene):
        super().__init__()

        # Configurações da porta
        self.width = 60
        self.height = 100
        self.side = side  # "right", "left", "top", "bottom"
        self.target_scene = target_scene
        self.interaction_radius = 70

        # Cria a superfície da porta
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_door()

        # Posiciona relativo ao boundary
        self.boundary = boundary
        self._reposition()

    def _draw_door(self):

        pygame.draw.rect(self.image, (150, 75, 0), (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, (200, 150, 50), (0, 0, self.width, self.height), 3)

    def _reposition(self):

        if self.side == "right":
            self.rect = self.image.get_rect(
                left=self.boundary.rect.right - self.width,
                centery=self.boundary.rect.centery
            )
        elif self.side == "left":
            self.rect = self.image.get_rect(
                right=self.boundary.rect.left + self.width,
                centery=self.boundary.rect.centery
            )

    def update(self):
        self._reposition()