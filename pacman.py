#!/usr/bin/env python3

import tkinter as tk
import sys
import time
import os
from pathlib import Path
import pygame
import numpy as np
from fonction_mouvement_fantome import *
#from gestion_fenetre import *

def affichage_plateau(carte):
    """
    Initialise le plateau dans tkinter à partir d'une matrice
    Cela va créer tout les éléments grpahique
    """
    global pacman
    global red, blue, pink, orange
    global id_liste
    global cotecarre
    id_liste = []

    for x in range(len(carte)):
        coord_x0 = 0
        coord_y0 = 0+(x*cotecarre)
        coord_x1 = cotecarre
        coord_y1 = cotecarre+(x*cotecarre)
        id_listex = []
        for y in range(len(carte[0])):
            if carte[x][y] == 1:
                canevas.create_rectangle(coord_x0, coord_y0, coord_x1, coord_y1, fill='blue', outline='blue')
            elif carte[x][y] == 3:
                #if face == 1: flag de la position
                pacman = canevas.create_arc(coord_x0+1, coord_y0+1, coord_x1-1, coord_y1-1, start=30, extent=300, fill="gold", outline="")#faceright
                #canevas.create_oval(coord_x0+1, coord_y0+1, coord_x1-1, coord_y1-1, fill='yellow', outline='')
            elif carte[x][y] == 0:
                id_listex.append(canevas.create_oval(coord_x0+(cotecarre/3), coord_y0+(cotecarre/3), coord_x1-(cotecarre/3), coord_y1-(cotecarre/3), fill='light yellow', outline=''))
            elif carte[x][y] == 4:
                id_listex.append(canevas.create_oval(coord_x0+(cotecarre/3), coord_y0+(cotecarre/3), coord_x1-(cotecarre/3), coord_y1-(cotecarre/3), fill='dark violet', outline=''))
            elif carte[x][y] == 6:
                red = canevas.create_oval(coord_x0+1, coord_y0+1, coord_x1-1, coord_y1-1, fill='red', outline='')
            elif carte[x][y] == 7:
                pink = canevas.create_oval(coord_x0+1, coord_y0+1, coord_x1-1, coord_y1-1, fill='pink', outline='')
            elif carte[x][y] == 8:
                blue = canevas.create_oval(coord_x0+1, coord_y0+1, coord_x1-1, coord_y1-1, fill='cyan', outline='')
            elif carte[x][y] == 9:
                orange = canevas.create_oval(coord_x0+1, coord_y0+1, coord_x1-1, coord_y1-1, fill='orange', outline='')
            if carte[x][y] not in [0, 4]:
                id_listex.append(0)
            coord_x0 += cotecarre
            coord_x1 += cotecarre
        id_liste.append(id_listex)

def Clavier(event):
    """ Gestion de l'événement Appui sur une touche du clavier """
    global direction
    direction = event.keysym

def pause():
    global direction
    global direction_sauv
    direction_sauv = direction
    direction = 'pause'

def start():
    global direction
    global direction_sauv
    if direction_sauv == ' ':
        move_pac_et_fant()
        direction_sauv = 'lancer'
    elif direction_sauv == 'pause':
        direction=direction_sauv
        move_pac_et_fant()


