import pygame


# creation des boites sur lesquelles le chat saute
class Accuil:

    def __init__(self):
        super().__init__()
        # crée la page de d'accuil
        # bouton plays
        self.plays_image = pygame.image.load("assets/start_button.png")
        self.plays_image = pygame.transform.scale(self.plays_image, (200, 100))
        self.plays_rect = self.plays_image.get_rect()
        self.plays_rect.x = 200
        self.plays_rect.y = 300
        # bouton credi
        self.credi_image = pygame.image.load("assets/credits.png")
        self.credi_image = pygame.transform.scale(self.credi_image, (200, 100))
        self.credi_rect = self.credi_image.get_rect()
        self.credi_rect.x = 100
        self.credi_rect.y = 500
        # bouton son
        self.son_image = pygame.image.load("assets/son_on.png")
        self.son_image = pygame.transform.scale(self.son_image, (100, 100))
        self.son_rect = self.son_image.get_rect()
        self.son_rect.x = 400
        self.son_rect.y = 500
        self.son_playing = True

    def son(self):
        if self.son_playing:
            self.son_image = pygame.image.load("assets/son_off.png")
            self.son_image = pygame.transform.scale(self.son_image, (100, 100))
            self.son_playing = False
            pygame.mixer.pause()
        else:
            self.son_image = pygame.image.load("assets/son_on.png")
            self.son_image = pygame.transform.scale(self.son_image, (100, 100))
            self.son_playing = True
            pygame.mixer.unpause()

    def aficher_credi(self, screen):
        # aficher le texte
        font = pygame.font.SysFont("monospace", 30)
        score_text = font.render(f" Realisé par : ", True, (250, 250, 250))
        screen.blit(score_text, (150, 50))
        score_text = font.render(f" Adrien POUYAT ", True, (250, 250, 250))
        screen.blit(score_text, (150, 150))
        score_text = font.render(f" Edgar LUONG ", True, (250, 250, 250))
        screen.blit(score_text, (150, 200))
        score_text = font.render(f" Ines EL GAROUANI ", True, (250, 250, 250))
        screen.blit(score_text, (150, 250))
        score_text = font.render(f" Pierre BONNIN ", True, (250, 250, 250))
        screen.blit(score_text, (150, 300))
        score_text = font.render(f" Luka RADOVANOVIC ", True, (250, 250, 250))
        screen.blit(score_text, (150, 350))
