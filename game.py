import pygame
from obstacles import Obstacles
from obstacles import Obstacles_1
from cat import Player
from boxes import Box
import random
from sounds import SoundManager
from accueil import Accuil
from niveau_du_jeux import Niveaux


class Game:

    def __init__(self):
        # on appelle la fonction player
        self.player = Player(self)
        # on appelle la fonction SoundManager
        self.sound_manager = SoundManager()
        # on appelle la fonction accueil
        self.accueil = Accuil()
        # on appelle la fonction Niveaux
        self.niveaux = Niveaux(self)

        # savoire si une partie a commencer :
        self.novel_partie = False
        # permet de savoir si le jeu est en route
        self.is_playing = False

        # groupe d'obstacles
        self.all_obstacles = pygame.sprite.Group()
        self.all_obstacles_1 = pygame.sprite.Group()

        # groupe de box
        self.all_box = pygame.sprite.Group()

        # afficher le bouton pose
        self.image = pygame.image.load("assets/pelotte.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 540
        self.rect.y = 0  # positions du sprite

        self.naming = False
        self.donne_son_nom = False

        # initialise toutes les variable qui vont être utilisées
        # savoir si on cherche la trajectoire, le chat saute, ou rien
        self.deplacement_du_chat = "en attente"
        # permet d'aller cherhcer dans la liste la position qui nous interesse au fur et à mesure
        self.position_du_chat = 0
        # permet d'empêcher les collisions alors que le chat monte
        self.tombe = False
        # pour savoir quand est la premiere fois qu'il y a une collision
        self.colision = 0
        # perdre de la vie une fois si le chat touche une boule
        self.predre_de_la_vie = 0
        # savoir si il y a eu une colition
        self.colision_true = False
        # commenser a charger le jeux
        self.running = False
        self.colision_premier = False

    def check_collision_pour_les_boite(self, sprite, group):
        # permet de savoir si il y a une collision entre une image et un groupe et que le sprite est superieur au groupe

        for group_sprite in group.sprites():
            if pygame.sprite.collide_mask(sprite, group_sprite):
                if sprite.rect.y < group_sprite.rect.y and self.tombe:
                    sprite.rect.y = group_sprite.rect.y - 19
                    sprite.rect.x = group_sprite.rect.x + 8
                    group_sprite.rect.y -= 700
                    group_sprite.rect.x = random.randint(0, 520)
                    self.colision_true = True

    def check_collision(self, sprite, group):
        # pemet de savoir si il y a une collision entre une image et un groupe
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_obstacles(self, hauteur):
        # crée un obstacle dans le jeu
        obstacles = Obstacles()
        obstacles.rect.y = hauteur
        self.all_obstacles.add(obstacles)

    def spawn_obstacles_1(self, hauteur):
        # crée un obstacle dans le jeu
        obstacles = Obstacles_1()
        obstacles.rect.y = hauteur
        self.all_obstacles_1.add(obstacles)

    def spawn_box(self, hauteur):
        # crée une boite dans le jeu
        box = Box()
        box.rect.y = hauteur
        self.all_box.add(box)

    def deplacer_le_jeux(self):
        # permet de deplacer tous les éléments du jeu
        # pour donner l'impression que le chat monte
        for Une_box in self.all_box:
            Une_box.move()
        for Un_Obstacles in self.all_obstacles:
            Un_Obstacles.move_down()
        for Un_Obstacles in self.all_obstacles_1:
            Un_Obstacles.move_down()
        self.player.rect.y += 2

    def update(self, screen):
        # afficher le score
        font = pygame.font.SysFont("monospace", 16)
        score_text = font.render(f"Score : {self.niveaux.score}", True, (250, 250, 250))
        screen.blit(score_text, (20, 20))

        # appliquer l'image du joueur
        screen.blit(self.player.image, self.player.rect)

        # actualiser la barre de vie du joueur
        self.player.update_stam_bar(screen)
        self.player.stamina_variation()

        # appliquer les images du groupe d'obstacles
        self.all_obstacles.draw(screen)
        self.all_obstacles_1.draw(screen)

        for Un_Obstacles in self.all_obstacles:
            Un_Obstacles.move()
        for Un_Obstacles in self.all_obstacles_1:
            Un_Obstacles.move()

        # appliquer les images du groupe des box
        self.all_box.draw(screen)

        # collision avec une boule:
        if self.check_collision(self.player, self.all_obstacles):
            self.player.stamina -= 0.1
        if self.check_collision(self.player, self.all_obstacles_1):
            if not self.colision_premier:
                self.niveaux.score -= 1
                self.colision_premier = True

        # pour deplacer le chat
        if self.deplacement_du_chat == "afficher la trajectoire":
            self.colision = 0
            x_souris, y_souris = pygame.mouse.get_pos()  # position du curseur
            self.player.trajectoire(screen, x_souris, y_souris)
            self.colision_true = False
        # si la trajectoire a été decidée alors :
        if self.deplacement_du_chat == "lancer le chat" or self.deplacement_du_chat == "en attente":
            self.check_collision_pour_les_boite(self.player, self.all_box)
            if self.tombe and self.colision_true:
                self.player.image = pygame.image.load("assets/chat_dans_boite.png")
                self.player.image = pygame.transform.scale(self.player.image, (100, 75))

                # si le chat tombe et qu'il y a collision alors
                # on indique si c'est la première collision avec cet objet
                if self.colision == 1:
                    self.player.stamina += 5
                    self.niveaux.score += 1

                # alors on remet la liste à 0
                self.player.traject_du_chat = []
                # on deplace tout le jeu jusqu'à ce qu'on soit arrivé au bord
                if 550 != self.player.rect.y and 551 != self.player.rect.y:
                    self.colision += 1
                    self.deplacer_le_jeux()
                    self.deplacement_du_chat = "en attente"
                else:
                    # quand on a totalment fini le deplacement du chat, alors on remet tous les parametres a 0
                    self.position_du_chat = 0
                    self.deplacement_du_chat = "en attente"
                    self.tombe = False
                    self.colision_true = False

            elif len(self.player.traject_du_chat) != 0:
                self.player.image = pygame.image.load("assets/chat_saut.png")
                self.player.image = pygame.transform.scale(self.player.image, (100, 75))
                # tant qu'on n'est pas arrivé à la fin de la liste alors on continue de deplacer le chat
                self.player.jump(self.player.traject_du_chat[self.position_du_chat], screen)
                if self.position_du_chat > 1:
                    # si le chat est en deplacement on regarde s'il tombe
                    self.tombe = self.player.traject_du_chat[self.position_du_chat][1] > \
                                 self.player.traject_du_chat[self.position_du_chat - 1][1]
                if self.tombe:
                    self.player.image = pygame.image.load("assets/chat_tombe.png")
                    self.player.image = pygame.transform.scale(self.player.image, (100, 75))
                self.position_du_chat += 1

    def cree_image(self, image_dir, taille, position_x, position_y):
        # permet d'initialiser une image
        # au cas où nous voulons rajouter plus d'images
        image = pygame.image.load(image_dir)
        image = pygame.transform.scale(image, taille)
        image_rect = image.get_rect()
        image_rect.x = position_x
        image_rect.y = position_y
        return image, image_rect

    def start(self):
        self.is_playing = True
        self.novel_partie = True

        # faire apparaître les boites
        self.spawn_box(300)
        self.spawn_box(0)
        self.spawn_box(- 200)

    def reinitialiser(self):

        # nouvelle parti
        self.is_playing = False

        # on met tout à 0
        self.deplacement_du_chat = "en attente"

        # on rememt le chat en position de depard
        self.position_du_chat = 0

        self.tombe = False
        self.colision = 0
        self.predre_de_la_vie = 0
        self.player.traject_du_chat = []
        self.colision_true = False
        self.colision_premier = False

        # on remet la bar de vie du joueur
        self.player.stamina = self.player.stamina_max

        # la longuer de la trajectoire revien a l'origine
        self.player.indice = 15

        # remet le niveux a 0
        self.niveaux.passer_le_niveau = 0

        # réinitialiser les objets
        self.all_box = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        self.all_obstacles_1 = pygame.sprite.Group()
        self.player.rect.x = 210
        self.player.rect.y = 550

    def score_fin(self, screen):
        # importer page modification du son
        self.accueil.son_rect.x = 250
        self.accueil.son_rect.y = 600
        screen.blit(self.accueil.son_image, self.accueil.son_rect)

        # on enregistre le nouveau score
        if self.niveaux.sauve_garder:
            self.niveaux.enregistrer(False)
            self.niveaux.sauve_garder = False

        # afficher le score
        font = pygame.font.SysFont("monospace", 25)
        score_text = font.render(f"Score {self.niveaux.nom_du_joueur} : {self.niveaux.score}", True, (250, 250, 250))
        screen.blit(score_text, (200, 200))

        # afficher scores
        font = pygame.font.SysFont("monospace", 20)
        score_text = font.render(f"Score Party : ", True, (250, 250, 250))
        screen.blit(score_text, (330, 230))
        score_text = font.render(f"Top Score : ", True, (250, 250, 250))
        screen.blit(score_text, (170, 230))

        # afficher les top scores
        for i in range(5):
            if i < len(self.niveaux.game_score):
                score_text = font.render(f"Score : {self.niveaux.game_score[i]}", True, (250, 250, 250))
                screen.blit(score_text, (330, 260 + i * 30))
            score_text = font.render(f"{self.niveaux.nom[i]} : {self.niveaux.top_score[i]}", True, (250, 250, 250))
            screen.blit(score_text, (180, 260 + i * 30))

    def game_over(self, screen):
        # quand cette fonction est appelée elle indique la fin de la partie

        self.reinitialiser()
        self.score_fin(screen)
        self.interaction(screen)

    def donner_pseudo(self, screen):

        # inscrire et afficher son nom
        font = pygame.font.SysFont("monospace", 25)
        text_pseudo = font.render(f"Donner un pseudo :", True, (250, 250, 250))
        screen.blit(text_pseudo, (180, 150))

        if self.donne_son_nom:
            text_nom = font.render(f"{self.niveaux.nom_du_joueur}", True, (0, 0, 0))
            pygame.draw.rect(screen, (250, 250, 250), [200, 200, 200, 30])
            screen.blit(text_nom, (200, 200))
        else:
            pygame.draw.rect(screen, (80, 77, 71), [200, 200, 200, 30])

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_souris, y_souris = pygame.mouse.get_pos()
                if 200 < x_souris < 400 and 200 < y_souris < 230:
                    self.donne_son_nom = True
            elif event.type == pygame.KEYDOWN:
                if self.donne_son_nom:
                    if event.unicode == '\r':
                        self.naming = False
                        self.donne_son_nom = False
                    elif event.unicode == ' ':
                        self.niveaux.nom_du_joueur = ""
                    elif event.unicode == '\x08':
                        sup = self.niveaux.nom_du_joueur
                        self.niveaux.nom_du_joueur = ""
                        for i in range(len(sup) - 1):
                            self.niveaux.nom_du_joueur += sup[i]
                    else:
                        self.niveaux.nom_du_joueur += event.unicode

    def interaction(self, screen):

        # importer page fin de jeux bouton nouvel partie
        novel_partie, novel_partie_rect = self.cree_image("assets/new_game_button.png", (200, 100), 80, 440)
        screen.blit(novel_partie, novel_partie_rect)

        # importer page fin de jeux
        fin_jeux, fin_jeux_rect = self.cree_image("assets/game_over.png", (200, 100), 200, 100)
        screen.blit(fin_jeux, fin_jeux_rect)

        # bouton changer nom
        button_pseudo, button_pseudo_rect = self.cree_image("assets/button.png", (200, 90), 350, 450)
        screen.blit(button_pseudo, button_pseudo_rect)

        # acction a menner
        for event in pygame.event.get():
            # quitter le jeu
            if event.type == pygame.QUIT:
                self.niveaux.game_score = []
                self.niveaux.enregistrer(True)

                self.running = False
                pygame.quit()
            # commencer une nouvel party
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_souris, y_souris = pygame.mouse.get_pos()
                if button_pseudo_rect.collidepoint(event.pos):
                    self.naming = True
                if self.accueil.son_rect.collidepoint(event.pos):
                    # le jeux couper
                    self.accueil.son()
                if novel_partie_rect.collidepoint(event.pos):
                    self.niveaux.sauve_garder = True
                    # clique sur le bouton alors mettre le jeu en mode "lancé"
                    self.start()
                    self.niveaux.score = 0
                    self.player.image = pygame.image.load("assets/chat_dans_boite.png")
                    self.player.image = pygame.transform.scale(self.player.image, (100, 75))

    def pause(self, screen):
        screen.blit(self.accueil.son_image, self.accueil.son_rect)
        self.accueil.credi_rect.x = 100
        screen.blit(self.accueil.credi_image, self.accueil.credi_rect)
        self.player.stamina += 0.025
        ...
