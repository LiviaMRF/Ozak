class Animation:
    def __init__(self, frames, speed):
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.time = 0

    def update(self, dt):
        self.time += dt
        if self.time >= self.speed:
            self.time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def current_image(self):
        return self.frames[self.current_frame]