def checkvie():
    global nombrevie
    global xpac, ypac
    global pacman
    global red, blue, pink, orange
    global cotecarre
    global liste_fant
    global coord_pacman

    if nombrevie<= 0:
        affichage_fenetre_fin(v_ou_d=1)
    else:
        nombrevie-=1
        #On replace pacman
        canevas.delete(pacman)
        carte[x][y] =2
        coord_pacman[0] = xpac
        coord_pacman[1] = ypac
        carte[x][y] =3
        pacman =canevas.create_arc((ypac)*cotecarre+1, (xpac)*cotecarre+1, (ypac+1)*cotecarre-1, (xpac+1)*cotecarre-1, start=300, extent=300, fill="gold", outline="")
        #On replace les fantômes
        for i in liste_fant:
            carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
            i[0], i[1] = i[4], i[5] #On redonne les coord initiales
            carte[i[0]][i[1]] =i[3] # a ces coord initiales, on lui remet sa valeur
            i[6] = 5 #On l'immobilise 30 tours
            if i[3] == 6:
                canevas.delete(red)
                red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
            if i[3] == 7:
                canevas.delete(pink)
                pink = canevas.create_oval(i[5]*cotecarre+1,  i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
            if i[3] == 8:
                canevas.delete(blue)
                blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
            if i[3] == 9:
                canevas.delete(orange)
                orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')


def move_pac_et_fant():
    """
    Mouvement du joueur
    """
    global carte
    global coord_pacman
    global liste_fant
    global pacman
    global cotecarre
    global red, blue, pink, orange
    global id_liste
    global direction
    global compteur_fuite, compteur_tour
    global type_ia
    global sauvegarde_ia
    global score
    global fenetre_jeu
    global Labelscore
    global Labelpower
    global Labelvie
    global nombrevie
    global vitesse

    coord_fantome=[0,0]
    diff = cotecarre
    if direction == 'Down':
        if coord_pacman[0]+1 < len(carte) and carte[coord_pacman[0]+1][coord_pacman[1]] >= 6:
            if type_ia != 6:
                checkvie()
                time.sleep(3)

            else:
                score+=600
                for i in liste_fant:
                    if i[0] == coord_pacman[0]+1 and i[1] == coord_pacman[1]:
                        carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                        i[0], i[1] =i[4], i[5] #On redonne les coord initiales
                        carte[i[0]][i[1]] =i[3] # a ces coord initiales, on lui remet sa valeur
                        i[6] =30 #On l'immobilise 30 tours
                        if i[3] == 6:
                            canevas.delete(red)
                            red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                        if i[3] == 7:
                            canevas.delete(pink)
                            pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                        if i[3] == 8:
                            canevas.delete(blue)
                            blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                        if i[3] == 9:
                            canevas.delete(orange)
                            orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                        carte[coord_pacman[0]+1][coord_pacman[1]] =3 #On deplace pacman
                        carte[coord_pacman[0]][coord_pacman[1]] =2
                        canevas.delete(pacman)
                        pacman = canevas.create_arc((coord_pacman[1])*cotecarre+1, (coord_pacman[0]+1)*cotecarre+1, (coord_pacman[1]+1)*cotecarre-1, (coord_pacman[0]+2)*cotecarre-1, start=300, extent=300, fill="gold", outline="")#facerdown
                        canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                        coord_pacman[0]+=1

        else:
            if coord_pacman[0]+1 >= len(carte) and carte[0][coord_pacman[1]] != 1:
                carte[0][coord_pacman[1]] = 3
                carte[coord_pacman[0]][y] = 2
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                canevas.move(pacman, 0, -diff*(len(carte)-1))
                x= 0
            elif carte[coord_pacman[0]+1][coord_pacman[1]] != 1:
                if carte[coord_pacman[0]+1][coord_pacman[1]] == 4:
                    type_ia=6
                    compteur_fuite=50
                    score+=90
                elif carte[coord_pacman[0]+1][coord_pacman[1]] == 0:
                    score+=30
                carte[coord_pacman[0]+1][coord_pacman[1]] =3
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(pacman)
                pacman = canevas.create_arc((coord_pacman[1])*cotecarre+1, (coord_pacman[0]+1)*cotecarre+1, (coord_pacman[1]+1)*cotecarre-1, (coord_pacman[0]+2)*cotecarre-1, start=300, extent=300, fill="gold", outline="")#facedown
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                coord_pacman[0]+=1
    elif direction == 'Up':
        if coord_pacman[0]-1 <0 and carte[coord_pacman[0]-1][coord_pacman[1]] >= 6:
            if type_ia != 6:
                checkvie()
                time.sleep(3)

            else:
                score+=600
                for i in liste_fant:
                    if i[0] == coord_pacman[0]-1 and i[1] == coord_pacman[1]:
                        carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                        i[0], i[1] =i[4], i[5] #On redonne les coord initiales
                        carte[i[0]][i[1]] =i[3] # a ces coord initiales, on lui remet sa valeur
                        i[6] =30 #On l'immobilise 30 tours
                        if i[3] == 6:
                            canevas.delete(red)
                            red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                        if i[3] == 7:
                            canevas.delete(pink)
                            pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                        if i[3] == 8:
                            canevas.delete(blue)
                            blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                        if i[3] == 9:
                            canevas.delete(orange)
                            orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                        carte[coord_pacman[0]-1][coord_pacman[1]] =3 #On deplace pacman
                        carte[coord_pacman[0]][coord_pacman[1]] =2
                        canevas.delete(pacman)
                        pacman = canevas.create_arc((coord_pacman[1])*cotecarre+1, (coord_pacman[0]-1)*cotecarre+1, (coord_pacman[1]+1)*cotecarre-1, (coord_pacman[0])*cotecarre-1, start=120, extent=300, fill="gold", outline="")#faceright
                        canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                        coord_pacman[0]-=1
        else:
            if coord_pacman[0]-1 <0 and carte[len(carte)-1][coord_pacman[1]] != 1:
                carte[len(carte)-1][coord_pacman[1]] =3285
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                canevas.move(pacman, 0, +diff*(len(carte)-1))
                coord_pacman[0]=len(carte)-1
            elif carte[coord_pacman[0]-1][coord_pacman[1]] != 1:
                if carte[coord_pacman[0]-1][coord_pacman[1]] == 4:
                    type_ia=6
                    compteur_fuite=50
                    score+=90
                elif carte[coord_pacman[0]-1][coord_pacman[1]] == 0:
                    score+=30
                carte[coord_pacman[0]-1][coord_pacman[1]] =3
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(pacman)
                pacman = canevas.create_arc((coord_pacman[1])*cotecarre+1, (coord_pacman[0]-1)*cotecarre+1, (coord_pacman[1]+1)*cotecarre-1, (coord_pacman[0])*cotecarre-1, start=120, extent=300, fill="gold", outline="")#faceright
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                coord_pacman[0]-=1

    elif direction == 'Left':
        if (coord_pacman[1]-1) >= 0 and carte[coord_pacman[0]][coord_pacman[1]-1] >= 6:
            if type_ia != 6:
                checkvie()
                time.sleep(3)

            else:
                score+=600
                for i in liste_fant:
                    if i[0] == coord_pacman[0] and i[1] == coord_pacman[1]-1:
                        carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                        i[0], i[1] =i[4], i[5] #On redonne les coord initiales
                        carte[i[0]][i[1]] =i[3] # a ces coord initiales, on lui remet sa valeur
                        i[6] =30 #On l'immobilise 30 tours
                        if i[3] == 6:
                            canevas.delete(red)
                            red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                        if i[3] == 7:
                            canevas.delete(pink)
                            pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                        if i[3] == 8:
                            canevas.delete(blue)
                            blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                        if i[3] == 9:
                            canevas.delete(orange)
                            orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                        carte[coord_pacman[0]][coord_pacman[1]-1] =3 #On deplace pacman
                        carte[coord_pacman[0]][coord_pacman[1]] =2
                        canevas.delete(pacman)
                        pacman = canevas.create_arc((coord_pacman[1])*cotecarre-1, coord_pacman[0]*cotecarre+1, (coord_pacman[1]-1)*cotecarre+1, (coord_pacman[0]+1)*cotecarre-1, start=210, extent=300, fill="gold", outline="")#faceleft
                        canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                        coord_pacman[1]-=1
        else:
            if coord_pacman[1]-1 < 0 and carte[coord_pacman[0]][len(carte[0])-1] != 1:
                carte[coord_pacman[0]][len(carte[0])-1] =3
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                canevas.move(pacman, +diff*(len(carte[0])-1), 0)
                y=len(carte[0])-1
            elif carte[coord_pacman[0]][coord_pacman[1]-1] != 1:
                if carte[coord_pacman[0]][coord_pacman[1]-1] == 4:
                    type_ia=6
                    compteur_fuite=50
                    score+=90
                elif carte[coord_pacman[0]][coord_pacman[1]-1] == 0:
                    score+=30
                carte[coord_pacman[0]][coord_pacman[1]-1] =3
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(pacman)
                pacman = canevas.create_arc((coord_pacman[1])*cotecarre-1, coord_pacman[0]*cotecarre+1, (coord_pacman[1]-1)*cotecarre+1, (coord_pacman[0]+1)*cotecarre-1, start=210, extent=300, fill="gold", outline="")#faceleft
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                coord_pacman[1]-=1


    elif direction == 'Right':
        if coord_pacman[1]+1 < len(carte[0]) and carte[coord_pacman[0]][coord_pacman[1]+1] >= 6:
            if type_ia != 6:
                checkvie()
                time.sleep(3)

            else:
                score+=600
                for i in liste_fant:
                    if i[0] == coord_pacman[0] and i[1] == coord_pacman[1]+1:
                        carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                        i[0], i[1] =i[4], i[5] #On redonne les coord initiales
                        carte[i[0]][i[1]] =i[3] # a ces coord initiales, on lui remet sa valeur
                        i[6] =30 #On l'immobilise 30 tours
                        if i[3] == 6:
                            canevas.delete(red)
                            red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                        if i[3] == 7:
                            canevas.delete(pink)
                            pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                        if i[3] == 8:
                            canevas.delete(blue)
                            blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                        if i[3] == 9:
                            canevas.delete(orange)
                            orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                        carte[coord_pacman[0]][coord_pacman[1]+1] =3 #On deplace pacman
                        carte[coord_pacman[0]][coord_pacman[1]] =2
                        canevas.delete(pacman)
                        pacman = canevas.create_arc((coord_pacman[1]+1)*cotecarre+1, coord_pacman[0]*cotecarre+1, (coord_pacman[1]+2)*cotecarre-1, (coord_pacman[0]+1)*cotecarre-1, start=30, extent=300, fill="gold", outline="")#faceright
                        canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                        coord_pacman[1]+=1
        else:
            if coord_pacman[1]+1 >= len(carte[0]) and carte[x][0] != 1:
                carte[coord_pacman[0]][0] =3
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                canevas.move(pacman, -diff*(len(carte[0])-1), 0)
                y= 0
            elif carte[coord_pacman[0]][coord_pacman[1]+1] != 1:
                if carte[coord_pacman[0]][coord_pacman[1]+1] == 4:
                    type_ia=6
                    compteur_fuite=50
                    score+=90
                elif carte[coord_pacman[0]][coord_pacman[1]+1] == 0:
                    score+=30
                carte[coord_pacman[0]][coord_pacman[1]+1] =3
                carte[coord_pacman[0]][coord_pacman[1]] =2
                canevas.delete(pacman)
                pacman = canevas.create_arc((coord_pacman[1]+1)*cotecarre+1, coord_pacman[0]*cotecarre+1, (coord_pacman[1]+2)*cotecarre-1, (coord_pacman[0]+1)*cotecarre-1, start=30, extent=300, fill="gold", outline="")#faceright
                canevas.delete(id_liste[coord_pacman[0]][coord_pacman[1]])
                coord_pacman[1]+=1

    for i in liste_fant:
        if i[3] == 6:
            i[6]-=1
            xs, ys=i[0], i[1]
            if compteur_fuite == 0:
                type_ia = sauvegarde_ia
            if i[6] <= 0: #S'il n'est pas immobilisé
                coord_fantome[0], coord_fantome[1]=move_adv(coord_pacman, i, carte, type_ia)
            else:
                coord_fantome[0], coord_fantome[1]=xs, ys
            if carte[coord_fantome[0]][coord_fantome[1]] == 3:
                if type_ia != 6:
                    checkvie()
                    time.sleep(3)
                    continue
                else:
                    if i[3] == 6:
                        canevas.delete(red)
                        red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                    if i[3] == 7:
                        canevas.delete(pink)
                        pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                    if i[3] == 8:
                        canevas.delete(blue)
                        blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                    if i[3] == 9:
                        canevas.delete(orange)
                        orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                    continue
            if coord_fantome[0] == xs and coord_fantome[1] == ys:
                carte[xs][ys] =2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                i[2] =2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            else:
                carte[xs][ys] =i[2]
                i[2] =carte[coord_fantome[0]][coord_fantome[1]] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            carte[coord_fantome[0]][coord_fantome[1]] =i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)

            canevas.move(red, -(ys-coord_fantome[1])*cotecarre, -(xs-coord_fantome[0])*cotecarre)

        if i[3] == 7:
            i[6]-=1
            xs, ys=i[0], i[1]
            if compteur_fuite == 0:
                type_ia = sauvegarde_ia
            if i[6] <= 0: #S'il n'est pas immobilisé
                coord_fantome[0], coord_fantome[1]=move_adv(coord_pacman, i, carte, type_ia)
            else:
                coord_fantome[0], coord_fantome[1]=xs, ys
            if carte[coord_fantome[0]][coord_fantome[1]] == 3:
                if type_ia != 6:
                    checkvie()
                    time.sleep(3)
                    continue
                else:
                    if i[3] == 6:
                        canevas.delete(red)
                        red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                    if i[3] == 7:
                        canevas.delete(pink)
                        pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                    if i[3] == 8:
                        canevas.delete(blue)
                        blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                    if i[3] == 9:
                        canevas.delete(orange)
                        orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                    continue
            if coord_fantome[0] == xs and coord_fantome[1] == ys:
                carte[xs][ys] =2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                i[2] =2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            else:
                carte[xs][ys] =i[2]
                i[2] =carte[coord_fantome[0]][coord_fantome[1]] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            carte[coord_fantome[0]][coord_fantome[1]] =i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)

            canevas.move(pink, -(ys-coord_fantome[1])*cotecarre, -(xs-coord_fantome[0])*cotecarre)

        if i[3] == 8:
            i[6]-=1
            xs, ys=i[0], i[1]
            if compteur_fuite == 0:
                type_ia = sauvegarde_ia
            if i[6] <= 0: #S'il n'est pas immobilisé
                coord_fantome[0], coord_fantome[1]=move_adv(coord_pacman, i, carte, type_ia)
            else:
                coord_fantome[0], coord_fantome[1]=xs, ys
            if carte[coord_fantome[0]][coord_fantome[1]] == 3:
                if type_ia != 6:
                   checkvie()
                   time.sleep(3)
                   continue
                else:
                    if i[3] == 6:
                        canevas.delete(red)
                        red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                    if i[3] == 7:
                        canevas.delete(pink)
                        pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                    if i[3] == 8:
                        canevas.delete(blue)
                        blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                    if i[3] == 9:
                        canevas.delete(orange)
                        orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                    continue
            if coord_fantome[0] == xs and coord_fantome[1] == ys:
                carte[xs][ys] =2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                i[2] =2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            else:
                carte[xs][ys] =i[2]
                i[2] =carte[coord_fantome[0]][coord_fantome[1]] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            carte[coord_fantome[0]][coord_fantome[1]] =i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)

            canevas.move(blue, -(ys-coord_fantome[1])*cotecarre, -(xs-coord_fantome[0])*cotecarre)

        if i[3] == 9:
            i[6]-=1
            xs, ys=i[0], i[1]
            if compteur_fuite == 0:
                type_ia = sauvegarde_ia
            if i[6] <= 0: #S'il n'est pas immobilisé
                coord_fantome[0], coord_fantome[1]=move_adv(coord_pacman, i, carte, type_ia)
            else:
                coord_fantome[0], coord_fantome[1]=xs, ys
            if carte[coord_fantome[0]][coord_fantome[1]] == 3:
                if type_ia != 6:
                    checkvie()
                    time.sleep(3)
                    continue
                else:
                    if i[3] == 6:
                        canevas.delete(red)
                        red = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='red', outline='')
                    if i[3] == 7:
                        canevas.delete(pink)
                        pink = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='pink', outline='')
                    if i[3] == 8:
                        canevas.delete(blue)
                        blue = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='cyan', outline='')
                    if i[3] == 9:
                        canevas.delete(orange)
                        orange = canevas.create_oval(i[5]*cotecarre+1, i[4]*cotecarre+1, (i[5]+1)*cotecarre-1, (i[4]+1)*cotecarre-1, fill='orange', outline='')
                    continue
            if coord_fantome[0] == xs and coord_fantome[1] == ys:
                carte[xs][ys] =2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                i[2] =2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            else:
                carte[xs][ys] =i[2]
                i[2] =carte[coord_fantome[0]][coord_fantome[1]] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
            carte[coord_fantome[0]][coord_fantome[1]] =i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)

            canevas.move(orange, -(ys-coord_fantome[1])*cotecarre, -(xs-coord_fantome[0])*cotecarre)

        i[0], i[1] =coord_fantome[0], coord_fantome[1]
    if compteur_fuite >0:
        compteur_fuite -= 1
    if 0 not in carte:
        affichage_fenetre_fin(v_ou_d= 0)

    Labelscore.destroy()
    Labelpower.destroy()
    Labelvie.destroy()
    Labelscore=tk.Label(fenetre_jeu, text="Score:"+str(score))
    Labelpower=tk.Label(fenetre_jeu, text="Tour d'immunite:"+str(compteur_fuite))
    Labelvie=tk.Label(fenetre_jeu, text="Nombre de vie restantes:"+str(nombrevie))
    Labelpower.pack(side='bottom')
    Labelscore.pack(side='bottom')
    Labelvie.pack(side="bottom")
    compteur_tour+=1
    if direction in ["Up", "Down", "Left", "Right", ""]:
        score-=10
        canevas.after(vitesse, move_pac_et_fant)


