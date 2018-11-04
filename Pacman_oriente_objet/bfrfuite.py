#! /usr/bin/env python3

import numpy as np
import tkinter as tk
import random
import sys
import math
import time 
import os
from pathlib import Path


#Il faut encore que type_ia 4 et 5 soient implementés ou retirés des choix
#-On peut prendre framerate demandé a user si on veut
#Bugs -> quand appuie sur start +sieurs fois, vitesse augmente
#Graphique des fantomes bizarre après mort de pacman
#pos de pacman pas mise a jour

class AppliPrincipale(tk.Tk):
    """
    Classe qui contient la fenetre mère
    """
    def __init__(self): #,carte):
        # Appel du constructeur de la classe mère (l'instance se retrouve dans le self)
        tk.Tk.__init__(self)
        self.configure(background='black')
        self.title("PAC-MAN")
        #self.cotecarre=40
        
        #btn1 = tk.Button(self, text="Quitter", command=self.quit)   #mettre boutons options ?
        #btn1.pack(side=tk.RIGHT) #si <FocusOut> pause ?
        

class StartMenu():
    """
    Menu qui prend les configurations définies par l'utilisateur
    Il doit etre invoqué dans une instance de Tk()
    """
    #cotecarre en var classe ?
    def __init__(self,fenetre): 
        """
        """
        # Appel du constructeur de la classe mère (l'instance se retrouve dans le self)

        self.conteneur=tk.Frame(fenetre,takefocus=1) #les widgets seront crées dedans
        #self.configure(background="green") #debug
        conteneur=self.conteneur
        conteneur.pack(expand=True)
        
        #variables qu'on veut extraire
        self.type_ia=1
        #COTECARRE
        self.Label1 = tk.Label(conteneur, text = "Choisissez la taille d'une case de la "
                                                 "map en pixels \n "
                                                 "(la valeur sera ajustée si trop grande)")
        self.Label1.grid(column=0,row=1)

        self.vals = [80, 60, 40, 20, 10] #Valeurs possibles de cotecarre
        self.etiqs = [str(val) for val in self.vals] 
        self.varGr = tk.IntVar()
        self.varGr.set(self.vals[2]) #cotecarre=40 par defaut
        self.cotecarre=self.vals[2]
        for i in range(len(self.vals)):
            carresize = tk.Radiobutton(conteneur, variable=self.varGr, text=self.etiqs[i],
                                       value=self.vals[i],command=self.sel_taille)
            carresize.grid(column=0,row=i+2)
        
        #NOM_MAP
        self.Label2 = tk.Label(conteneur, text = "\nVoici les map trouvées dans le répertoire\n"
                                            "Choisissez votre map parmi celles proposées ci dessous:")
        self.Label2.grid(column=2,row=8)
        
        mapfiles=list(Path('.').glob('*.map'))
        #Liste des cartes
        legalmaps=[str(pathmap) for pathmap in mapfiles if is_legal(str(pathmap))]
        self.dropd=tk.Listbox(conteneur) 
        for i,map in enumerate(legalmaps): #enumerate
            self.dropd.insert(i,map)
            self.dropd.bind('<ButtonRelease-1>',self.clic)
        self.nom_map=self.dropd.get((0,))
        #self.nom_map_pardefaut()
        self.dropd.grid(column=2,row=9)
        
        
        #PSEUDO
        Label3 = tk.Label(conteneur, text = "Entrez votre pseudo ici !")
        Label3.grid(column=4,row=2)
        
        self.pseudo="test"
        self.varGr3= tk.StringVar()
        entree = tk.Entry(conteneur,textvariable=self.varGr3)
        entree.grid(column=4,row=3)
        
        tk.Button(conteneur, text = "Valider", command=self.retour).grid(column=4,row=4)
        
        #TYPE IA
        self.Label4 = tk.Label(conteneur, text = "\nNiveaux de difficulté")
        self.Label4.grid(column=1,row=1)
        
        self.vals4 = [1,2,3,4,5]
        self.etiqs4 = ['Très Facile', 'Facile', 'Normal','Difficile','Impossible']
        self.varGr4= tk.IntVar()
        self.type_ia=self.vals4[0]
        self.varGr4.set(self.vals4[0])
        for k in range(len(self.etiqs4)):
            self.b4 = tk.Radiobutton(conteneur, variable=self.varGr4, text=self.etiqs4[k],\
                                     value=self.vals4[k],command=self.sel_dif)
            self.b4.grid(column=1,row=k+2)
        
        
        #NOMBRE VIE
        Label5 = tk.Label(conteneur, text = "Nombre de vie")
        Label5.grid(column=2,row=1)
        
        vals5 = [0,1,2,3,4]
        etiqs5 = ['1','2','3','4','5']
        self.varGr5= tk.IntVar()
        self.nombrevie=vals5[0]
        self.varGr5.set(vals5[0])
        for l in range(len(etiqs5)):
            b5 = tk.Radiobutton(conteneur, variable=self.varGr5, text=etiqs5[l],\
                                value=vals5[l],command=self.sel_vie)
            b5.grid(column=2,row=l+2)
        
        #VITESSE
        Label6 = tk.Label(conteneur, text = "Vitesse du jeu")
        Label6.grid(column=3,row=1)
        self.vitesse=200
        vals6 = [300,250,200,150,100]
        etiqs6 = ['Très lent','Lent','Normal','Rapide','Très rapide']
        self.varGr6= tk.IntVar()
        self.vitesse=vals6[2]
        self.varGr6.set(vals6[2])
        for p in range(len(etiqs6)):
            b6 = tk.Radiobutton(conteneur, variable=self.varGr6, text=etiqs6[p],\
                                value=vals6[p],command=self.sel_vitesse)
            b6.grid(column=3,row=p+2)
        

            
        #safety net    
        bouton_quitter = tk.Button(conteneur, text="Commencer une partie",command=conteneur.quit) #destroy fait planter
        bouton_quitter.grid()

        fenetre.title("Paramètres de jeu")
        
        fenetre.mainloop()
        
        
    
    def sel_taille(self):
        """ """
        self.cotecarre = self.varGr.get()
    

    def clic(self,evt): #on peut appeler evt? developpez.com
        """
        """
        i=self.dropd.curselection()  ## Récupération de l'index de l'élément sélectionné
        self.nom_map = self.dropd.get(i)  ## On retourne l'élément (un string) sélectionné 
    
    def retour(self):
        #global pseudo
        self.pseudo=self.varGr3.get()
    
    def sel_dif(self):
        """
        """
        self.type_ia=self.varGr4.get()
        
    def sel_vitesse(self):
        self.vitesse=self.varGr6.get()
    
    
    def sel_vie(self):
        #global nombrevie
        self.nombrevie=self.varGr5.get()
    
        
    
    

        
    


   
