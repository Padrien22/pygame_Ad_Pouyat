import pygame
from game import Game

pygame.mixer.pre_init(88200, -16, 2, 512)
pygame.init()
pygame.mixer.init()


# charger la fonction game
game = Game()

# initialisation de la fenetre de jeu
screen = pygame.display.set_mode((620, 720))
pygame.display.set_caption("Jumpy Cat")

# charger le background
background = pygame.image.load("assets/backgroundspace.png")
background = pygame.transform.scale(background, (620, 720))
background_rect = background.get_rect()
background_rect.x = 0
background_rect.y = 0

# variable utilisée dans le jeu
game.running = True
game.deplacement_du_chat = "en attente"
sense_du_jouer = True
aficher_credi = False
en_pause = False
donne_son_nom = False


# jeu lancé
while game.running:

    # metre le son
    game.sound_manager.play('ambiance')

    # appliquer l'image du joueur
    screen.blit(background, background_rect)
    if aficher_credi:
        game.accueil.aficher_credi(screen)
        game.accueil.credi_rect.x = 200
        screen.blit(game.accueil.credi_image, game.accueil.credi_rect)
    else:
        # verifier si notre jeu a commencé ou non
        if game.is_playing:
            # declencher les instructions de la partie
            game.update(screen)
            # appliquer l'image du bouton pose
            screen.blit(game.image, game.rect)
            if en_pause:
                game.pause(screen)
        elif not game.novel_partie:
            # ajouter l'ecran de bienvenue
            screen.blit(game.accueil.plays_image, game.accueil.plays_rect)
            screen.blit(game.accueil.son_image, game.accueil.son_rect)
            game.accueil.credi_rect.x = 100
            font = pygame.font.SysFont("monospace", 25)
            text_pseudo = font.render(f"Donner un pseudo :", True, (250, 250, 250))
            if donne_son_nom:
                text_nom = font.render(f"{game.niveaux.nom_du_joueur}", True, (0, 0, 0))
                pygame.draw.rect(screen, (250, 250, 250), [200, 200, 200, 30])
                screen.blit(text_nom, (200, 200))
            else:
                pygame.draw.rect(screen, (80, 77, 71), [200, 200, 200, 30])
            screen.blit(game.accueil.credi_image, game.accueil.credi_rect)
            screen.blit(text_pseudo, (180, 150))

        else:
            game.game_over(screen)
    if game.running:
        pygame.display.flip()

        for event in pygame.event.get():
            # quitter le jeu
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_souris, y_souris = pygame.mouse.get_pos()
                if game.is_playing:

                    if en_pause:
                        if game.rect.collidepoint(event.pos):
                            # metre le jeux en pose
                            en_pause = False
                        if game.accueil.son_rect.collidepoint(event.pos):
                            # le son du jeux est couper ou activer
                            game.accueil.son()
                        if game.accueil.credi_rect.collidepoint(event.pos):
                            # permet d'aficher les credit
                            if aficher_credi:
                                aficher_credi = False
                            else:
                                aficher_credi = True
                    else:
                        if game.rect.collidepoint(event.pos):
                            # metre le jeux en pose
                            en_pause = True
                        else:
                            # permet de calculer la trajectoire
                            game.deplacement_du_chat = "afficher la trajectoire"
                            game.colision_premier = False

                if not game.is_playing:
                    if 200 < x_souris < 400 and 200 < y_souris < 230:
                        donne_son_nom = True
                    if game.accueil.plays_rect.collidepoint(event.pos):
                        donne_son_nom = False
                    # verification pour savoir si la souris clique sur un bouton
                    if game.accueil.plays_rect.collidepoint(event.pos):
                        # mettre le jeu en mode "lancé"
                        game.start()
                    if game.accueil.son_rect.collidepoint(event.pos):
                        # le son du jeux est couper ou activer
                        game.accueil.son()
                    if game.accueil.credi_rect.collidepoint(event.pos):
                        # permet d'aficher les credit
                        if aficher_credi:
                            aficher_credi = False
                        else:
                            aficher_credi = True

            elif event.type == pygame.MOUSEBUTTONUP:
                game.deplacement_du_chat = "lancer le chat"
                game.position_du_chat = 0
                game.tombe = False
                game.sound_manager.play('saut')
                if game.niveaux.score > 2:
                    game.niveaux.dif()
            elif event.type == pygame.KEYDOWN:
                if donne_son_nom:
                    if event.unicode == '\r':
                        donne_son_nom = False
                    elif event.unicode == ' ':
                        game.niveaux.nom_du_joueur = ""
                    elif event.unicode == '\x08':
                        sup = game.niveaux.nom_du_joueur
                        game.niveaux.nom_du_joueur = ""
                        for i in range(len(sup) - 1):
                            game.niveaux.nom_du_joueur += sup[i]
                    else:
                        game.niveaux.nom_du_joueur += event.unicode