def ouvrecarte(mapfile):
    """
    ouvrecarte(mapfile)
    Cette fonction prend un fichier rempli de 0 et de 1 et retourne un ndarray
    """
    global nom_map
    with open(nom_map, 'r') as file1:
        ligne=file1.readline().replace(" ", "")  #attention si mauvais formatage fichier
        cartetmp=[] #faire en sorte de completer si ligne vide ? si espace entre ligne
        while ligne !="": #ne marchera pas/mal si diff de lignes
            listeligne=[]
            for i in range(len(ligne)-1):
                listeligne.append(int(ligne[i])) #int !!!

            cartetmp.append(listeligne)
            ligne=file1.readline().replace(" ", "")
    return np.array(cartetmp)

def resize_map(fenetre_jeu, carte):
    """
    Prend la fenetre_jeu principale
    Permet de changer la résolution de la carte si la carte est plus grande que ce que peut afficher l'écran
    Créée un canvas
    Retourne un element canvas et la taille des tuiles
    """
    global cotecarre

    largeurmax = fenetre_jeu.winfo_screenwidth() #on recupere taille de l'ecran
    hauteurmax = fenetre_jeu.winfo_screenheight()
    haut=(len(carte))*cotecarre
    lar=(len(carte[0]))*cotecarre

    while haut>hauteurmax or lar>largeurmax: #tant que la carte est trop grande
        cotecarre=cotecarre-10 #ou 5 ?
        haut=(len(carte))*cotecarre
        lar=(len(carte[0]))*cotecarre

    return tk.Canvas(fenetre_jeu, width=lar, height=haut, bg='black')

