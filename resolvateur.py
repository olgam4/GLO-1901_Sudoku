#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Module permettant la résolution d'une grille de sudoku.
"""
__auteur__ = "LOLAB97"
__date__ = "16-11-14"
__coequipiers__ = "OLGAM4", "GUBIA1"  # mettre None si aucun coéquipier


# Definition d'une classe en Python
class Solution:
    """Forme une solution d'une grille de sudoku 9x9
    self.resoudre résoud la grille selon les différentes méthodes implémentées
    self.recursion trouve par récursion toutes les solutions possibles de la grille (Attention, lent!!!)
    """
    chaine = ''
    separateur = '.'
    solutions = []

    def __init__(self, chainedejeu):
        """ Initialise une solution de sudoku

        :param chainedejeu: grille avec laquelle initialiser la solution. Doit être de 81 caractères
        :type chainedejeu: str
        """
        if len(chainedejeu) != 81 or not isinstance(chainedejeu, str):
            raise ValueError()
        self.chaine = chainedejeu

    def __getitem__(self, idx):
        """ Quand solutions est une liste d'étapes, retourne l'étape indiquée

        :param idx: indice de l'étape voulue
        :type idx: int
        :return: étape spécifiée par l'indice
        :rtype: str
        """
        try:
            if isinstance(self.solutions, list):
                return self.solutions[idx]
            else:
                raise TypeError("Erreur, l'attribut soutions est de type: ", type(self.solutions))
        except Exception as erreur:
            print(erreur)

    def __setitem__(self, key, value):
        """ Ne fait rien, il est imposible de modifier manuellement une solution

        :param key:mati
        :type key:
        :param value:
        :type value:
        """
        try:
            raise NotImplementedError("Il est impossible d'assigner une valeur à une solution")
        except Exception as erreur:
            print(erreur)

    def __str__(self):
        """ Affichage de la solution si elle est trouvée, différents messages autrement.

        :return: affichage de la solution trouvée si applicable
        :rtype:
        """
        if isinstance(self.solutions, set):  # resultat de self.recursion()
            return "Toutes les solutions possibles sont:" + str(self.solutions)

        elif isinstance(self.solutions, type(None)):
            return "Pas de solutions trouvée"

        elif isinstance(self.solutions, list):
            try:
                return str(self.solutions[-1])
            except IndexError:
                return "Une solution n'est pas encore trouvée.\n" \
                       "Il faut utiliser la méthode resoudre() pour trouver une solution"
        else:  # l'attribut solution doit être de type set, list, ou NoneType
            raise TypeError("Erreur, l'attribut solutions est de type: " + str(type(self.solutions)))

    def resoudre(self):
        """ Résoud la grille

        :return: solution de la grille
        :rtype: List[str]
        """
        self.solution_dirigee()
        return self.solutions

    def solution_dirigee(self):
        """ Algorithme de resolution de sudoku par méthodes.

        :return:
        :rtype: None
        """
        etapes = []

        def _solution_dirigee(chaine):
            """ Implementation  de résolution par semi-récursivité

            :param chaine: chaine à résoudre
            :type chaine: str
            :return: solution actuelle
            :rtype: Tuple[bool, str]
            """
            if chaine.find('.') == -1:
                return True, chaine

            # Trouve les candidats pour la grille
            candidats = self._trouver_candidats(chaine)

            # Solution evidente (1 seul candidat dans la case)
            chaine_mod = self._trouver_cases_resolues(chaine, candidats)
            if chaine_mod is None:
                return None
            elif chaine_mod != chaine:
                chaine = chaine_mod
                solution = _solution_dirigee(chaine)
                if solution is None:
                    return None
                elif solution[0]:
                    etapes.append(chaine)  # Ou mettre une fonction "prive" _sauve_etape
                    return solution

            # Solution cachee (candidats dans la case > 1,
            # mais dans la ligne/colonne/secteur, un nombre ne peut aller qu'a un endroit)
            chaine_mod = self._trouver_simples_caches(chaine, candidats)
            if chaine_mod is None:
                return None
            elif chaine_mod != chaine:
                chaine = chaine_mod
                solution = _solution_dirigee(chaine)
                if solution is None:
                    return None
                elif solution[0]:
                    etapes.append(chaine)  # Ou mettre une fonction "prive" _sauve_etape
                    return solution

            # Besoin de faire un "guess"
            candidat_court = (0, 10)  # Premier membre du tuple est l'indice et le second le nombre de candidats
            for clef, elus in candidats.items():
                if len(elus) < candidat_court[1]:
                    candidat_court = (clef, len(elus))

            i = candidat_court[0]
            for elu in candidats[i]:
                solution = _solution_dirigee(chaine[:i] + elu + chaine[i+1:])
                if solution is None:
                    continue
                elif solution[0]:
                    etapes.append(chaine)  # Ou mettre une fonction "prive" _sauve_etape
                    return solution
            else:
                return None
        resultat = _solution_dirigee(self.chaine)
        etapes.append(self.chaine)
        solutions = list(reversed(etapes))
        if resultat is None:
            self.solutions = None
        elif resultat[0]:
            if not solutions:
                solutions.append(resultat[1])
            # solutions.append(resultat[1])
            self.solutions = solutions
            # print('la solution est "' + resultat[1] + '"')
            # print("pour l'appeller, self.solutions[-1]")

    def _trouver_simples_caches(self, chaine, candidats):
        """ Méthode interne (ne devrait pas être utilisée).

        Pour une chaine et un dictionnaire de candidats donnés,
        retourne une chaine où les candidats n'ayant qu'une case possible se voient attribués à cette case.

        Si un candidat n'a qu'une case possible selon les lignes, colonnes ou secteurs,
        que le même candidat a aussi une case différente où les mêmes critères indiquent qu'il ne peux aller que là,
        et que ces deux cases sont reliés, cela implique que le même candidat doit être dans deux cases différentes
        reliées.
        Retourne None pour indiquer que la grille n'as pas de solution valide.

        Exemple: les lignes indiquent que '1' doit être dans les cases d'indice 0 et 27.
        Les cases d'indices 0 et 27 sont dans la même colonne, la grille est invalide.

        :param chaine: grille sur laquelle appliquer l'algorithme
        :type chaine: str
        :param candidats: dictionnaire de possibilités pour la grille
        :type candidats: Dict[int, List[str]]
        :return: chaine modifiée si algorithme le permet
        :rtype: str
        """
        simples = {}
        for i in candidats.keys():
            simple_l = set(candidats[i])
            simple_c = set(candidats[i])
            simple_s = set(candidats[i])
            for j in candidats.keys():
                if (self._m_lig(i, j)) and (i != j):
                    simple_l.difference_update(set(candidats[j]))
                if (self._m_col(i, j)) and (i != j):
                    simple_c.difference_update(set(candidats[j]))
                if (self._m_sec(i, j)) and (i != j):
                    simple_s.difference_update(set(candidats[j]))
                if len(simple_l) == len(simple_c) == len(simple_s) == 0:
                    break
            if len(simple_l) == 1:
                simples[i] = simple_l.pop()
            elif len(simple_c) == 1:
                simples[i] = simple_c.pop()
            elif len(simple_s) == 1:
                simples[i] = simple_s.pop()
        for i in simples:
            for j in simples:
                if (self._relies(i, j)) and (i != j):
                    if simples[i] == simples[j]:
                        return None
        for i, elu in simples.items():
            chaine = chaine[:i] + elu + chaine[i+1:]
        return chaine

    def _trouver_cases_resolues(self, chaine, candidats):
        """ Méthode interne (ne devrait pas être utilisée).

        Pour une chaine et un dictionnaire de candidats donnés,
        retourne une chaine où les cases n'ayant qu'un candidat possible sont remplies de ce candidat.

        Si une case non résolue n'a pas de candidats possible, ou si deux cases reliées n'ont que le même candidat
        possible, retourne None pour indiquer que la grille n'as pas de solution valide.

        :param chaine: grille sur laquelle appliquer l'algorithme
        :type chaine: str
        :param candidats: dictionnaire de possibilités pour la grille
        :type candidats: Dict[int, List[str]]
        :return: chaine modifiée si algorithme le permet
        :rtype: str
        """
        resolues = {}
        for i, elu in candidats.items():
            if len(elu) == 1:
                resolues[i] = elu[0]
            elif len(elu) == 0:
                return None
        for i in resolues:
            for j in resolues:
                if (self._relies(i, j)) and (i != j):
                    if resolues[i] == resolues[j]:
                        return None
        for i, elu in resolues.items():
            chaine = chaine[:i] + elu[0] + chaine[i+1:]
        return chaine

    def _trouver_candidats(self, chaine):
        """ Méthode interne (ne devrait pas être utilisée).

        Pour une grille donnée, retourne un dictionnaire des candidats possibles pour chaque case.

        :param chaine: grille sur laquelle appliquer l'algorithme
        :type chaine: str
        :return: dictionnaire de possibilités pour la grille
        :rtype: Dict[int, List[str]]
        """
        candidats = {}
        for i in range(81):
            if chaine[i] == self.separateur:
                candidats[i] = []
                non_voulues = set()
                for j in range(81):
                    if self._relies(i, j):
                        non_voulues.add(chaine[j])

                for elu in '123456789':
                    if elu not in non_voulues:
                        candidats[i].append(elu)
        return candidats

    def recursion(self):
        """ Résoud la grille de façon récursive et met un ensemble de toutes
        les solutions possibles dans l'attribut de classe self.solutions.

        Si la grille n'as pas de solution, cet attribut de classe se voit assigner la valeur None.

        **ATTENTION, TRÈS LENT**

        """
        solutions = []

        def _recursion(chaine):
            nonlocal solutions

            i = chaine.find('.')
            if i == -1:
                solutions.append(chaine)

            non_voulues = set()
            for j in range(81):
                if self._relies(i, j):
                    non_voulues.add(chaine[j])

            for elu in '123456789':
                if elu not in non_voulues:
                    _recursion(chaine[:i] + elu + chaine[i+1:])
        _recursion(self.chaine)
        if len(solutions) == 0:
            self.solutions = None
            # print('aucune solution trouvee')
        elif len(solutions) == 1:
            self.solutions = set(solutions)
            # print('1 seule solution trouvee')
        elif len(solutions) > 1:
            self.solutions = set(solutions)
            # print("plus d'une solution trouvee")

    def _relies(self, i, j):
        """ Teste si des indices de grille de sudoku i et j sont reliés

        :param i: indice i
        :type i: int
        :param j: indice j
        :type j: int
        :return: résultat du test
        :rtype: bool
        """
        return self._m_lig(i, j) or self._m_col(i, j) or self._m_sec(i, j)

    @staticmethod
    def _m_lig(i, j):
        """ Teste si l'index i est dans la même ligne que l'index j

        :param i: indice i
        :type i: int
        :param j: indice j
        :type j: int
        :return: résultat du test
        :rtype: bool
        """
        return i // 9 == j // 9

    @staticmethod
    def _m_col(i, j):
        """ Teste si l'index i est dans la même colone que l'index j

        :param i: indice i
        :type i: int
        :param j: indice j
        :type j: int
        :return: résultat du test
        :rtype: bool
        """
        return i % 9 == j % 9

    @staticmethod
    def _m_sec(i, j):
        """ Teste si l'index i est dans le même secteur que l'index j

        :param i: indice i
        :type i: int
        :param j: indice j
        :type j: int
        :return: résultat du test
        :rtype: bool
        """
        return (i % 9//3 + i//27*3) == (j % 9//3 + j//27*3)
