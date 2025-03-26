class Animation:
    def __init__(self, frames, speed=0.1):
        if isinstance(frames, list):  # Verifica se é lista
            self.frames = frames
        else:  # Se for uma única Surface
            self.frames = [frames]  # Converte em lista com um único frame

        self.speed = speed
        self.current_frame = 0
        self.time = 0

    def update(self, dt):
        if len(self.frames) > 1:  # Só anima se tiver múltiplos frames
            self.time += dt
            if self.time >= self.speed:
                self.time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def current_image(self):
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.time = 0