def is_legal(mapfile, verbose=False):
    """
    Fonction qui lit un fichier map et qui retourne un booléen indiquant si
    la carte est correcte dans son organisation.
    La fonction peut prendre un paramètre booléen verbose qui si Vrai, retourne
    pourquoi le fichier n'est pas valide.
    Si un fichier a des caractères non entiers, des lignes de taille différente,
    ou des lignes vides, il est non valide.
    """
    with open(mapfile, 'r') as file1:
        ligne=file1.readline().replace(" ", "")
        taille_ligne=len(ligne) #On considère que toutes les lignes ont la meme taille que la premiere
        while ligne !="": # or ligne != "\n" pour arreter a ligne vide sous linux?
            try:
                int(ligne)
            except:
                if verbose:
                    print("{} a des caractères qui ne sont pas des entiers ou des lignes vides".format(mapfile))
                return False

            if len(ligne) != taille_ligne:
                if verbose:
                    print("{} a des lignes de taille différente".format(mapfile))
                return False
            ligne=file1.readline().replace(" ", "")
    return True

def locate_pacman(carte):
    """
    Prend une carte (numpyarray)
    Regarde si la carte est légale (possède un unique pacman) sinon quitte le programme
    Si un seul pacman est trouvé, on retourne ses coordonnées
    """
    array_pac = np.argwhere(carte == 3)

    if(len(array_pac) > 1):
        print("ERREUR !! il y a plusieurs pacman")
        sys.exit()
    if (len(array_pac) <1): #resoudre avec map ?
        print("ERREUR !! il n'y a pas de pacman")
        sys.exit()
    return ([array_pac[0, 0], array_pac[0, 1]])

