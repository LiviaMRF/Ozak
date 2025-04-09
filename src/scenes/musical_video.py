import cv2
from settings import *
import os

class MusicalVideo:

    def __init__(self):
        self.video = cv2.VideoCapture("assets"+os.sep+"video"+os.sep+"bad_apple.mp4")
        self.sound = pygame.mixer.Sound("assets"+os.sep+"music"+os.sep+"bad_apple.mp3")
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

