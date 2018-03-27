#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Affichage d'une grille Sudoku dans un UI qui permet l'affichage automatique ou manuel.
Mise à jour en temps réel de la grille selon les entrées données.
"""
__auteur__ = "OLGAM4"
__date__ = "16-12-14"
__coequipiers__ = "LOLAB97", "GUBIA1"  # mettre None si aucun coéquipier

# Importation des modules standards
from tkinter import *
# Importation des modules locaux
import resolvateur as rslv
from grille_de_jeu import GrilleDeJeu as Gdj


# Definition d'une classe en Python
class SudokuUI(Frame):
    """Classe encapsulant l'affichage graphique d'un sudoku

    """
    def __init__(self, grille, master=None):
        """ Initialise la fenêtre du Sudoku avec une grille et détermine la hiéarchie de classe.

        :param grille: Grille d'initialisation
        :type grille: grille_de_jeu.GrilleDeJeu
        :param master:
        :type master: tkinter.Tk
        """
        Frame.__init__(self, master)
        if isinstance(grille, Gdj):
            self.grilleDeJeu = grille
            self.grilleActuelle = grille
            self.grilleDeJeuRésolue = self.__resoudre_grille(grille.chaine_grille)
            self.pack()
            self.__init_menu()
        if isinstance(grille, list):
            self.etapeid = 0
            self.etapes = grille
            self.grilleDeJeu = grille[0]
            self.pack()
            self.__monter_etapes()

    def __monter_etapes(self):
        """ Montre les étapes directement une à une en cliquant.

        :return:
        :rtype: None
        """
        self.nbDeClics = 0

        # Création du canvas grille, on lui donne les entrées Clic droit et touche du clavier.
        self.grille = Canvas(self, width=740, height=740, bg='whitesmoke')
        self.grille.pack(fill=BOTH, expand=1)
        self.grille.bind("<Button-1>", self.__click)
        self.grille.bind("<Key>", self.__entrée)

        # Construction et remplissage de la grille
        self.__construire_grille()
        self.__remplir_grille()

        # Création du bouton Quitter
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quitter"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "bottom"}, fill=BOTH)

        # Création du bouton Next
        self.ETAPE = Button(self)
        self.ETAPE["text"] = "Voir la prochaine étape"
        self.ETAPE["command"] = self.__prochaine_etape
        self.ETAPE.pack({"side": "bottom"}, fill=BOTH)

        # Création du bouton sauter à la fin
        self.FIN = Button(self)
        self.FIN["text"] = "Voir la solution"
        self.FIN["command"] = self.__voir_solution
        self.FIN.pack({"side": "bottom"}, fill=BOTH)

    def __prochaine_etape(self):
        """ Permet de modifier la grille avec l'étape subséquente quand le bouton ETAPE est appuyé.

        :return:
        :rtype: None
        """

        etapeid = self.etapeid
        chaine0 = self.etapes[etapeid]
        etapeid += 1
        chaine1 = self.etapes[etapeid]
        diff_ids = self.__different(chaine0, chaine1)
        for idx in range(81):
            # Vérifie chaque élément de l'étape présente et le met en bleu s'il est nouveau
            textid = self.text[idx]
            if idx in diff_ids:
                self.grille.itemconfigure(textid, text=chaine1[idx], fill='blue')
            else:
                self.grille.itemconfigure(textid, fill='black')

        if etapeid == len(self.etapes) - 2:
            # Érradication la dernière étape pour l'affichage
            self.ETAPE.destroy()
        self.etapeid = etapeid

    def __voir_solution(self):
        """ Permet de sauter directement à la solution finale.

        :return:
        :rtype:
        """

        self.ETAPE.destroy()
        for idx in range(81):
            # Mettre chaque élément de la grille égal à l'index de la chaine de caractère finale
            textid = self.text[idx]
            self.grille.itemconfigure(textid, text=self.etapes[-1][idx], fill='black')
        self.FIN.destroy()

    @staticmethod
    def __different(chaine1, chaine2):
        """ Compare deux chaines de caractères et retourne les indices des différences

        :param chaine1: première chaine à tester
        :type chaine1: str
        :param chaine2: deuxième chaine à tester
        :type chaine2: str
        :return: ensemble des différences
        :rtype: object
        """
        diff_ids = set()
        for idx in range(81):
            if chaine1[idx] != chaine2[idx]:
                diff_ids.add(idx)
        return diff_ids

    def __init_menu(self):
        """ Initialise le menu en mode manuel

        :return:
        :rtype:
        """

        # Création du canvas du menu et l'image du menu
        self.menu = Canvas(self, width=740, height=416)
        self.menu.pack(fill=BOTH, expand=1)
        self.imgMenu = PhotoImage(file='./menu.png')
        self.menu.create_image(370, 208, image=self.imgMenu)

        # Création du bouton jouer qui pointe à _init_jeu
        self.START = Button(self)
        self.START["text"] = "Jouer"
        self.START["command"] = self.__init_jeu
        self.START.pack({"side": "left"}, fill=BOTH, expand=1)

        # Création du bouton Quitter
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quitter"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "right"}, fill=BOTH, expand=1)

    def __init_jeu(self):
        """ Initialise le jeu

        :return:
        :rtype:
        """

        # Remettet les variables nécessaires à zéro ou vide et effacer ce qu'il y avait dans le menu
        self.nbDeClics = 0
        self.START.destroy()
        self.QUIT.destroy()
        self.menu.pack_forget()
        self.grilleDeJeuPrésente = {}
        self.caseChoisie = False
        self.case = ''

        # Création du canvas de la grille en lui donnant encore le bind de click et touche du clavier
        self.grille = Canvas(self, width=740, height=740, bg='whitesmoke')
        self.grille.pack(fill=BOTH, expand=1)
        self.grille.bind("<Button-1>", self.__click)
        self.grille.bind("<Key>", self.__entrée)

        # Dessine la grille et lui ajoute les chiffres initiaux
        self.__construire_grille()
        self.__remplir_grille()

        # Création du bouton Quitter
        self.RETOUR = Button(self)
        self.RETOUR["text"] = "Quitter"
        self.RETOUR["command"] = self.quit
        self.RETOUR.pack({"side": "bottom"}, fill=BOTH)

        # Création du boutton tester
        self.TESTER = Button(self)
        self.TESTER["text"] = "Tester la grille"
        self.TESTER["command"] = self.__tester_grille
        self.TESTER.pack({"side": "bottom"}, fill=BOTH)

        # Création du bouton effacer
        self.EFFACER = Button(self)
        self.EFFACER["text"] = "Effacer la grille"
        self.EFFACER["command"] = self.__effacer_grille
        self.EFFACER.pack({"side": "bottom"}, fill=BOTH)

    def __construire_grille(self):
        """ Construit la grille en dessinant les lignes sur le canvas

        :return:
        :rtype: None
        """

        # Si la ligne est de contour, la met noire et épaisse, et si elle sépare les cases, grise et mince
        self.padding = 20
        for i in range(10):
            if i % 3 == 0:
                color, width = 'black', 3
            else:
                color, width = 'gray', 1

            # Point de départ de chaque ligne, le padding + la largeur d'une case * l'indice en x et le padding en y
            x1 = self.padding + i * 700/9
            y1 = self.padding

            # Point d'arrivée de chaque ligne, soit même en x, car les lignes sont verticales 700 pixels plus bas
            x2 = x1
            y2 = 700 + self.padding
            self.grille.create_line(x1, y1, x2, y2, fill=color, width=width)

            # Point d'arrivée et de départ inversés pour les lignes horizontales
            x1 = self.padding
            y1 = self.padding + i * 700/9
            x2 = 700 + self.padding
            y2 = y1
            self.grille.create_line(x1, y1, x2, y2, fill=color, width=width)

    def __remplir_grille(self):
        """ Remplit la grille des nombres initiaux qu'il y a dans le sudoku

        :return:
        :rtype: None
        """

        self.original = {}
        self.text = {}
        for idx in range(81):
            i = idx // 9
            j = idx % 9
            # Pour chaque élément, point fixe au centre de chaque case d'index 0-80
            x = self.padding + 700/(2*9) + 700/9 * j
            y = self.padding + 700/(2*9) + 700/9 * i
            # Si ce n'est pas un élément vide, ajout de cet élément à la grille de jeu actuelle
            # Si ajout, création d'une instance de texte aux coordonnées
            # contenant le nombre lié à la grille originale
            if self.grilleDeJeu[idx] != '.':
                self.initiales = self.grilleDeJeu[idx]
                self.original[idx] = True
            else:
                self.original[idx] = False
                self.initiales = ' '
            textid = self.grille.create_text(x, y, text=self.initiales, tags=("original", str(x), str(y)),
                                             fill="black", font=('Helvetica', 20, 'bold'))
            self.text[idx] = textid

    def __tester_grille(self):
        """ Teste la grille pour la résolution et change l'affichage en conséquence.

        :return:
        :rtype: None
        """
        reponse = ''
        for idx in range(81):
            if self.grilleDeJeu[idx] != '.':
                self.grilleDeJeuPrésente[idx] = self.grilleDeJeu[idx]
        for clé in sorted(self.grilleDeJeuPrésente):
            reponse += self.grilleDeJeuPrésente[clé]
        if len(reponse) != 81:
            self.TESTER["text"] = "Vous devez remplir la grille! Tester"
        elif reponse == self.grilleDeJeuRésolue:
            self.__victoire()
        else:
            self.TESTER["text"] = "Vous n'avez pas la bonne réponse. Tester"

    def __effacer_grille(self):
        """ Remmet la grille de jeu à son état initial

        :return:
        :rtype: None
        """
        self.grilleDeJeuPrésente = {}
        for idx in range(80):
            textid = self.text[idx]
            if not self.original[idx]:
                self.grille.itemconfigure(textid, text=' ', fill='black')
                self.grilleActuelle[idx] = '.'
            else:
                self.grille.itemconfigure(textid, fill='black')

    def __click(self, event):
        """ Détecte si clic de l'utilisateur est dans une position valide.

        :param event:
        :type event:
        :return:
        :rtype: None
        """
        # Si ce n'est pas la première fois qu'il y a un clic, effacer le dernier encadré
        if self.nbDeClics != 0:
            self.grille.delete(self.encadré2, self.encadré4, self.encadré3, self.encadré1)

        # Mise à jour de l'emplacement du clic
        x = event.x
        y = event.y

        # Si le click est dans le canvas, mettre le focus sur le canvas grille
        if self.padding < x < self.padding + 700 and self.padding < y < self.padding + 700:
            self.grille.focus_set()
            for idx in range(81):
                i = idx // 9
                j = idx % 9
                self.case = idx
                # Si cette case ne contient pas un élément original
                if not self.original[idx]:
                    self.xPrésent1 = self.padding + 700 / 9 * j
                    self.xPrésent2 = self.padding + 700 / 9 * (j+1)
                    self.yPrésent1 = self.padding + 700 / 9 * i
                    self.yPrésent2 = self.padding + 700 / 9 * (i+1)
                    # Vérification de la case exacte cliquée
                    if self.xPrésent1 < x < self.xPrésent2 and self.yPrésent1 < y < self.yPrésent2:
                        # Création d'un encadré à cette case avec des lignes rouges et mise à jour du booléen
                        # indiquant qu'une case est choisie.
                        self.caseChoisie = True
                        self.nbDeClics += 1
                        self.encadré1 = self.grille.create_line(self.xPrésent1, self.yPrésent1, self.xPrésent1 +
                                                                700 / 9, self.yPrésent1, fill="red", width=4)
                        self.encadré2 = self.grille.create_line(self.xPrésent1, self.yPrésent1, self.xPrésent1,
                                                                self.yPrésent1 + 700 / 9, fill="red", width=4)
                        self.encadré3 = self.grille.create_line(self.xPrésent2, self.yPrésent2,
                                                                self.xPrésent2 - 700 / 9, self.yPrésent2, fill="red",
                                                                width=4)
                        self.encadré4 = self.grille.create_line(self.xPrésent2, self.yPrésent2,
                                                                self.xPrésent2, self.yPrésent2 - 700 / 9, fill="red",
                                                                width=4)
                        return
                    else:
                        # Si la case contient un élément original ou si le click n'est pas dans une case, mise à jour
                        # du booléen indiquant qu'aucune case est choisie
                        self.caseChoisie = False
                else:
                    self.caseChoisie = False

    def __entrée(self, event):
        """ Change une valeur de la grille si ce changement est valide

        :param event:
        :type event:
        :return:
        :rtype: None
        """
        if event.char in ' 123456789' and self.caseChoisie:

            # Vérification de la case choisie et changement de sa valeur
            idx = self.case
            self.grilleDeJeuPrésente[idx] = event.char

            # Changement de sa valeur affichée pour être conforme avec ce que l'utilisateur écrit
            self.grilleActuelle[idx] = event.char
            textid = self.text[idx]
            self.grille.itemconfigure(textid, text=event.char, fill='blue', font=('Helvetica', 20, 'normal'))

            # Vérification de s'il y a un changement à faire sur la couleur des nombres
            self.__nombres_en_rouge()

    def __nombres_en_rouge(self):
        """ Met en rouge tous les nombres qui sont identiques ET sur la même ligne, colonne ou bloc

        :return:
        :rtype: None
        """

        # Création d'un set qui contient tous éléments avec leur index qui soit sur le même nombre sur la même
        # ligne, colonne ou bloc
        en_rouge = self.__verifier()
        # Changement de la couleur du texte lié à ces éléments qui ne sont pas bons selon le fait qu'ils soient
        # valides : BLEU ou NOIR(Si original)
        # invalides : ROUGE
        for idx in range(81):
            textid = self.text[idx]
            if idx in en_rouge:
                self.grille.itemconfigure(textid, fill='red')
            else:
                if self.original[idx]:
                    self.grille.itemconfigure(textid, fill='black')
                else:
                    self.grille.itemconfigure(textid, fill='blue')

    def __verifier(self):
        """ Vérifie que pour une ligne, colonne ou bloc, il n'y ait pas deux fois le même nombre

        :return: non_valides
        :rtype: set
        """
        non_valides = set()
        for i in range(81):
            for j in range(81):
                # Pour chaque élément de la grille pris avec un autre, vérification de liaison
                # Si oui, ajout au set de non valide
                if self.__relies(i, j) and i != j:
                    if self.grilleActuelle[i] == self.grilleActuelle[j]:
                        non_valides.add(i)
                        non_valides.add(j)
        return non_valides

    def __victoire(self):
        """ Montre la banière de victoire

        :return:
        :rtype: None
        """

        # Destruction de l'affichage du jeu
        self.TESTER.destroy()
        self.RETOUR.destroy()
        self.EFFACER.destroy()
        self.grille.pack_forget()

        # Création de l'image de victoire dans un canevas
        self.victoire = Canvas(self, width=740, height=416)
        self.victoire.pack(fill=BOTH, expand=1)
        self.imgVictoire = PhotoImage(file='./victoire.png')
        self.victoire.create_image(370, 208, image=self.imgVictoire)

        # Création du boutton qui quitte une fois la victoire accomplie
        self.VICTOIRE = Button(self)
        self.VICTOIRE["text"] = "Bravo!"
        self.VICTOIRE["command"] = self.quit
        self.VICTOIRE.pack({"side": "bottom"}, fill=BOTH)

    @staticmethod
    def __resoudre_grille(grille):
        """ Résoud la grille initiale à l'usage de test pour la validation

        :param grille:
        :type grille:
        :return: solution
        :rtype: str
        """

        # Appel aux fonctions du resolvateur pour solutionner la grille qui lui est donnée
        solution = rslv.Solution(grille)
        solution.resoudre()
        return str(solution)

    @staticmethod
    def __relies(i, j):
        """ Teste si i est un index de grille de sudoku relié a l'indexe j.

        :param i: premier index dans la grille
        :type i: int
        :param j: deuxième index dans la grille
        :type j: int
        :return: booléen représentant la liaison des deux indexes
        :rtype: bool
        """
        return i // 9 == j // 9 or i % 9 == j % 9 or (i % 9 // 3 + i // 27 * 3) == (j % 9 // 3 + j // 27 * 3)