def locate_ghost(carte):
    """
    Prend une carte (numpyarray)
    Retourne une liste de liste des coordonnées de chaque fantome et l'element de la case du fantome(vide, pac-gum...)
    0, 1: x, y
    2: case vide
    3: numero antome
    4, 5: coord d'origine
    6: timer d'immobilisation
    """
    liste_fant=[]
    coord_fant=[]
    array_fant=np.argwhere(carte >= 6) #retourne une matrice avec les coordonnées des fantomes
    immobilisation =0

    for i in array_fant:
        coord_fant.append(i[0])
        coord_fant.append(i[1]) #raccourcir
        coord_fant.append(2) #on considere que le fantome est généré sur une case vide
        coord_fant.append(carte[i[0]][i[1]]) #rajoute valeur de case du fantome
        xor, yor=i[0], i[1] #on def les x et y d'origine en evitant le piège des pointeurs
        coord_fant.append(xor)
        coord_fant.append(yor)
        coord_fant.append(immobilisation) #par defaut le fantome n'a aucun tour d'immobilis
        liste_fant.append(coord_fant)
        coord_fant=[] #reinit pour prochain fantome
    return liste_fant

def transforme_list_en_int(x):
    return int(x)

def highscore():
    global nom_map, score, compteur_tour
    global pseudo
    test_fichier="./Fichier_score/"+nom_map[15:-3]+"score"
    nom_score = nom_map[14:-3]+"score"

    texte_fichier=[]
    ligne_a_ajouter=[]

    if os.path.isfile(test_fichier):
        with open(test_fichier, 'r') as fichier:
            for ligne in fichier:
                ligne = ligne[:-1]
                ligne = ligne.split(" ")
                ligne[0] =str(ligne[0])
                ligne[1] =int(ligne[1])
                ligne[2] =int(ligne[2])
                texte_fichier.append(ligne)
            ligne_a_ajouter.append(str(pseudo))
            ligne_a_ajouter.append(int(compteur_tour))
            ligne_a_ajouter.append(int(score))
            texte_fichier.append(ligne_a_ajouter)
            texte_fichier.sort(key=lambda x: x[2], reverse=True)
            position = texte_fichier.index(ligne_a_ajouter)

        os.chdir("./Fichier_score/")
        with open(nom_score, 'w') as fichier:
            for i in range(len(texte_fichier)):
                fichier.write(str(texte_fichier[i][0]) + " ")
                fichier.write(str(texte_fichier[i][1]) + " ")
                fichier.write(str(texte_fichier[i][2]))
                fichier.write("\n")
        os.chdir("..")

    else:
        os.chdir("./Fichier_score/")
        with open(nom_score, 'w') as fichier:
            ligne_a_ajouter.append(str(pseudo))
            ligne_a_ajouter.append(int(compteur_tour))
            ligne_a_ajouter.append(str(score))
            texte_fichier.append(ligne_a_ajouter)
            for i in range(len(texte_fichier)):
                fichier.write(str(texte_fichier[i][0]) + " ")
                fichier.write(str(texte_fichier[i][1]) + " ")
                fichier.write(str(texte_fichier[i][2]))
                fichier.write("\n")
                position=-1
        os.chdir("..")
    return position

