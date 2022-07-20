import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {
            'saut': pygame.mixer.Sound("assets/saut.mp3"),
            'ambiance': pygame.mixer.Sound("assets/son_ambiance.ogg"),
        }


    def play(self, name):
        self.sounds[name].play()
