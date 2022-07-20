import pygame
import random


# creation des boites sur lesquelles le chat saute
class Box(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # crée les parametres de la boite
        self.image = pygame.image.load('assets/boite.png')
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect()
        # permet d'attribuer des positions aléatoires aux boites
        self.rect.x = random.randint(0, 520)
        self.rect.y = 200

    def move(self):
        # permet de déplacer la boite vers le bas
        self.rect.y += 2
        if self.rect.y > 740:
            self.rect.y = 0