def affichage_fenetre_fin(v_ou_d):
    global compteur_tour
    global score
    global pseudo

    fenetre_fin = tk.Tk()

    if v_ou_d == 0:
        texte_victoire="Bravo !!!\nTu as gagner cette partie très difficile d'un jeu merveilleusement bien codé\net ce par des personnes exceptionelles.\n\n\nTu as gagnés en {0} tours\nTu as eu un score de {1}".format(compteur_tour, score)
        message_victoire = tk.Label(fenetre_fin, text=texte_victoire)
        message_victoire.pack(padx=200, pady=50, side='top')
    elif v_ou_d == 1:
        texte_defaite="Dommage, tu as perdus !!!\nTu as perdus cette partie très difficile d'un jeu merveilleusement bien codé\net ce par des personnes exceptionelles.\n\n\nTu as perdus en {0} tours\nTu as eu un score de {1}".format(compteur_tour, score)
        message_defaite = tk.Label(fenetre_fin, text=texte_defaite)
        message_defaite.pack(padx=200, pady=50, side='top')

    position = highscore()

    texte_position="Vous êtes {0}ème sur cette map.".format(position+1)
    if position == 0:
         texte_position="Vous êtes PREMIER sur cette map, vous êtes un boss de Pacman."
    if position == -1:
         texte_position="Vous êtes PREMIER sur cette map, vous êtes un boss de Pacman.\nEn même temps vous êtes le seul a avoir fais un score ^^."

    message_position = tk.Label(fenetre_fin, text=texte_position)
    message_position.pack(padx=200, pady=50, side='top')

    bouton_quitter2 = tk.Button(fenetre_fin, text="Quitter", command=sys.exit)
    bouton_quitter2.pack(expand=True, side = tk.BOTTOM)

    fenetre_fin.mainloop()


