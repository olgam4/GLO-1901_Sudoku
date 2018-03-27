#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Programme principal du jeu
"""
__auteur__ = "LOLAB97"
__date__ = "16-10-23"
__coequipiers__ = "OLGAM4", "GUBIA1"  # mettre None si aucun coéquipier

# Importation des modules standards
import os
import tkinter as tk
import argparse
# Importation des modules locaux
import grille_de_jeu as gdj
import resolvateur as res
import affichage as aff
import tkinter as tk


# Definition d'une fonction simple
def cls():
    """ Fait la mise à zéro du terminal selon le système d'eploitation de l'utilisateur

    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def lecture_fichier(source):
    """ Lit un fichier de grilles de sudoku

    :param source: emplacement du fichier à lire
    :type source: str
    :return: liste de grilles dans le fichier
    :rtype: List[str]
    """
    contenu = ''
    with open(source, 'r') as fichier:
        contenu += fichier.read().replace('\n', '').replace(' ', '')
    try:
        if len(contenu) % 81 != 0:
            raise ValueError()
    except ValueError:
        print("Le fichier ne contient pas exclusivement de grille valide.")
        return None
    liste_grilles = list(map(''.join, zip(*[iter(contenu)]*81)))
    return liste_grilles

if __name__ == "__main__":
    # Définition des arguments d'initialisation
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['auto', 'manuel'], default='manuel',
                    help="Choix du mode de fonctionnement du jeu.")
    ap.add_argument('--interface', choices=['textuel', 'graphique'], default='textuel',
                    help="Choix de l'affichage du jeu.")
    ap.add_argument('nom_de_fichier', help='Nom du fichier texte contenant la ou les grilles de jeu.', type=str)
    args = ap.parse_args()

    # Création de la liste de grilles
    listeGrilles = lecture_fichier(args.nom_de_fichier)

    # Actions selon les argumetns saisis lors du démarage
    if args.interface == 'textuel':
        # Actions au cas où l'utilisateur choici l'interface textuelle
        if args.mode == 'manuel':
            # Actions au cas où l'utilisateur choici le mode manuel

            # Initialisation de l'objet GrilleDeJeu avec la grille de jeu choisie
            grille = gdj.GrilleDeJeu(listeGrilles[0])

            # Création de la grille solution
            solver = res.Solution(grille.chaine_grille)
            solver.resoudre()

            # Misa à zéro du terminal et affichage de la grille
            cls()
            print('Sudoku!\n\nVoici votre grille :\n')
            print(grille)

            while grille.chaine_grille != str(solver):
                colonne = input('\nVeuillez saisir le numéro de colonne de la valeur à modifier : ')

                # Validation de la variable colonne de la valeur à modifier
                if len(colonne) != 1 and not colonne.isdigit() and int(colonne) <= 0:
                    print('\nLe numéro de colonne choisi n\'est pas valide.'
                          'Veuillez saisir un valeur entre 1 et 9...')

                else:
                    ligne = input('Veuillez saisir le numéro de ligne de la valeur à modifier : ')

                    # Validation de la variable colonne de la valeur à modifier
                    if len(ligne) != 1 and not ligne.isdigit() and int(ligne) <= 0:
                        print('\nLe numéro de ligne choisi n\'' +
                              'est pas valide. Veuillez saisir un valeur entre 1 et 9...')

                    else:

                        # Validation de la position à modifier
                        if grille.grille_validation[int(ligne)-1][int(colonne)-1]:
                            invalide = True

                            while invalide:
                                valeur = input('Veuillez saisir la nouvelle valeur : ')

                                # Validation de la valeur
                                if len(valeur) == 1 and valeur.isdigit() and int(valeur) > 0:
                                    invalide = False
                                    grille[(int(ligne)*int(colonne))-1] = valeur

                                else:
                                    print('\nLa valeur choisie n\'est pas valide.' +
                                          ' Veuillez saisir une valeur entre 1 et 9...')

                            cls()
                            print('Sudoku!\n\nVoici votre grille :\n')
                            print(grille)

                        else:
                            print('\nLa valeur dans la position choisie est non modifiable...')

            # Message lorsque la grille complétée est égale à la grille solution
            print('\nVictoire!')

        else:
            # Actions au cas où l'utilisateur choici le mode automatique
            compteur = 0

            # Boucle pour l'affichage des chaines de grilles de solution
            for grille in listeGrilles:
                compteur += 1
                if len(listeGrilles) > 0:
                    print('\nSolution de la grille ' + str(compteur) + '/' + str(len(listeGrilles)) + ' :\n')
                grilleResolue = res.Solution(grille)
                grilleResolue.resoudre()
                print(grilleResolue)
    else:
        # Actions au cas où l'utilisateur choici l'interface graphique
        root = tk.Tk()
        if args.mode == 'manuel':
            # Actions au cas où l'utilisateur choici le mode manuel

            # Initialisation de la classe SudokuUI pour l'affichage graphique en manuel
            gameInstance = aff.SudokuUI(gdj.GrilleDeJeu(listeGrilles[0]), master=root)
        else:
            # Actions au cas où l'utilisateur choici le mode automatique

            # Initialisation de la classe SudokuUI pour l'affichage graphique en automatique à partir
            # de la liste des étapes de solution
            grilleResolue = res.Solution(listeGrilles[0])
            grilleResolue.resoudre()
            gameInstance = aff.SudokuUI(grilleResolue.solutions, master=root)
        gameInstance.master.title("Sudoku")
        gameInstance.mainloop()
        root.destroy()
