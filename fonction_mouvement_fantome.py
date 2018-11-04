#!/usr/bin/env python3

import random

def move_adv(coord_pacman, coord_fantome, carte, type_ia):
    """
    Cette fonction traduit la direction de mouvement du fantôme (haut, bas etc)
    en coordonnées dans la matrice
    """
    direction_adv = choix_ia(coord_pacman, coord_fantome, carte, type_ia)
    if coord_fantome[0]-1 >= 0 \
    and direction_adv == 'z' \
    and carte[coord_fantome[0]-1][coord_fantome[1]] != 1:
        return coord_fantome[0]-1, coord_fantome[1]
    elif coord_fantome[0]+1 < len(carte) \
    and direction_adv == 's' \
    and carte[coord_fantome[0]+1][coord_fantome[1]] != 1:
        return coord_fantome[0]+1, coord_fantome[1]
    elif coord_fantome[1]-1 >= 0 \
    and direction_adv == 'q' \
    and carte[coord_fantome[0]][coord_fantome[1]-1] != 1:
        return coord_fantome[0], coord_fantome[1]-1
    elif coord_fantome[1]+1 < len(carte[0]) \
    and direction_adv == 'd' \
    and carte[coord_fantome[0]][coord_fantome[1]+1] != 1:
        return coord_fantome[0], coord_fantome[1]+1
    return coord_fantome[0], coord_fantome[1]

def choix_mov_rand(coord_fantome, carte):
    """
    Cette fonction choisis aléatoirement une direction de déplacement pour les fantôme
    """
    while True:
        choix = random.choice(['up', 'down', 'right', 'left'])

        if choix == 'up':
            if coord_fantome[0]-1 >= 0 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] not in [1, 6, 7, 8, 9]:
                return 'z'
            else:
                continue
        if choix == 'down':
            if coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] not in [1, 6, 7, 8, 9]:
                return 's'
            else:
                continue
        if choix == 'left':
            if coord_fantome[1]-1 >= 0 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] not in [1, 6, 7, 8, 9]:
                return 'q'
            else:
                continue
        if choix == 'right':
            if coord_fantome[1]+1 < len(carte[0]) \
            and  carte[coord_fantome[0]][coord_fantome[1]+1] not in [1, 6, 7, 8, 9]:
                return 'd'
            else:
                continue
        if carte[coord_fantome[0]-1][coord_fantome[1]] in [1, 6, 7, 8, 9] \
        and carte[coord_fantome[0]+1][coord_fantome[1]] in [1, 6, 7, 8, 9] \
        and carte[coord_fantome[0]][coord_fantome[1]-1] in [1, 6, 7, 8, 9] \
        and carte[coord_fantome[0]][coord_fantome[1]+1] in [1, 6, 7, 8, 9]:
            return 'none'