def lancer_le_jeu():

    fenetre_menu.destroy()

    global cotecarre
    global coord_pacman
    global liste_fant
    global direction, direction_sauv
    global type_ia
    global canevas
    global carte
    global score
    global fenetre_jeu
    global Labelscore
    global Labelpower
    global Labelvie
    global compteur_fuite
    global nombrevie
    global xpac, ypac


    fenetre_jeu = tk.Tk()

    bouton_son = tk.Button(fenetre_jeu, text="Stop la musique", command=stop_son).pack(side="bottom")
    bouton_son = tk.Button(fenetre_jeu, text="Joue la musique", command=joue_son).pack(side="bottom")

    carte = ouvrecarte(map)

    #On regarde si la carte est légale
    coord_pacman=[0,0]
    coord_pacman = locate_pacman(carte) #On prend les coordonnées de pacman
    xpac, ypac = coord_pacman[0], coord_pacman[1] #Les coord d'origine du pacman
    liste_fant = locate_ghost(carte) #On prend les informations des fantomes

    canevas = resize_map(fenetre_jeu, carte) #on prend canvas et dimensions

    direction = ''
    direction_sauv = ' '
    sauvegarde_ia = 0
    type_ia = sauvegarde_ia

    affichage_plateau(carte)

    canevas.pack(side=tk.LEFT)
    canevas.focus_set()
    canevas.bind('<Key>', Clavier)

    bouton_pause = tk.Button(fenetre_jeu, text="Pause", command=pause)
    bouton_pause.pack(expand=True)

    bouton_start = tk.Button(fenetre_jeu, text="Start", command=start)
    bouton_start.pack(expand=True)

    bouton_quitter = tk.Button(fenetre_jeu, text="Quitter", command=fenetre_jeu.destroy)
    bouton_quitter.pack(expand=True, side = tk.BOTTOM)

    Labelscore=tk.Label(fenetre_jeu, text="Score:"+str(score))
    Labelscore.pack(side='bottom')

    Labelpower=tk.Label(fenetre_jeu, text="Tour d'immunite:"+str(compteur_fuite))
    Labelpower.pack(side='bottom')

    Labelvie=tk.Label(fenetre_jeu, text="Nombre de vie restantes:"+str(nombrevie))
    Labelvie.pack(side="bottom")

    fenetre_jeu.mainloop()

fenetre_menu = tk.Tk()

bouton_lancer = tk.Button(fenetre_menu, text="Lancer le jeu", command=lancer_le_jeu)
#bouton_lancer.pack(padx=100, pady=50, side='top')
bouton_lancer.grid(column=2, row= 0)

def sel_taille():
    global cotecarre
    cotecarre = varGr.get()

Label1 = tk.Label(fenetre_menu, text="Choississez la taille d'une case de la map ! (en pixel)")
Label1.grid(column=0, row=1)