class GestionMouvement():
    """
    Creation du canvas et
    toutes les IA
    """
    def __init__(self,fenetre): #ou **prendre carte** et initialiser dedans ? et prendre root
        #carte maintenant prise dans StartMenu
        #il faut carte, elems graphiques et coord, + liste pac gum, cotecarre
        
        param_user=StartMenu(fenetre)   
        self.nom_map=param_user.nom_map    
        self.carte=ouvre_carte(param_user.nom_map)
        cotecarre=param_user.cotecarre
        self.pseudo=param_user.pseudo
        self.type_ia=param_user.type_ia #Pouvoir modif apres 
        self.vitesse=param_user.vitesse
        self.nombrevie=param_user.nombrevie
        param_user.conteneur.destroy()
        
        self.x,self.y=locate_pacman(self.carte)
        self.xpac,self.ypac=self.x,self.y #coordonnées d'origine de pacman
        self.liste_fant=locate_ghost(self.carte)
        self.canevas,self.cotecarre=resize_map(fenetre,self.carte,cotecarre) 
        self.pacman=""
        self.red,self.pink,self.blue,self.orange="","","",""
        self.id_liste=[] #id des pac-gommes et power ups
        
        fenetre.title("PAC-MAN") 
        
        self.direction=""
        self.direction_sauv=' '
        
        self.compteur_fuite=0
        self.compteur_tour=0
        self.score=0
        #self.nombrevie=3
        self.window=fenetre #pour appeler argument de init dans methodes
        
        self.affichage_plateau()
        
        self.canevas.focus_set()
        self.canevas.bind('<Key>',self.clavier)
        
        self.canevas.pack(side=tk.LEFT) #affichage plateau apres ?
        #print("Canvas créé")
        bouton_pause = tk.Button(fenetre, text="Pause",command=self.pause) #! agit sur fenetre, pas self
        bouton_pause.pack(expand=True)
    
        bouton_start = tk.Button(fenetre, text="Start",command=self.start)
        bouton_start.pack(expand=True)
    
        bouton_quitter = tk.Button(fenetre, text="Quitter",command=fenetre.destroy)
        bouton_quitter.pack(expand=True,side = tk.BOTTOM)
        
        self.Labelscore=tk.Label(fenetre,text="Score:"+str(self.score))
        self.Labelscore.pack(side='bottom')
    
        self.Labelpower=tk.Label(fenetre,text="Tour(s) d'immunité :"+str(self.compteur_fuite))
        self.Labelpower.pack(side='bottom')
    
        self.Labelvie=tk.Label(fenetre,text="Nombre de vie(s) restant(es) :"+str(self.nombrevie))
        self.Labelvie.pack(side="bottom")
        self.move_pac_et_fant()
        
        fenetre.mainloop()
        
    
    def affichage_plateau(self):#,carte): #!!!!!!!!!!!!!!!!!!!!!!!! OK ?
        """
        Initialise le plateau dans tkinter à partir d'une matrice
        """
        #global pacman
        #global red,blue,pink,orange
        #global id_liste
        #id_liste = []
        #print(id(self.window)) #debug
        carte=self.carte #On prend les valeurs initialisées dans le init
        cotecarre=self.cotecarre
        canevas=self.canevas
        for x in range(len(carte)):
            coord_x0=0
            coord_y0=0+(x*cotecarre)
            coord_x1=cotecarre
            coord_y1=cotecarre+(x*cotecarre)
            id_listex=[]
            for y in range(len(carte[0])):
                if carte[x][y] == 1: #Mur
                    canevas.create_rectangle(coord_x0,coord_y0,\
                                            coord_x1,coord_y1,\
                                            fill='blue',outline='blue')
                elif carte[x][y] == 3: #Pac-man
                    #if face == 1: flag de la position
                    self.pacman = canevas.create_arc(coord_x0+1,coord_y0+1,\
                                                     coord_x1-1,coord_y1-1,\
                                                     start=30,extent=300,\
                                                     fill="gold",outline="")#faceright
                elif carte[x][y] == 0: #On recupere les id des pac-gommes créées
                    id_listex.append(canevas.create_oval(
                                     coord_x0+(cotecarre/3),coord_y0+(cotecarre/3),\
                                     coord_x1-(cotecarre/3),coord_y1-(cotecarre/3),\
                                     fill='light yellow',outline=''))
                elif carte[x][y] == 4: #idem pour les powerups
                    id_listex.append(canevas.create_oval(
                                    coord_x0+(cotecarre/4),coord_y0+(cotecarre/4),\
                                    coord_x1-(cotecarre/4),coord_y1-(cotecarre/4),\
                                    fill='dark violet',outline=''))
                elif carte[x][y] == 6: #Blinky
                    self.red = canevas.create_oval(coord_x0+1,coord_y0+1,\
                                                   coord_x1-1,coord_y1-1,\
                                                   fill='red',outline='')
                elif carte[x][y] == 7: #Pinky
                    self.pink = canevas.create_oval(coord_x0+1,coord_y0+1,\
                                                    coord_x1-1,coord_y1-1,\
                                                    fill='pink',outline='')
                elif carte[x][y] == 8: #Inky
                    self.blue = canevas.create_oval(coord_x0+1,coord_y0+1,\
                                                    coord_x1-1,coord_y1-1,\
                                                    fill='cyan',outline='')
                elif carte[x][y] == 9: #Clyde
                    self.orange = canevas.create_oval(coord_x0+1,coord_y0+1,\
                                                      coord_x1-1,coord_y1-1,\
                                                      fill='orange',outline='')
                if carte[x][y] not in [0,4]: #si la case n'a pas de pac-g ou p-up
                    id_listex.append(0)
                coord_x0+=cotecarre #On avance d'un carré
                coord_x1+=cotecarre
            self.id_liste.append(id_listex)

    
    
    def clavier(self,event): #OK ?
        """ 
        Gestion de l'appui sur une touche du clavier
        redirige key recue dans move -> concatener ? 
        """
        #global direction
        self.direction = event.keysym
        
        #print(self.direction, type(self.direction))
        #self.move_everybody()#self.direction) #faire en sorte que n'appelle pas a chaque fois que enregistre tape clavier
        
    def pause(self):

        self.direction_sauv=self.direction
        self.direction = 'pause'
    
    def start(self):

        if self.direction_sauv == ' ':
            self.move_pac_et_fant()
        elif self.direction_sauv != ' ':
            self.direction=self.direction_sauv
            self.move_pac_et_fant()

        
    def checkvie(self): #indenté, rajouter docstring
        
        #Fonction qui determine si pacman a encore des vies
        #Si oui, il retourne a la position initiale
        
        xpac,ypac=self.xpac,self.ypac
        #global pacman
        #global red,blue,pink,orange
        cotecarre=self.cotecarre
        #global liste_fant
        x,y=self.x,self.y
        canevas=self.canevas
        carte=self.carte
    
        if self.nombrevie<=0:
            print("GAME OVER !!")
            self.affichage_fenetre_fin(v_ou_d=1)
            self.window.quit()
        else:
            self.nombrevie-=1
            #On replace pacman
            canevas.delete(self.pacman)
            carte[x][y]=2
            self.x,self.y=self.xpac,self.ypac #on retourne a la position initiale
            carte[x][y]=3
            self.pacman = canevas.create_arc((ypac)*cotecarre+1,(xpac)*cotecarre+1,\
                                             (ypac+1)*cotecarre-1,(xpac+1)*cotecarre-1,\
                                             start=300,extent=300,fill="gold",outline="")
            #On replace les fantômes
            for i in self.liste_fant:
                print("valeur avant :",carte[i[0]][i[1]])
                carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                print("valeur après :",carte[i[0]][i[1]])
                i[0],i[1]=i[4],i[5] #On redonne les coord initiales
                carte[i[0]][i[1]]=i[3] # a ces coord initiales, on lui remet sa valeur
                i[6]=5 #On l'immobilise 30 tours
                if i[3]==6:
                    canevas.delete(self.red)
                    self.red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                fill='red',outline='')
                if i[3]==7:
                    canevas.delete(self.pink)
                    self.pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                 (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                 fill='pink',outline='')
                if i[3]==8:
                    canevas.delete(self.blue)
                    blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                            (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                            fill='cyan',outline='')
                if i[3]==9:
                    canevas.delete(self.orange)
                    self.orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                   (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                   fill='orange',outline='')
    
        
    def choix_ia(self,x,y,x2,y2,carte): #!!!!!!!!!!!!!!!!! VOIR ARGS? carte ?
        """
        Definit le comportement des fantomes
        """
        #global type_ia
        type_ia=self.type_ia
        choix_mov=self.choix_mov #On assigne les méthodes pour éviter de taper self.methode a chaque fois
        choix_mov_rand=self.choix_mov_rand
        choix_mov_fuite=self.choix_mov_fuite
        if type_ia == 1:
            if carte[x2][y2]==6:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==7:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==8:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==9:
                return choix_mov_rand(x2,y2,carte)
    
        if type_ia == 2:
            if carte[x2][y2]==6:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==7:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==8:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==9:
                return choix_mov(x,y,x2,y2,carte)
                
        if type_ia == 3:
            if carte[x2][y2]==6:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==7:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==8:
                return choix_mov(x,y,x2,y2,carte)
            if carte[x2][y2]==9:
                return choix_mov(x,y,x2,y2,carte)
                
        if type_ia == 4:
            if carte[x2][y2]==6:
                return choix_mov_rand(x2,y2,carte)
            if carte[x2][y2]==7:
                return choix_mov(x,y,x2,y2,carte)
            if carte[x2][y2]==8:
                return choix_mov(x,y,x2,y2,carte)
            if carte[x2][y2]==9:
                return choix_mov(x,y,x2,y2,carte)
                
        if type_ia == 5:
            if carte[x2][y2]==6:
                return choix_mov(x,y,x2,y2,carte)
            if carte[x2][y2]==7:
                return choix_mov(x,y,x2,y2,carte)
            if carte[x2][y2]==8:
                return choix_mov(x,y,x2,y2,carte)
            if carte[x2][y2]==9:
                return choix_mov(x,y,x2,y2,carte)
                
        if type_ia == 6:
            if carte[x2][y2]==6:
                return choix_mov_fuite(x,y,x2,y2,carte)
            if carte[x2][y2]==7:
                return choix_mov_fuite(x,y,x2,y2,carte)
            if carte[x2][y2]==8:
                return choix_mov_fuite(x,y,x2,y2,carte)
            if carte[x2][y2]==9:
                return choix_mov_fuite(x,y,x2,y2,carte)
        
    
    def move_adv(self,x,y,x2,y2,carte): #!!!!!!!!!!!! OK?
        """
        Mouvement aleatoire
        """
        direction_adv=self.choix_ia(x,y,x2,y2,carte)
        if x2-1 >= 0 and direction_adv == 'z' and carte[x2-1][y2] != 1:
            return x2-1,y2
        elif x2+1 < len(carte) and direction_adv == 's'and carte[x2+1][y2] != 1:
            return x2+1,y2
        elif y2-1 >= 0 and direction_adv == 'q' and carte[x2][y2-1] != 1:
            return x2,y2-1
        elif y2+1 < len(carte[0]) and direction_adv == 'd' and carte[x2][y2+1] != 1:
            return x2,y2+1
        else:
            return x2,y2
    
    
    def choix_mov_rand(self,x2,y2,carte): #!!!!!!!!!!!!!!!!!!!!
        while True:
            choix=random.choice(['up','down','right','left'])

            if choix == 'up' :
                if x2-1 >=0 and carte[x2-1][y2] not in [1,6,7,8,9] :
                    return 'z'
                else:
                    continue
            if choix == 'down' :
                if x2+1 < len(carte) and carte[x2+1][y2] not in [1,6,7,8,9]:
                    return 's'
                else:
                    continue
            if choix == 'left' :
                if y2-1 >=0 and carte[x2][y2-1] not in [1,6,7,8,9]:
                    return 'q'
                else:
                    continue
            if choix == 'right' :
                if y2+1 < len(carte[0]) and  carte[x2][y2+1] not in [1,6,7,8,9]:
                    return 'd'
                else:
                    continue
            if carte[x2-1][y2] in [1,6,7,8,9] and carte[x2+1][y2] in [1,6,7,8,9]\
                    and carte[x2][y2-1] in [1,6,7,8,9] \
                    and carte[x2][y2+1] in [1,6,7,8,9]:
                return 'none' #?
    
    
    def choix_mov_fuite(self,x,y,x2,y2,carte): #indenté
        """
        Choix du mouvement de fuite des fantomes basé sur choix_mov
        On considere fantomes comme des obstacles
        """
        if x > x2 and (abs(x2-x)>=abs(y2-y)):
            #si le joueur est au dessus et plus loin verticalement
            if x2-1 >=0 and carte[x2-1][y2] !=1 and carte[x2-1][y2] <6:
                # si il n'y a pas de mur sur le chemin
                return 'z'
            else:# Il y a un mur sur le chemin
                if y2-1 >=0 and y2+1 < len(carte[0]) and carte[x2][y2-1] == 1 \
                        and carte[x2][y2+1]!=1 and carte[x2][y2+1]<6:
                    #S'il y a un mur a gauche
                    return 'd'
                elif y2-1 >=0 and y2+1 < len(carte[0]) and carte[x2][y2+1] == 1 \
                        and carte[x2][y2-1] != 1 and carte[x2][y2-1] <6:
                    #S'il y a un mur a droite
                    return 'q'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2-1][y2] ==1 or carte[x2-1][y2] >= 6) \
                        and (carte[x2][y2+1]==1 or carte[x2][y2+1]>= 6) \
                        and (carte[x2][y2-1]==1 or carte[x2][y2-1]>= 6):
                    return 's'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and carte[x2][y2-1] != 1 and carte[x2][y2+1] != 1:
                    #Il n'y a pas de mur ni a droite ni a gauche
                    choix=random.choice(['q','d'])
                    return choix # Au hasard a droite ou a gauche
    
        if x < x2 and (abs(x2-x)>=abs(y2-y)):
            #si le joueur est en dessous et plus loin verticalement
            if x2+1<len(carte) and carte[x2+1][y2] != 1 and carte[x2+1][y2] <6:
                # si il n'y a pas de mur sur le chemin
                return 's'
            else:# Il y a un mur sur le chemin
                if y2-1 >=0 and y2+1 < len(carte[0]) and carte[x2][y2-1] == 1 \
                        and carte[x2][y2+1]!=1 and carte[x2][y2+1]<6: 
                    #S'il y a un mur a gauche
                    return 'd'
                elif y2-1 >=0 and y2+1 < len(carte[0]) and carte[x2][y2+1] == 1 \
                        and carte[x2][y2-1]!=1 and carte[x2][y2-1]<6:
                    #S'il y a un mur a droite
                    return 'q'
                elif  y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2+1][y2] ==1 or carte[x2+1][y2] >= 6) \
                        and (carte[x2][y2+1]==1 or carte[x2][y2+1]>= 6) \
                        and (carte[x2][y2-1]==1 or carte[x2][y2-1]>= 6):
                    return 'z'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and carte[x2][y2-1] != 1 and carte[x2][y2+1] != 1:
                    #Il n'y a pas de mur ni a droite ni a gauche
                    choix=random.choice(['q','d'])
                    return choix # Au hasard a droite ou a gauche
    
        if y < y2 and (abs(y2-y)>abs(x2-x)):
            #si le joueur est à droite et plus loin horizontalement
            if y2+1<len(carte[0]) and carte[x2][y2+1]!=1 and carte[x2][y2+1]<6 :
                # si il n'y a pas de mur sur le chemin
                return 'd'
            else:# Il y a un mur sur le chemin
                if x2-1>=0 and x2+1<len(carte) and carte[x2-1][y2] == 1\
                        and carte[x2+1][y2]!=1 and carte[x2+1][y2]<6:
                    #S'il y a un mur en haut
                    return 's'
                elif x2-1>=0 and x2+1<len(carte) and  carte[x2+1][y2] == 1 \
                        and carte[x2-1][y2]!=1 and carte[x2-1][y2]<6:
                    #S'il y a un mur en bas
                    return 'z'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2-1][y2] ==1 or carte[x2-1][y2] >= 6) \
                        and (carte[x2][y2+1]==1 or carte[x2][y2+1]>= 6) \
                        and (carte[x2+1][y2]==1 or carte[x2+1][y2]>= 6):
                    return 'a'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] != 1 \
                        and carte[x2-1][y2] != 1:
                    #Il n'y a pas de mur ni en haut ni en bas
                    choix=random.choice(['s','z'])
                    return choix # Au hasard en haut ou en bas
    
        if y > y2 and (abs(y2-y)>abs(x2-x)):
            #si le joueur est à gauche
            if y2-1>=0 and carte[x2][y2-1]!=1 and carte[x2][y2-1]<6:
                # si il n'y a pas de mur sur le chemin
                return 'q'
            else:# Il y a un mur sur le chemin
                if x2-1>=0 and x2+1<len(carte) and carte[x2-1][y2] == 1 \
                        and carte[x2+1][y2]!=1 and carte[x2+1][y2]<6:
                    #S'il y a un mur en haut
                    return 's'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] == 1 \
                        and carte[x2-1][y2]!=1 and carte[x2-1][y2]<6:
                    #S'il y a un mur en bas
                    return 'z'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2-1][y2] ==1 or carte[x2-1][y2] >= 6) \
                        and (carte[x2][y2-1]==1 or carte[x2][y2-1]>= 6) \
                        and (carte[x2+1][y2]==1 or carte[x2+1][y2]>= 6):
                    return 'd'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] != 1 \
                        and carte[x2-1][y2] != 1:
                    #Il n'y a pas de mur ni en haut ni en bas
                    choix=random.choice(['s','z'])
                    return choix # Au hasard en haut ou en bas
    
    def choix_mov(self,x,y,x2,y2,carte): #indenté
        """
        Choix mouvement fantome de maniere brute, on considere fantomes comme des obstacles
        x et y : coordonnées actuelles
        x2 et y2 : coordonnées considérées
        """
        if x < x2 and (abs(x2-x)>=abs(y2-y)):
            #si le joueur est au dessus et plus loin verticalement
            if x2-1>=0 and carte[x2-1][y2] !=1 and carte[x2-1][y2] <6:
                # si il n'y a pas de mur sur le chemin
                return 'z'
            else:# Il y a un mur sur le chemin
                if y2-1>=0 and y2+1<len(carte[0]) and carte[x2][y2-1] == 1 \
                        and carte[x2][y2+1]!=1 and carte[x2][y2+1]<6:
                    #S'il y a un mur a gauche
                    return 'd'
                elif y2-1>=0 and y2+1<len(carte[0]) and carte[x2][y2+1] == 1 \
                        and carte[x2][y2-1] != 1 and carte[x2][y2-1] <6:
                    #S'il y a un mur a droite
                    return 'q'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2-1][y2] ==1 or carte[x2-1][y2] >= 6) \
                        and (carte[x2][y2+1]==1 or carte[x2][y2+1]>= 6) \
                        and (carte[x2][y2-1]==1 or carte[x2][y2-1]>= 6):
                    return 's'
                elif y2-1>=0 and y2+1<len(carte[0]) and carte[x2][y2-1] != 1 \
                        and carte[x2][y2+1] != 1:
                    #Il n'y a pas de mur ni a droite ni a gauche
                    choix=random.choice(['q','d'])
                    return choix # Au hasard a droite ou a gauche
    
        if x > x2 and (abs(x2-x)>=abs(y2-y)):
            #si le joueur est en dessous et plus loin verticalement
            if x2+1<len(carte) and carte[x2+1][y2] != 1 and carte[x2+1][y2] <6:
                # si il n'y a pas de mur sur le chemin
                return 's'
            else:# Il y a un mur sur le chemin
                if y2-1>=0 and y2+1<len(carte[0]) and carte[x2][y2-1] == 1 \
                        and carte[x2][y2+1]!=1 and carte[x2][y2+1]<6:
                    #S'il y a un mur a gauche
                    return 'd'
                elif y2-1>=0 and y2+1<len(carte[0]) and carte[x2][y2+1] == 1 \
                        and carte[x2][y2-1]!=1 and carte[x2][y2-1]<6:
                    #S'il y a un mur a droite
                    return 'q'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2+1][y2] ==1 or carte[x2+1][y2] >= 6) \
                        and (carte[x2][y2+1]==1 or carte[x2][y2+1]>= 6) \
                        and (carte[x2][y2-1]==1 or carte[x2][y2-1]>= 6):
                    return 'z'
                elif y2-1>=0 and y2+1<len(carte[0]) and carte[x2][y2-1] != 1 \
                        and carte[x2][y2+1] != 1:
                    #Il n'y a pas de mur ni a droite ni a gauche
                    choix=random.choice(['q','d'])
                    return choix # Au hasard a droite ou a gauche
    
        if y > y2 and (abs(y2-y)>abs(x2-x)):
            #si le joueur est à droite et plus loin horizontalement
            if y2+1<len(carte[0]) and carte[x2][y2+1]!=1 and carte[x2][y2+1]<6 :
                # si il n'y a pas de mur sur le chemin
                return 'd'
            else:# Il y a un mur sur le chemin
                if x2-1>=0 and x2+1<len(carte) and carte[x2-1][y2] == 1 \
                        and carte[x2+1][y2]!=1 and carte[x2+1][y2]<6:
                    #S'il y a un mur en haut
                    return 's'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] == 1 \
                        and carte[x2-1][y2]!=1 and carte[x2-1][y2]<6:
                    #S'il y a un mur en bas
                    return 'z'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2-1][y2] ==1 or carte[x2-1][y2] >= 6) \
                        and (carte[x2][y2+1]==1 or carte[x2][y2+1]>= 6) \
                        and (carte[x2+1][y2]==1 or carte[x2+1][y2]>= 6):
                    return 'a'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] != 1 \
                        and carte[x2-1][y2] != 1:
                    #Il n'y a pas de mur ni en haut ni en bas
                    choix=random.choice(['s','z'])
                    return choix # Au hasard en haut ou en bas
    
        if y < y2 and (abs(y2-y)>abs(x2-x)):
            #si le joueur est à gauche
            if y2-1>=0 and carte[x2][y2-1]!=1 and carte[x2][y2-1]<6:
                # si il n'y a pas de mur sur le chemin
                return 'q'
            else:# Il y a un mur sur le chemin
                if x2-1>=0 and x2+1<len(carte) and carte[x2-1][y2] == 1 \
                        and carte[x2+1][y2]!=1 and carte[x2+1][y2]<6:
                    #S'il y a un mur en haut
                    return 's'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] == 1 \
                        and carte[x2-1][y2]!=1 and carte[x2-1][y2]<6:
                    #S'il y a un mur en bas
                    return 'z'
                elif y2-1 >=0 and y2+1 < len(carte[0]) \
                        and x2-1 >=0 and x2+1 < len(carte) \
                        and (carte[x2-1][y2] ==1 or carte[x2-1][y2] >= 6) \
                        and (carte[x2][y2-1]==1 or carte[x2][y2-1]>= 6) \
                        and (carte[x2+1][y2]==1 or carte[x2+1][y2]>= 6):
                    return 'd'
                elif x2-1>=0 and x2+1<len(carte) and carte[x2+1][y2] != 1 \
                        and carte[x2-1][y2] != 1:
                    #Il n'y a pas de mur ni en haut ni en bas
                    choix=random.choice(['s','z'])
                    return choix # Au hasard en haut ou en bas





    def move_pac_et_fant(self): #C'est quoi ce monstre !!!!!!!!!!!!!!!!!!
        debut = time.time() #Enlever les print après
        """
        Mouvement du joueur et des fantomes
        Fonction appelée après que les décisions de mouvement pour les fantomes ont été appelées
        On agit sur carte, prend valeur de coordonnées pacman/fantomes
        dimensions d'une tuile,liste des pac-gommes dessinés
        """

        carte=self.carte 
        cotecarre=self.cotecarre
        x,y=self.x,self.y #Attention a leur valeur
        liste_fant=self.liste_fant
        canevas=self.canevas 
        pacman=self.pacman 
        red,blue,pink,orange=self.red,self.blue,self.pink,self.orange
        id_liste=self.id_liste #devrait pointer sur meme liste
        direction=self.direction #pareil que pour x,y
        compteur_fuite=self.compteur_fuite
        type_ia=self.type_ia
        score=self.score
        nombrevie=self.nombrevie
        move_adv=self.move_adv 
        checkvie=self.checkvie
    
        #print("ia :",type_ia)
        diff = cotecarre
        if self.direction == "": # si le joueur n'a pas encore joué
            return
            
        if direction == 'Down':
            if x+1 < len(carte) and carte[x+1][y] >= 6: #Si on tombe sur un fantome
                if type_ia != 6:
                    checkvie()
                    time.sleep(3) #on laisse un temps avant de reprendre
                else: #on mange le fantome
                    self.score+=600
                    for i in liste_fant: #on cherche quel fantome est mangé
                        print("i[0],i[1]",i[0],i[1]," coord de là ou va pacman :",x+1,y)
                        if i[0] == x+1 and i[1] == y:
                            carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                            i[0],i[1]=i[4],i[5] #On redonne les coord initiales
                            carte[i[0]][i[1]]=i[3] # a ces coord initiales, on lui remet sa valeur
                            i[6]=30 #On l'immobilise 30 tours
                            if i[3]==6:
                                canevas.delete(red) #mettre self ? ??????????????????????????????????????
                                red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                       (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                       fill='red',outline='')
                            if i[3]==7:
                                canevas.delete(pink)
                                pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='pink',outline='')
                            if i[3]==8:
                                canevas.delete(blue)
                                blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='cyan',outline='')
                            if i[3]==9:
                                canevas.delete(orange)
                                orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                          (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                          fill='orange',outline='')
                            carte[x-1][y]=3 #On deplace pacman
                            carte[x][y]=2
                            canevas.delete(pacman)
                            self.pacman=canevas.create_arc((y)*cotecarre+1,(x+1)*cotecarre+1,\
                                                          (y+1)*cotecarre-1,(x+2)*cotecarre-1,\
                                                          start=300,extent=300,\
                                                          fill="gold",outline="")#facedown
                            canevas.delete(id_liste[x][y])
                            self.x+=1
            else: 
                if x+1 >= len(carte) and carte[0][y] != 1: #si on est au bord de l'ecran
                    carte[0][y]=3
                    carte[x][y]=2
                    canevas.delete(id_liste[x][y])
                    canevas.move(pacman,0,-diff*(len(carte)-1))
                    self.x=0
                elif x+1 >= len(carte) and carte[0][y] == 1:
                    print("Ce n'est pas un warp, juste une erreur dans la construction de la map")
                elif carte[x+1][y] != 1:
                    if carte[x+1][y] == 4: #on trouve un powerup
                        self.type_ia=6
                        self.compteur_fuite=50
                        self.score+=90
                    elif carte[x+1][y]==0:
                        self.score+=30
                    carte[x+1][y]=3
                    carte[x][y]=2
                    canevas.delete(pacman)
                    self.pacman = canevas.create_arc((y)*cotecarre+1,(x+1)*cotecarre+1,\
                                                    (y+1)*cotecarre-1,(x+2)*cotecarre-1,\
                                                    start=300,extent=300,\
                                                    fill="gold",outline="")#facedown
                    canevas.delete(id_liste[x][y])
                    self.x+=1
                    
        elif direction == 'Up':
            if x-1 <0 and carte[x-1][y] >= 6: #on rencontre un fantome
                if type_ia != 6:
                    checkvie()
                    time.sleep(3)
                else:
                    self.score+=600
                    for i in liste_fant:
                        print("i[0],i[1]",i[0],i[1]," coord de là ou va pacman :",x+1,y)
                        if i[0] == x-1 and i[1] == y:
                            carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                            i[0],i[1]=i[4],i[5] #On redonne les coord initiales
                            carte[i[0]][i[1]]=i[3] # a ces coord initiales, on lui remet sa valeur
                            i[6]=30 #On l'immobilise 30 tours
                            if i[3]==6:
                                canevas.delete(red)
                                red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                       (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                       fill='red',outline='')
                            if i[3]==7:
                                canevas.delete(pink)
                                pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='pink',outline='')
                            if i[3]==8:
                                canevas.delete(blue)
                                blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='cyan',outline='')
                            if i[3]==9:
                                canevas.delete(orange)
                                orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                          (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                          fill='orange',outline='')
                            carte[x-1][y]=3 #On deplace pacman
                            carte[x][y]=2
                            canevas.delete(pacman)
                            self.pacman = canevas.create_arc((y)*cotecarre+1,(x-1)*cotecarre+1,\
                                                            (y+1)*cotecarre-1,(x)*cotecarre-1,\
                                                            start=120,extent=300,\
                                                            fill="gold",outline="")#faceup
                            canevas.delete(id_liste[x][y])
                            self.x-=1
            else:
                if x-1 <0 and carte[len(carte)-1][y] != 1:
                    carte[len(carte)-1][y]=3
                    carte[x][y]=2
                    canevas.delete(id_liste[x][y])
                    canevas.move(pacman,0,+diff*(len(carte)-1))
                    self.x=len(carte)-1
                elif x-1 < 0 and carte[len(carte)-1][y] == 1:
                    print("Ce n'est pas un warp, juste une erreur dans la construction de la map")
                elif carte[x-1][y] != 1:
                    if carte[x-1][y] == 4:
                        self.type_ia=6
                        self.compteur_fuite=50
                        self.score+=90
                    elif carte[x-1][y] == 0:
                        self.score+=30
                    carte[x-1][y]=3
                    carte[x][y]=2
                    canevas.delete(pacman)
                    self.pacman = canevas.create_arc((y)*cotecarre+1,(x-1)*cotecarre+1,\
                                                    (y+1)*cotecarre-1,(x)*cotecarre-1,\
                                                    start=120,extent=300,\
                                                    fill="gold",outline="")
                    canevas.delete(id_liste[x][y])
                    self.x-=1
    
        elif direction =='Left':
            if (y-1) >=0 and carte[x][y-1] >= 6:
                if type_ia != 6:
                    checkvie()
                    time.sleep(3)
                else:
                    self.score+=600
                    for i in liste_fant:
                        print("i[0],i[1]",i[0],i[1]," coord de là ou va pacman :",x+1,y)
                        if i[0] == x and i[1] == y-1:
                            carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                            i[0],i[1]=i[4],i[5] #On redonne les coord initiales
                            carte[i[0]][i[1]]=i[3] # a ces coord initiales, on lui remet sa valeur
                            i[6]=30 #On l'immobilise 30 tours
                            if i[3]==6:
                                canevas.delete(red)
                                red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                       (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                       fill='red',outline='')
                            if i[3]==7:
                                canevas.delete(pink)
                                pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='pink',outline='')
                            if i[3]==8:
                                canevas.delete(blue)
                                blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='cyan',outline='')
                            if i[3]==9:
                                canevas.delete(orange)
                                orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                          (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                          fill='orange',outline='')
                            carte[x-1][y]=3 #On deplace pacman
                            carte[x][y]=2
                            canevas.delete(pacman)
                            self.pacman = canevas.create_arc((y)*cotecarre-1,x*cotecarre+1,\
                                                            (y-1)*cotecarre+1,(x+1)*cotecarre-1,\
                                                            start=210,extent=300,\
                                                            fill="gold",outline="")
                            canevas.delete(id_liste[x][y])
                            self.y-=1
            else:
                if y-1 < 0 and carte[x][len(carte[0])-1] != 1 :
                    carte[x][len(carte[0])-1]=3
                    carte[x][y]=2
                    canevas.delete(id_liste[x][y])
                    canevas.move(pacman,+diff*(len(carte[0])-1),0)
                    self.y=len(carte[0])-1
                elif y-1 <0 and carte[x][len(carte[0])-1] == 1 :
                    print("Ce n'est pas un warp, juste une erreur dans la construction de la map")
                elif carte[x][y-1] != 1:
                    if carte[x][y-1] == 4:
                        self.type_ia=6
                        self.compteur_fuite=50
                        self.score+=90
                    elif carte[x][y-1] == 0:
                        self.score+=30
                    carte[x][y-1]=3
                    carte[x][y]=2
                    canevas.delete(pacman)
                    self.pacman = canevas.create_arc((y)*cotecarre-1,x*cotecarre+1,\
                                                    (y-1)*cotecarre+1,(x+1)*cotecarre-1,\
                                                    start=210,extent=300,\
                                                    fill="gold",outline="")
                    canevas.delete(id_liste[x][y])
                    self.y-=1
    
    
        elif direction == 'Right':
            if y+1 < len(carte[0]) and carte[x][y+1] >= 6:
                if type_ia != 6:
                    checkvie()
                    time.sleep(3)
                else:
                    self.score+=600
                    for i in liste_fant:
                        print("i[0],i[1]",i[0],i[1]," coord de là ou va pacman :",x+1,y)
                        if i[0] == x and i[1] == y+1:
                            carte[i[0]][i[1]] = 2 # on supprime le fantôme de la case
                            i[0],i[1]=i[4],i[5] #On redonne les coord initiales
                            carte[i[0]][i[1]]=i[3] # a ces coord initiales, on lui remet sa valeur
                            i[6]=30 #On l'immobilise 30 tours
                            if i[3]==6:
                                canevas.delete(red)
                                red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                       (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                       fill='red',outline='')
                            if i[3]==7:
                                canevas.delete(pink)
                                pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='pink',outline='')
                            if i[3]==8:
                                canevas.delete(blue)
                                blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                        (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                        fill='cyan',outline='')
                            if i[3]==9:
                                canevas.delete(orange)
                                orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                          (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                          fill='orange',outline='')
                            carte[x-1][y]=3 #On deplace pacman
                            carte[x][y]=2
                            canevas.delete(pacman)
                            self.pacman = canevas.create_arc((y+1)*cotecarre+1,x*cotecarre+1,\
                                                            (y+2)*cotecarre-1,(x+1)*cotecarre-1,\
                                                            start=30,extent=300,\
                                                            fill="gold",outline="")#faceright
                            canevas.delete(id_liste[x][y])
                            self.y+=1
            else:
                if y+1 >= len(carte[0]) and carte[x][0] != 1:
                    carte[x][0]=3
                    carte[x][y]=2
                    canevas.delete(id_liste[x][y])
                    canevas.move(pacman,-diff*(len(carte[0])-1),0)
                    self.y=0
                elif y+1> len(carte[0]) and carte[x][0] == 1:
                    print("Ce n'est pas un warp, juste une erreur dans la construction de la map")
                elif carte[x][y+1] != 1:
                    if carte[x][y+1] == 4:
                        self.type_ia=6
                        self.compteur_fuite=50
                        self.score+=90
                    elif carte[x][y+1] == 0:
                        self.score+=30
                    carte[x][y+1]=3
                    carte[x][y]=2
                    canevas.delete(pacman)
                    self.pacman = canevas.create_arc((y+1)*cotecarre+1,x*cotecarre+1,\
                                                    (y+2)*cotecarre-1,(x+1)*cotecarre-1,\
                                                    start=30,extent=300,\
                                                    fill="gold",outline="")
                    canevas.delete(id_liste[x][y])
                    self.y+=1
        #Fin des mouvements de Pac-Man
        #La partie qui suit devrait etre mieux commentée
        for i in liste_fant:
            if i[3]==6:
                i[6]-=1
                xs,ys=i[0],i[1]
                if compteur_fuite == 0:
                    self.type_ia=1
                if i[6] <= 0 : #S'il n'est pas immobilisé
                    x2,y2=move_adv(x,y,i[0],i[1],carte)
                else:
                    x2,y2=xs,ys
                if carte[x2][y2] == 3:
                    if type_ia != 6:
                        checkvie()
                        time.sleep(3)
                    else:
                        if i[3]==6:
                            canevas.delete(red)
                            red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                   (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                   fill='red',outline='')
                        if i[3]==7:
                            canevas.delete(pink)
                            pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='pink',outline='')
                        if i[3]==8:
                            canevas.delete(blue)
                            blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='cyan',outline='')
                        if i[3]==9:
                            canevas.delete(orange)
                            orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                      (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                      fill='orange',outline='')
                        continue
                if x2 == xs and y2 == ys:
                    carte[xs][ys]=2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                    i[2]=2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                else :
                    carte[xs][ys]=i[2]
                    i[2]=carte[x2][y2] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                carte[x2][y2]=i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)
    
                canevas.move(red,-(ys-y2)*cotecarre,-(xs-x2)*cotecarre)
    
            if i[3]==7:
                i[6]-=1
                xs,ys=i[0],i[1]
                if compteur_fuite == 0:
                    self.type_ia=1
                if i[6] <= 0 : #S'il n'est pas immobilisé
                    x2,y2=move_adv(x,y,i[0],i[1],carte)
                else:
                    x2,y2=xs,ys
                if carte[x2][y2] == 3:
                    if type_ia != 6:
                        checkvie()
                        time.sleep(3)
                    else:
                        if i[3]==6:
                            canevas.delete(red)
                            red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                   (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                   fill='red',outline='')
                        if i[3]==7:
                            canevas.delete(pink)
                            pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='pink',outline='')
                        if i[3]==8:
                            canevas.delete(blue)
                            blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='cyan',outline='')
                        if i[3]==9:
                            canevas.delete(orange)
                            orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                      (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                      fill='orange',outline='')
                        continue
                if x2 == xs and y2 == ys:
                    carte[xs][ys]=2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                    i[2]=2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                else :
                    carte[xs][ys]=i[2]
                    i[2]=carte[x2][y2] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                carte[x2][y2]=i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)
    
                canevas.move(pink,-(ys-y2)*cotecarre,-(xs-x2)*cotecarre)
    
            if i[3]==8:
                i[6]-=1
                xs,ys=i[0],i[1]
                if compteur_fuite == 0:
                    self.type_ia=1
                if i[6] <= 0 : #S'il n'est pas immobilisé
                    x2,y2=move_adv(x,y,i[0],i[1],carte)
                else:
                    x2,y2=xs,ys
                if carte[x2][y2] == 3:
                    if type_ia != 6:
                        checkvie()
                        time.sleep(3)
                    else:
                        if i[3]==6:
                            canevas.delete(red)
                            red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                   (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                   fill='red',outline='')
                        if i[3]==7:
                            canevas.delete(pink)
                            pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='pink',outline='')
                        if i[3]==8:
                            canevas.delete(blue)
                            blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='cyan',outline='')
                        if i[3]==9:
                            canevas.delete(orange)
                            orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                      (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                      fill='orange',outline='')
                        continue
                if x2 == xs and y2 == ys:
                    carte[xs][ys]=2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                    i[2]=2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                else :
                    carte[xs][ys]=i[2]
                    i[2]=carte[x2][y2] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                carte[x2][y2]=i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)
    
                canevas.move(blue,-(ys-y2)*cotecarre,-(xs-x2)*cotecarre)
    
            if i[3]==9:
                i[6]-=1
                xs,ys=i[0],i[1]
                if compteur_fuite == 0:
                    self.type_ia=1
                if i[6] <= 0 : #S'il n'est pas immobilisé
                    x2,y2=move_adv(x,y,i[0],i[1],carte)
                else:
                    x2,y2=xs,ys
                if carte[x2][y2] == 3:
                    if type_ia != 6:
                        checkvie()
                        time.sleep(3)
                    else:
                        if i[3]==6:
                            canevas.delete(red)
                            red=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                   (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                   fill='red',outline='')
                        if i[3]==7:
                            canevas.delete(pink)
                            pink=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='pink',outline='')
                        if i[3]==8:
                            canevas.delete(blue)
                            blue=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                    (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                    fill='cyan',outline='')
                        if i[3]==9:
                            canevas.delete(orange)
                            orange=canevas.create_oval(i[5]*cotecarre+1,i[4]*cotecarre+1,\
                                                      (i[5]+1)*cotecarre-1,(i[4]+1)*cotecarre-1,\
                                                      fill='orange',outline='')
                        continue
                if x2 == xs and y2 == ys:
                    carte[xs][ys]=2 #valeur sur laquelle etait le fantome !!!! A la premiere iteration bizarre; que pas erreur avec 3
                    i[2]=2 #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                else :
                    carte[xs][ys]=i[2]
                    i[2]=carte[x2][y2] #on donne la valeur de ce qui se trouve dans la case ou va aller le fantome
                carte[x2][y2]=i[3] #deplacement # !!! A MODIFIER (prendre valeur du fantome)
    
                canevas.move(orange,-(ys-y2)*cotecarre,-(xs-x2)*cotecarre)
    
            i[0],i[1]=x2,y2
        #print("fuite pour encore", compteur_fuite ,"tours")
        #print("dcore :",score)
        if compteur_fuite > 0 :
            self.compteur_fuite -= 1
        if 0 not in carte:
            print("VICTOIRE !!")
            self.affichage_fenetre_fin(v_ou_d=0)
            self.window.quit()
    
        self.Labelscore.destroy()
        self.Labelpower.destroy()
        self.Labelvie.destroy()
        self.Labelscore=tk.Label(self.window,text="Score:"+str(score))
        self.Labelpower=tk.Label(self.window,text="Tour d'immunite :"+str(compteur_fuite))
        self.Labelvie=tk.Label(self.window,text="Nombre de vie restantes :"+str(nombrevie))
        self.Labelpower.pack(side='bottom')
        self.Labelscore.pack(side='bottom')
        self.Labelvie.pack(side="bottom")
        fin = time.time() #a enlever après
        #print("{:.3f}".format((fin-debut)*10000))
        self.compteur_tour+=1
        if direction in ["Up","Down","Left","Right",""]:
            self.score-=10
            canevas.after(self.vitesse,self.move_pac_et_fant)
        print(carte,"\n") #debug, aenlever après
        #print("")
        

    def highscore(self):
        
        compteur_tour=self.compteur_tour
        score=self.score
        nom_map=self.nom_map
        pseudo=self.pseudo
        test_fichier="./Fichier_score"+nom_map[15:-3]+"score"
    
        texte_fichier=[]
        ligne_a_ajouter=[]
        
        if os.path.isfile(test_fichier) :
            with open(test_fichier,'r') as fichier:
                for ligne in fichier:
                    ligne = ligne[:-1]
                    ligne = ligne.split(" ")
                    ligne[0]=str(ligne[0])
                    ligne[1]=int(ligne[1])
                    ligne[2]=int(ligne[2])
                    texte_fichier.append(ligne)
                ligne_a_ajouter.append(str(pseudo))
                ligne_a_ajouter.append(int(compteur_tour))
                ligne_a_ajouter.append(int(score))
                texte_fichier.append(ligne_a_ajouter)
                texte_fichier.sort(key=lambda x: x[2],reverse=True)
                position = texte_fichier.index(ligne_a_ajouter)
    
            with open(test_fichier,'w') as fichier:
                for i in range(len(texte_fichier)):
                    fichier.write(str(texte_fichier[i][0]) + " ")
                    fichier.write(str(texte_fichier[i][1]) + " ")
                    fichier.write(str(texte_fichier[i][2]))
                    fichier.write("\n")
    
        else:
            with open(test_fichier,'w') as fichier:
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
        return position
        
    def affichage_fenetre_fin(self,v_ou_d):
        
        compteur_tour=self.compteur_tour
        score=self.score
        pseudo=self.pseudo
    
        fenetre_fin = tk.Toplevel()
    
        if v_ou_d == 0:
            texte_victoire="Bravo !!!\nTu as gagné cette partie très difficile d'un jeu merveilleusement bien codé\net ce par des personnes exceptionelles.\n\n\nTu as gagnés en {0} tours\nTu as eu un score de {1}".format(compteur_tour,score)
            message_victoire = tk.Label(fenetre_fin,text=texte_victoire)
            message_victoire.pack(padx=200,pady=50,side='top')
        elif v_ou_d == 1:
            texte_defaite="Dommage, tu as perdu !!!\nTu as perdu cette partie très difficile d'un jeu merveilleusement bien codé\net ce par des personnes exceptionnelles.\n\n\nTu as perdu en {0} tours\nTu as eu un score de {1}".format(compteur_tour,score)
            message_defaite = tk.Label(fenetre_fin,text=texte_defaite)
            message_defaite.pack(padx=200,pady=50,side='top')
    
        position = self.highscore()
    
        texte_position="Vous êtes {0}ème sur cette map.".format(position+1)
        if position == 0 :
            texte_position="Vous êtes PREMIER sur cette map, vous êtes un boss de Pacman."
        if position == -1 :
            texte_position="Vous êtes PREMIER sur cette map, vous êtes un boss de Pacman.\nEn même temps vous êtes le seul a avoir fais un score ^^."
    
        message_position = tk.Label(fenetre_fin,text=texte_position)
        message_position.pack(padx=200,pady=50,side='top')
    
        bouton_quitter2 = tk.Button(fenetre_fin, text="Quitter",command=sys.exit)
        bouton_quitter2.pack(expand=True,side = tk.BOTTOM)
        
    
        fenetre_fin.mainloop()

    
    
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!POUR LES METHODES (dans classe),METTRE SELF ? ET si dans methode canvas ?   
    
