# Pacman-C

Titre: Pacman en python

Auteur: -Ian KOSZO
        -Alexandre LECOEUR
        -Lilian YANG-CROSSON

Date de version: 16 / 09 / 2017

Package natif utiliser:
    -random
    -sys
    -math
    -time
    -os
    -tkinter
    -pathlib

Package a installer :
    -numpy pour la gestion de matrice
    (pip3 install numpy)

    -pygame pour la gestion du son
    (pip3 install pygame)

Description du projet:

Pour le lancer il faut lancer la commande python3 pacman.py.
Nous vous conseillons la map nommé niveau4.map , ou bien la map nommer niveau.map.

Ce projet est un jeu Pacman codé en python.
Il est composé du script python et de 3 dossiers:
    - Le dossier Fichier_map est là ou il y a toutes les maps et ou l'utilisateur peut mettre ces propres maps
    - Le dossier Fichier_score est là ou il y a tous les fichiers de score (1 par map)
    - Le dossier Fichier_son est là ou il y a les sons

Un fichier .map est un fichier contenu d'entiers, avec des lignes de meme taille (sans compter les espaces)
	- 0: pac-gomme
	- 1: mur
	- 2: vide
	- 3: pac-man
	- 4: power-up
	- 6 à 9: fantomes

Le script python commence par afficher une fenêtre de menu qui permet de configurer :
    - La taille d'une case de la map (Est ajuster si trop grande par rapport a la taille de l'écran)
    - Le niveaux de difficulté
    - Le nombre de vie
    - La vitesse du jeu
    - De rentrer son pseudo pour le highscore (Par défaut 'test')
    - De choisir sa map (Dans le dossier Fichier_map)
    - Il y a aussi un bouton pour lancer et un pour arrêter la musique

Pour lancer le jeu il faut sélectionner une map et cliquer sur lancer le jeu 

A ce moment là une nouvelle fenêtre apparaît et l'ancienne disparaît.
Pour lancer le jeu il faut appuyer sur start, puis se diriger avec les flèches directionnelles.
On peut mettre sur pause et quitter le jeu.
On peut aussi lancer ou stopper la musique.
Il y a marqué sur le coté le nombre de vie, le score et le nombre de tour d'immunité lorsque l'on a mangé un power up.

Pacman est en jaune, les 4 fantômes en rouge, cyan, rose et orange.
Les pacgum sont en jaune clair.
Les power up sont en violet.

Lorsque l'on perd ou que l'on gagne, le jeu se stop et une fenêtre apparaît et nous donne notre score et notre position dans le classement.
L'utilisation de power-up est possible mais entraîne cependant dans certains cas un bug de desynchronisation entre Tkinter et la matrice.



Nous avons essayer de réaliser le code en orienté objet, le code est situé dans le dossier orienté objet, mais par manque de temps il n'est pas parfait et bug parfois.

Pacman orienté objet
Le script est composé de trois classes:
_Une classe AppliPrincipale qui contient la fenetre tk mère
_Une classe StartMenu qui ouvre une instance frame qui va contenir
des widgets qui demanderont les configurations de jeu à l'utilisateur
(taille des tuiles, vitesse de jeu, difficulté, nombre de vies, pseudo et carte)
Si l'utilisateur ne selectionne rien, des valeurs par défaut seront renvoyées
_Une classe GestionMouvement qui va ouvrir une instance de StartMenu
y récuperer les variables entrées et créer dans la fenetre mère un canevas 
qui contiendra le jeu, et des boutons permettant de mettre en pause/quitter
ainsi que des informations sur le score, le nombre de vies... 
Toute la gestion du jeu se fait dans GestionMouvement
Une fois une condition de game over atteinte (victoire ou défaite)
une fenetre Toplevel s'ouvre dans GestionMouvement et donne les résultats
