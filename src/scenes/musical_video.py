import cv2
from settings import *
import os

class MusicalVideo:

    def __init__(self):
        video_path = os.path.join("..", "assets", "video", "bad_apple.mp4")
        self.video = cv2.VideoCapture(video_path)
        sound_path = os.path.join("..", "assets", "music", "bad_apple.mp3")
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.set_volume(0.5)
        self.sound.play(loops=0)

    def update(self, screen):
        success, video_image = self.video.read()

        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
            screen.blit(video_surf, (0, 0))
        else:
            screen.fill(BLACK)

    def end_music(self):
        self.sound.set_volume(0)