#class MovingObject():
 #   def __init__(self,root):
    





#Fonctions de gestion de mouvement_______________________________________________________






#Fonctions d'IA________________________________________________________________________________




#Fonctions de carte__________________________________________________________________

def is_legal(mapfile,verbose=False):
    """
    Fonction qui lit un fichier map et qui retourne un booléen indiquant si
    la carte est correcte dans son organisation.
    La fonction peut prendre un paramètre booléen verbose qui si Vrai, retourne
    pourquoi le fichier n'est pas valide.
    Si un fichier a des caractères non entiers, des lignes de taille différente,
    ou des lignes vides, il est non valide.
    """
    with open(mapfile,'r') as file1:
        ligne=file1.readline().replace(" ","")
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
            ligne=file1.readline().replace(" ","")
    return True


def ouvre_carte(mapfile):
    """
    ouvrecarte(mapfile)
    Cette fonction prend un fichier rempli d'entiers et retourne un ndarray
    """
    with open(mapfile,'r') as file1:
        ligne=file1.readline().replace(" ","")  #attention si mauvais formatage fichier
        cartetmp=[] #faire en sorte de completer si ligne vide ? si espace entre ligne
        while ligne !="": #ne marchera pas/mal si diff de lignes
            listeligne=[]
            for i in range(len(ligne)-1):
                listeligne.append(int(ligne[i])) #int !!! FAIRE UN TRY AU CAS OU non entier

            cartetmp.append(listeligne)
            ligne=file1.readline().replace(" ","")
    #print(np.array(cartetmp),np.argwhere(np.array(cartetmp == 3)))
    return np.array(cartetmp)


