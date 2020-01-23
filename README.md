# PolyChess - IDU3 - Polytech Annecy

#### Responsable de projet :
Gosselin Rémi
##### Membres du projet :
Razafindrabe Noah, Vieu Loïc, Gosselin Rémi, Cenci Thomas

Ce projet a pour but la création d'un jeu d'échecs en python. Celui-ci proposera deux modes de jeu : joueur contre joueur et joueur contre machine.
Le jeu se joue dans un terminal de commandes.

## Fonctionnalités:
Les fonctionnalités disponible sont les suivantes :
- **Un mode joueur contre joueur :** Ce mode de jeu permet d'affronter un autre joueur. Les règles de base des échecs sont       implémentées (les déplacements possibles, la mise en échec, échec et mat ainsi que le pat). Les coups spéciaux disponibles au échecs sont implémentés, tel que le roque, l'en passant et la promotion. A tout moment de la partie les joueurs peuvent voir les pièces détruites.
- **Sauvegarde d'une partie :** Un joueur peut sauvegarder une partie à tout moment et la reprendre plus tard.


## Pré-requis :
Python 3.x

## Lancement du jeu
Pour lancer le jeu, placez-vous dans le répertoire Polychess et lancez Main.py.
Tour à tour les joueurs communiquent leurs intentions de jeu selon le format suivant : x1y1 x2y2
x1y1 représentant les coordonnées initiales de la pièce à déplacer et x2y2 les coordonnées de la destination de la pièce.
**Exemple :** a2 a4

## Version interface utilisateur
Github : https://github.com/Rem-G/PolyChess_Django

Jouer en ligne : http://ceremi.pythonanywhere.com/polychess/

## Trello
https://trello.com/b/GnWD5gmq/polychess
----------

## Clone du projet
Permet de télécharger le projet en local
```bash
git clone https://github.com/Rem-G/PolyChess.git
```

## Mise à jour du dépôt local
A utiliser lorsque un dépôt local existe déjà
```bash
git pull origin [branch]
```

## Mise à jour du dépôt git
```bash
git add [fichiers modifiés]
git commit -m "Commit"
git push -u origin [branch]
```
