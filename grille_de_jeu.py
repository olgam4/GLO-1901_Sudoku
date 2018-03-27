#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Module qui définit la structure de la grille de jeu
"""
__auteur__ = "GUBIA1"
__date__ = "16-11-13"
__coequipiers__ = "LOLAB97", "OLGAM4"  # mettre None si aucun coéquipier


# Definition d'une classe en Python
class GrilleDeJeu:
    """ Classe de la grille de jeu principale
    """
    chaine_grille = ''
    grille = []
    grille_validation = []
    separateur = '.'

    def __init__(self, chaine_jeu):
        """ Initialise la grille de jeu

        :param chaine_jeu: grille d'initialisation
        :type chaine_jeu: str
        """
        self.chaine_jeu_orig = chaine_jeu
        self.chaine_grille = chaine_jeu
        self.grille = [[self.separateur]*9 for i in range(9)]
        self.grille_validation = [[''] * 9 for i in range(9)]
        for i in range(0, 9):
            for j in range(0, 9):
                self.grille_validation[i][j] = not chaine_jeu[i * 9 + j].isdigit()

                if chaine_jeu[i*9 + j].isdigit():
                    self.grille[i][j] = int(chaine_jeu[i*9 + j])

    def __getitem__(self, idx):
        """ Donne valeur à la position désirée

        :param idx: indice dans la grille
        :type idx: int
        :return: valeur voulue
        :rtype: str
        """
        return self.chaine_grille[idx]

    def __setitem__(self, idx, valeur):
        """ Assigne la valeur à la position dans la grille

        :param idx: indice dans la grille
        :type idx: int
        :param valeur: valeur souhaitée
        :type valeur: str
        """
        if not isinstance(valeur, str):
            raise TypeError("La valeur n'est pas un caractère")
        elif not len(valeur) == 1:
            raise ValueError("La valeur doit être un caractère unique")
        else:
            self.grille[idx//9][idx % 9] = valeur
            self.chaine_grille = self.chaine_grille[:idx] + valeur + self.chaine_grille[idx + 1:]

    def __str__(self):
        """ Affichage de la grille

        :return:
        :rtype: None
        """
        chaine = '    1 2 3   4 5 6   7 8 9 \n  +-------+-------+-------\n'
        for i in range(0, 9):
            chaine += str(i+1) + ' |'
            for j in range(0, 3):
                for k in range(0, 3):
                    if j == 0 and k == 0:
                        chaine += ' '
                    chaine += str(self.grille[i][j*3 + k]) + ' '
                if j < 2:
                    chaine += '| '
                elif i != 8:
                    chaine += '\n'
            if (i + 1) % 3 == 0 and i != 8:
                chaine += '  +-------+-------+-------\n'
        return chaine