def resize_map(fenetre,carte,cotecarre=40):
    """
    Prend la fenetre Tk principale
    Permet de changer la résolution de la carte si la carte est plus grande que ce que peut afficher l'écran 
    Créée un canvas
    Retourne un element canvas et la taille des tuiles
    """

    largeurmax = fenetre.winfo_screenwidth() #on recupere taille de l'ecran
    hauteurmax = fenetre.winfo_screenheight()

    haut=(len(carte))*cotecarre
    lar=(len(carte[0]))*cotecarre

    while haut>hauteurmax or lar>largeurmax: #tant que la carte est trop grande pour l'écran
        cotecarre=cotecarre-10 #ou 5 ?
        haut=(len(carte))*cotecarre
        lar=(len(carte[0]))*cotecarre
    
    return tk.Canvas(fenetre,width=lar,height=haut,bg='black'),cotecarre


def locate_pacman(carte):
    """
    Prend une carte (numpyarray)
    Regarde si la carte est légale (possède un unique pacman) sinon quitte le programme
    Si un seul pacman est trouvé, on retourne ses coordonnées 
    """
    array_pac = np.argwhere(carte == 3)
    if len(array_pac) <1:
        if check_in_carte(3,carte) !=False:
            print("Passé par check")
            return check_in_carte(3,carte) #Bof complexite

    if(len(array_pac) > 1):
        print("ERREUR !! il y a plusieurs pacman")
        sys.exit()
    if (len(array_pac) <1): #resoudre avec map ?
        print("ERREUR !! il n'y a pas de pacman")
        sys.exit()
    return (array_pac[0,0],array_pac[0,1])