def choix_mov_fuite(coord_pacman, coord_fantome, carte):
    """
    Choix mouvement fantome de maniere brute, on considere fantomes comme des obstacles
    """
    if coord_pacman[0] > coord_fantome[0] \
    and (abs(coord_fantome[0]-coord_pacman[0]) >= abs(coord_fantome[1]-coord_pacman[1])):
        #si le joueur est au dessus et plus loin verticalement
        if coord_fantome[0]-1 >= 0 and carte[coord_fantome[0]-1][coord_fantome[1]] != 1 \
        and carte[coord_fantome[0]-1][coord_fantome[1]] < 6:
            # si il n'y a pas de mur sur le chemin
            return 'z'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] < 6:
                #S'il coord_pacman[1] a un mur a gauche
                return 'd'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] < 6:
                #S'il coord_pacman[1] a un mur a droite
                return 'q'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]-1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]+1] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]-1] >= 6):
                return 's'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1:
                #Il n'y a pas de mur ni a droite ni a gauche
                choix = random.choice(['q', 'd'])
                return choix # Au hasard a droite ou a gauche

    if coord_pacman[0] < coord_fantome[0] \
    and (abs(coord_fantome[0]-coord_pacman[0]) >= abs(coord_fantome[1]-coord_pacman[1])):
        #si le joueur est en dessous et plus loin verticalement
        if coord_fantome[0]+1 < len(carte) \
        and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
        and carte[coord_fantome[0]+1][coord_fantome[1]] < 6:
            # si il n'y a pas de mur sur le chemin
            return 's'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] < 6:
                #S'il coord_pacman[1] a un mur a gauche
                return 'd'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] < 6:
                #S'il coord_pacman[1] a un mur a droite
                return 'q'
            elif  coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]+1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]+1] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]-1] >= 6):
                return 'z'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1:
                #Il n'y a pas de mur ni a droite ni a gauche
                choix = random.choice(['q', 'd'])
                return choix # Au hasard a droite ou a gauche

    if coord_pacman[1] < coord_fantome[1] \
    and (abs(coord_fantome[1]-coord_pacman[1]) > abs(coord_fantome[0]-coord_pacman[0])):
        #si le joueur est à droite et plus loin horizontalement
        if coord_fantome[1]+1 < len(carte[0]) \
        and carte[coord_fantome[0]][coord_fantome[1]+1] != 1 \
        and carte[coord_fantome[0]][coord_fantome[1]+1] < 6:
            # si il n'y a pas de mur sur le chemin
            return 'd'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en haut
                return 's'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and  carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en bas
                return 'z'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]-1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]+1] >= 6) \
            and (carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]+1][coord_fantome[1]] >= 6):
                return 'a'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1:
                #Il n'y a pas de mur ni en haut ni en bas
                choix = random.choice(['s', 'z'])
                return choix # Au hasard en haut ou en bas

    if coord_pacman[1] > coord_fantome[1] \
    and (abs(coord_fantome[1]-coord_pacman[1]) > abs(coord_fantome[0]-coord_pacman[0])):
        #si le joueur est à gauche
        if coord_fantome[1]-1 >= 0 and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
        and carte[coord_fantome[0]][coord_fantome[1]-1] < 6:
            # si il n'y a pas de mur sur le chemin
            return 'q'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en haut
                return 's'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en bas
                return 'z'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]-1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]-1] >= 6) \
            and (carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]+1][coord_fantome[1]] >= 6):
                return 'd'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1:
                #Il n'y a pas de mur ni en haut ni en bas
                choix = random.choice(['s', 'z'])
                return choix # Au hasard en haut ou en bas

