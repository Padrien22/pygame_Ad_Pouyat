import pygame
import random


class Obstacles(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # crée les parametres de la boule
        self.image = pygame.image.load('assets/pelotte.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 100)
        self.rect.y = 0
        self.velocity = random.randint(1, 3)

    def move(self):
        # deplace la boule de droite a gauche
        self.rect.x += self.velocity

        if self.rect.x < 0 or self.rect.x > 540:
            self.velocity *= -1

    def move_down(self):
        # permet de deplacer vers le bas la boule
        self.rect.y += 2
        if self.rect.y > 740:
            self.kill()

class Obstacles_1(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # crée les parametres de la boule
        self.image = pygame.image.load('assets/cactus.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 100)
        self.rect.y = 200
        self.velocity = random.randint(1, 3)

    def move(self):
        # deplace la boule de droite a gauche
        self.rect.x += self.velocity

        if self.rect.x < 0 or self.rect.x > 540:
            self.velocity *= -1

    def move_down(self):
        # permet de deplacer vers le bas la boule
        self.rect.y += 2
        if self.rect.y > 740:
            self.kill()