def locate_ghost(carte):
    """
    Prend une carte (numpyarray)
    Retourne une liste de liste des coordonnées de chaque fantome 
    et l'element de la case du fantome(vide, pac-gum...)
    0,1 : x,y
    2: case vide
    3: numero fantome
    4,5 : coord d'origine
    6: timer d'immobilisation
    """
    liste_fant=[]
    coord_fant=[]
    array_fant=np.argwhere(carte >= 6) #retourne une matrice avec les coordonnées des fantomes
    immobilisation=0

    for i in array_fant:
        coord_fant.append(i[0])
        coord_fant.append(i[1]) #raccourcir
        coord_fant.append(2) #on considere que le fantome est généré sur une case vide
        coord_fant.append(carte[i[0]][i[1]]) #rajoute valeur de case du fantome
        xor,yor=i[0],i[1] #on def les x et y d'origine en evitant le piège des pointeurs
        coord_fant.append(xor)
        coord_fant.append(yor)
        coord_fant.append(immobilisation) #par defaut le fantome n'a aucun tour d'immobilis
        liste_fant.append(coord_fant)
        coord_fant=[] #reinit pour prochain fantome
    return liste_fant
    
def check_in_carte(element,carte):
    """
    Verifie qu'un entier est dans un np array si argwhere echoue
    """
    #verifier element int, carte np array
    element_here=False
    for i in range(len(carte)):       
        for j in range(len(carte[0])):
            if carte[i,j]==element:
                return i,j #On ne verifie pas plusieurs pacmans
    return False


###ZONE DE TESTS______________________________________________
#x, y, liste_fant, cotecarre, direction, canevas, carte en var globales ici -> essayer d'enlever

#a=GestionMouvement("tmpcanevas")    
#print(a.carte)

root = AppliPrincipale() #on ouvre une instance de Tk
#carte = ouvre_carte(CARTE) #on lit une matrice
game = GestionMouvement(root)

