# creation des niveau du jeux
class Niveaux:

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.score = 0
        self.dif_tire = 0
        self.passer_le_niveau = 0
        self.game_score = []
        self.top_score = []
        self.lignes = []
        self.nom = []
        self.nom_du_joueur = ""
        self.sauve_garder = True

    def dif(self):
        if self.passer_le_niveau == 0:
            self.niveau_1()
        elif self.passer_le_niveau == 1 and self.score % 5 == 0 and self.score % 15 != 0:
            self.niveau_2()
        elif self.passer_le_niveau == 2 and self.score % 10 == 0:
            self.niveau_3()
        elif self.passer_le_niveau == 3 and self.score % 15 == 0:
            self.niveau_4()

    def niveau_1(self):
        if self.game.player.indice > 3:
            self.game.player.indice -= 2
            if self.game.player.indice < 13:
                self.passer_le_niveau += 1
        else:
            self.passer_le_niveau += 1

    def niveau_2(self):
        # aparition des premier obstacle
        self.game.spawn_obstacles(0)
        self.game.spawn_obstacles(- 400)
        self.niveau_1()

    def niveau_3(self):
        self.game.spawn_obstacles_1(100)
        self.game.spawn_obstacles_1(- 500)
        self.niveau_1()

    def niveau_4(self):
        self.game.spawn_obstacles_1(100)
        self.game.spawn_obstacles_1(- 500)
        self.game.spawn_obstacles(0)
        self.game.spawn_obstacles(- 400)
        self.niveau_1()
        self.passer_le_niveau = 1

    def lire_txt(self, sup):
        self.lignes = []
        scrore_total = open('score.txt', "r")
        for ligne in scrore_total:
            self.lignes.append(ligne)
        self.top_score = str(self.lignes[1]).split(",")
        if not sup:
            self.game_score = str(self.lignes[3]).split(",")
        self.nom = str(self.lignes[5]).split(",")

        for i in range(len(self.top_score)):
            self.top_score[i] = int(self.top_score[i])
        if not sup:
            for i in range(len(self.game_score)):
                if self.game_score[0] != "\n":
                    if i == len(self.game_score):
                        self.game_score[i] = int((self.game_score[i]).split("\n"))
                    else:
                        self.game_score[i] = int(self.game_score[i])
                else:
                    self.game_score = []

    def enregistrer(self, sup):
        # enregistrer les score
        self.lire_txt(sup)
        # on ajoute a la liste des score de la party le nouveau score a sa place :
        poser = True
        i = 0
        while poser:
            if sup:
                poser = False
            elif len(self.game_score) == 0:
                self.game_score.append(self.score)
            elif i == len(self.game_score):
                if self.score != self.game_score[i-1]:
                    self.game_score.append(self.score)
                poser = False
            elif self.score > self.game_score[i]:
                if self.score != self.game_score[i-1]:
                    self.game_score.insert(i, self.score)
                    self.game_score.pop()
                poser = False
            else:
                i += 1
        # on ajoute a la liste des top score le nouveau score a sa place :
        poser = True
        i = 0
        while poser:
            if i == len(self.top_score):
                poser = False
            elif self.score >= self.top_score[i]:
                if self.score != self.top_score[i]:
                    self.top_score.insert(i, self.score)
                    self.nom.insert(i, self.nom_du_joueur)
                    self.nom.pop(len(self.nom)-1)
                    self.top_score.pop(len(self.top_score)-1)
                poser = False
            else:
                i += 1

        i = 0
        # trasformer en texte :
        text_game = ""
        if len(self.game_score) != 0:
            for i in range(len(self.game_score) - 1):
                text_game += str(self.game_score[i]) + ","
            text_game += str(self.game_score[i]) + "\n"
        else:
            text_game = "\n"

        text_top = ""
        for i in range(len(self.top_score) - 1):
            text_top += str(self.top_score[i]) + ","
        text_top += str(self.top_score[i + 1]) + "\n"

        text_nom = ""
        for i in range(len(self.nom) - 1):
            text_nom += str(self.nom[i]) + ","
        text_nom += str(self.nom[i + 1])

        # modifier le fichier .txt :
        scrore_total = open('score.txt', "w")
        text = self.lignes[0] + text_top + self.lignes[2] + text_game + self.lignes[4] + text_nom
        scrore_total.write(text)
        scrore_total.close()

