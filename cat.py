import pygame
import time


# classe joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        # on appelle la fonction game
        self.game = game
        # variables de la barre d'endurance
        self.stamina_max = 100
        self.stamina = 100
        # pour le joueur
        self.image = pygame.image.load("assets/chat_dans_boite.png")
        self.image = pygame.transform.scale(self.image, (100, 75))
        self.rect = self.image.get_rect()
        self.rect.x = 210
        self.rect.y = 550  # positions du sprite
        # pour la trajectoire
        self.point = pygame.image.load("assets/unknown.png")
        self.point = pygame.transform.scale(self.point, (20, 10))
        # liste qui enregistre la trajectoire du chat
        self.traject_du_chat = []
        self.indice = 15

    def stamina_variation(self):
        # vitesse a laquelle le chat perd de la vie
        self.stamina -= 0.025
        # permet de verifier si la barre n'est pas à 0
        if self.stamina < 0:
            self.game.is_playing = False

    def update_stam_bar(self, surface):
        # dessiner la barre de stamina
        pygame.draw.rect(surface, (80, 77, 71), [self.rect.x + 30, self.rect.y - 20, self.stamina_max, 8])
        pygame.draw.rect(surface, (113, 226, 34), [self.rect.x + 30, self.rect.y - 20, self.stamina, 8])

    def jump(self, i, screen):
        # permet de deplacer le joueur
        self.rect.x = i[0] - 50
        self.rect.y = i[1] - 50
        # pemet de verifier si le chat n'est pas sorti du cadre
        if self.rect.y > screen.get_height() + 30 or -170 > self.rect.x or self.rect.x > screen.get_width() + 100:
            self.game.is_playing = False

    def formule(self, x, debut, x_v, y_v, screen):
        # formule physique utilisée pour calculer la trajectoire
        t = (x - debut) / x_v
        # on met G = 10 ; m = 1
        y = int((y_v * t) - ((1 / 2) * 1 * 10 * (t ** 2)))
        # adapte le resulta au systeme inverser de pygme du grillage
        y = screen.get_height() - y - screen.get_height() + self.rect.y
        return y

    def trajectoire(self, screen, x_souris, y_souris):
        self.image = pygame.image.load("assets/chat_elan_boite.png")
        self.image = pygame.transform.scale(self.image, (100, 75))
        # permet d'initialiser le vecteur qui s'applique sur le chat :
        # force ; sens ; direction
        self.traject_du_chat = []
        if y_souris < self.rect.y:
            y_v = self.rect.y - y_souris
            x_v = x_souris - (self.rect.x + 90)

        else:
            y_v = y_souris - self.rect.y
            x_v = (self.rect.x + 90) - x_souris

        # permet de s'assurer qu'il n'y a pas de trop importante et inutile appliqué
        if x_v == 0:
            x_v = 1
        elif x_v > 40:
            x_v = 40
        elif x_v < -40:
            x_v = -40
        # recentre le calcul
        debut = self.rect.x + 90
        if x_v > 0:
            for x in range(0, screen.get_width() + 200):
                if x % x_v/5 == 0:
                    y = self.formule(x, debut, x_v, y_v, screen)
                    if debut < x:
                        # permet d'afficher seulement une partie de la trajectoire
                        if len(self.traject_du_chat) < self.indice:
                            screen.blit(self.point, (x, y))
                        # permet d'enregistrer les positions que l'on veut que le chat prenne
                        self.traject_du_chat.append((x, y))
        else:
            for x in range(screen.get_width(), -400, -1):
                if x % x_v/5 == 0:
                    y = self.formule(x, debut, x_v, y_v, screen)
                    if debut > x:
                        # permet d'afficher seulement une partie de la trajectoire
                        if len(self.traject_du_chat) < self.indice:
                            screen.blit(self.point, (x, y))
                        # permet d'enregistrer les positions que l'on veut que le chat prenne
                        self.traject_du_chat.append((x, y))