def choix_mov(coord_pacman, coord_fantome, carte):
    """
    Choix mouvement fantome de maniere brute, on considere fantomes comme des obstacles
    coord_pacman[0] et coord_pacman[1]: coordonnées actuelles
    coord_fantome[0] et coord_fantome[1]: coordonnées considérées
    """
    if coord_pacman[0] < coord_fantome[0] \
    and (abs(coord_fantome[0]-coord_pacman[0]) >= abs(coord_fantome[1]-coord_pacman[1])):
        #si le joueur est au dessus et plus loin verticalement
        if coord_fantome[0]-1 >= 0 and carte[coord_fantome[0]-1][coord_fantome[1]] != 1 \
        and carte[coord_fantome[0]-1][coord_fantome[1]] < 6:
            # si il n'y a pas de mur sur le chemin
            return 'z'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] < 6:
                #S'il coord_pacman[1] a un mur a gauche
                return 'd'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] < 6:
                #S'il coord_pacman[1] a un mur a droite
                return 'q'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]-1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]+1] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]-1] >= 6):
                return 's'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1:
                #Il n'y a pas de mur ni a droite ni a gauche
                choix = random.choice(['q', 'd'])
                return choix # Au hasard a droite ou a gauche

    if coord_pacman[0] > coord_fantome[0] \
    and (abs(coord_fantome[0]-coord_pacman[0]) >= abs(coord_fantome[1]-coord_pacman[1])):
        #si le joueur est en dessous et plus loin verticalement
        if coord_fantome[0]+1 < len(carte) and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
        and carte[coord_fantome[0]+1][coord_fantome[1]] < 6:
            # si il n'y a pas de mur sur le chemin
            return 's'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] < 6:
                #S'il coord_pacman[1] a un mur a gauche
                return 'd'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]-1] < 6:
                #S'il coord_pacman[1] a un mur a droite
                return 'q'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]+1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]+1] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]-1] >= 6):
                return 'z'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
            and carte[coord_fantome[0]][coord_fantome[1]+1] != 1:
                #Il n'y a pas de mur ni a droite ni a gauche
                choix = random.choice(['q', 'd'])
                return choix # Au hasard a droite ou a gauche

    if coord_pacman[1] > coord_fantome[1] \
    and (abs(coord_fantome[1]-coord_pacman[1]) > abs(coord_fantome[0]-coord_pacman[0])):
        #si le joueur est à droite et plus loin horizontalement
        if coord_fantome[1]+1 < len(carte[0]) \
        and carte[coord_fantome[0]][coord_fantome[1]+1] != 1 \
        and carte[coord_fantome[0]][coord_fantome[1]+1] < 6:
            # si il n'y a pas de mur sur le chemin
            return 'd'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en haut
                return 's'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en bas
                return 'z'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]-1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]+1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]+1] >= 6) \
            and (carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]+1][coord_fantome[1]] >= 6):
                return 'a'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1:
                #Il n'y a pas de mur ni en haut ni en bas
                choix = random.choice(['s', 'z'])
                return choix # Au hasard en haut ou en bas

    if coord_pacman[1] < coord_fantome[1] \
    and (abs(coord_fantome[1]-coord_pacman[1]) > abs(coord_fantome[0]-coord_pacman[0])):
        #si le joueur est à gauche
        if coord_fantome[1]-1 >= 0 and carte[coord_fantome[0]][coord_fantome[1]-1] != 1 \
        and carte[coord_fantome[0]][coord_fantome[1]-1] < 6:
            # si il n'y a pas de mur sur le chemin
            return 'q'
        else:# Il coord_pacman[1] a un mur sur le chemin
            if coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]+1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en haut
                return 's'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] < 6:
                #S'il coord_pacman[1] a un mur en bas
                return 'z'
            elif coord_fantome[1]-1 >= 0 and coord_fantome[1]+1 < len(carte[0]) \
            and coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and (carte[coord_fantome[0]-1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]-1][coord_fantome[1]] >= 6) \
            and (carte[coord_fantome[0]][coord_fantome[1]-1] == 1 \
            or carte[coord_fantome[0]][coord_fantome[1]-1] >= 6) \
            and (carte[coord_fantome[0]+1][coord_fantome[1]] == 1 \
            or carte[coord_fantome[0]+1][coord_fantome[1]] >= 6):
                return 'd'
            elif coord_fantome[0]-1 >= 0 and coord_fantome[0]+1 < len(carte) \
            and carte[coord_fantome[0]+1][coord_fantome[1]] != 1 \
            and carte[coord_fantome[0]-1][coord_fantome[1]] != 1:
                #Il n'y a pas de mur ni en haut ni en bas
                choix = random.choice(['s', 'z'])
                return choix # Au hasard en haut ou en bas

def choix_ia(coord_pacman, coord_fantome, carte, type_ia):
    """
    Cette fonction permet d'allouer a chaque fantôme son algorithme en
    fonction de son niveau de difficulté
    """
    if type_ia == 1:
        if carte[coord_fantome[0]][coord_fantome[1]] == 6:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 7:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 8:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 9:
            return choix_mov_rand(coord_fantome, carte)

    if type_ia == 2:
        if carte[coord_fantome[0]][coord_fantome[1]] == 6:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 7:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 8:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 9:
            return choix_mov(coord_pacman, coord_fantome, carte)
    if type_ia == 3:
        if carte[coord_fantome[0]][coord_fantome[1]] == 6:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 7:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 8:
            return choix_mov(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 9:
            return choix_mov(coord_pacman, coord_fantome, carte)
    if type_ia == 4:
        if carte[coord_fantome[0]][coord_fantome[1]] == 6:
            return choix_mov_rand(coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 7:
            return choix_mov(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 8:
            return choix_mov(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 9:
            return choix_mov(coord_pacman, coord_fantome, carte)
    if type_ia == 5:
        if carte[coord_fantome[0]][coord_fantome[1]] == 6:
            return choix_mov(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 7:
            return choix_mov(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 8:
            return choix_mov(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 9:
            return choix_mov(coord_pacman, coord_fantome, carte)
    if type_ia == 6:
        if carte[coord_fantome[0]][coord_fantome[1]] == 6:
            return choix_mov_fuite(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 7:
            return choix_mov_fuite(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 8:
            return choix_mov_fuite(coord_pacman, coord_fantome, carte)
        if carte[coord_fantome[0]][coord_fantome[1]] == 9:
            return choix_mov_fuite(coord_pacman, coord_fantome, carte)