vals = [80, 60, 40, 20, 10]
etiqs = ['80', '60', '40', '20', '10']
varGr = tk.IntVar()
varGr.set(vals[2])
cotecarre=vals[2]
for i in range(len(vals)):
    b = tk.Radiobutton(fenetre_menu, variable=varGr, text=etiqs[i], value=vals[i], command=sel_taille)
    b.grid(column =0, row=i+2)

Label2 = tk.Label(fenetre_menu, text="Coississez ici votre map parmis celle proposez ci dessous")
Label2.grid(column=2, row=8)

def nom_map_pardefaut():
    global nom_map
    index_element = (0, )
    nom_map = dropd.get(index_element)

def clic(evt): #on peut appeler evt? developpez.com
    global nom_map
    i = dropd.curselection()  ## Récupération de l'index de l'élément sélectionné
    nom_map = dropd.get(i)  ## On retourne l'élément (un string) sélectionné ; Faire en sorte de prendre dernier selectionné
    nom_map = "./Fichier_map/" + nom_map

legalmaps=[]

mapfiles = list(Path('./Fichier_map/').glob('*.map'))
legalmaps2 = [str(pathmap) for pathmap in mapfiles if is_legal(str(pathmap))]
for m in legalmaps2:
    legalmaps.append(m[12:])
listeoptions = list(range(1, 1000))
dropd = tk.Listbox(fenetre_menu) #, listvariable=listeoptions)

for i in range(1, len(legalmaps2)+1): #enumerate
  dropd.insert(i, legalmaps[i-1])
  dropd.bind('<ButtonRelease-1>', clic)
nom_map_pardefaut()
dropd.grid(column=2, row=9)

def sel_dif():
    global type_ia
    global sauvegarde_ia
    type_ia = varGr4.get()
    sauvegarde_ia = type_ia #Le niveau de difficulté du jeu auquel on doit revenir après la fin de la fuite

compteur_fuite = 0
score = 0
nombrevie = 0
compteur_tour = 0
pseudo = 'test'
vitesse = 200


Label4 = tk.Label(fenetre_menu, text="Niveaux de difficultés")
Label4.grid(column=1, row=1)

vals4 = [1, 2, 3, 4, 5]
etiqs4 = ['Très Facile', 'Facile', 'Normal', 'Difficile', 'Impossible']
varGr4 = tk.IntVar()
type_ia = vals4[0]
sauvegarde_ia = vals4[0]
varGr4.set(vals4[0])
for k in range(len(etiqs4)):
    b4 = tk.Radiobutton(fenetre_menu, variable=varGr4, text=etiqs4[k], value=vals4[k], command=sel_dif)
    b4.grid(column=1, row=k+2)

def sel_vitesse():
    global vitesse
    vitesse = varGr6.get()

Label6 = tk.Label(fenetre_menu, text="Vitesse du jeu")
Label6.grid(column=3, row=1)

vals6 = [300, 250, 200, 150, 100]
etiqs6 = ['Très lent', 'Lent', 'Normal', 'Rapide', 'Très rapide']
varGr6 = tk.IntVar()
vitesse = vals6[2]
varGr6.set(vals6[2])
for p in range(len(etiqs6)):
    b6 = tk.Radiobutton(fenetre_menu, variable=varGr6, text=etiqs6[p], value=vals6[p], command=sel_vitesse)
    b6.grid(column=3, row=p+2)

def sel_vie():
    global nombrevie
    nombrevie = varGr5.get()

Label5 = tk.Label(fenetre_menu, text="Nombre de vie")
Label5.grid(column=2, row=1)

vals5 = [0, 1, 2, 3, 4]
etiqs5 = ['1', '2', '3', '4', '5']
varGr5 = tk.IntVar()
nombrevie = vals5[0]
varGr5.set(vals5[0])
for l in range(len(etiqs5)):
    b5 = tk.Radiobutton(fenetre_menu, variable=varGr5, text=etiqs5[l], value=vals5[l], command=sel_vie)
    b5.grid(column=2, row=l+2)

def retour():
    global pseudo
    pseudo=varGr3.get()

Label3 = tk.Label(fenetre_menu, text="Entrez votre pseudo ici !")
Label3.grid(column=4, row=2)

varGr3 = tk.StringVar()
entree = tk.Entry(fenetre_menu, textvariable=varGr3)
entree.grid(column=4, row=3)

tk.Button(fenetre_menu, text="Valider", command=retour).grid(column=4, row=4)

pygame.mixer.init()

def joue_son():
    pygame.mixer.Sound("./Fichier_son/pacman_beginning.wav").play(-1)

def stop_son():
    pygame.mixer.stop()

bouton_son = tk.Button(fenetre_menu, text="Joue la musique", command=joue_son).grid(column=0, row=1000)
bouton_son = tk.Button(fenetre_menu, text="Stop la musique", command=stop_son).grid(column=1, row=1000)



fenetre_menu.mainloop()
