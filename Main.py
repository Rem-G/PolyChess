'''
Projet PolyChess - PROJ531
VIEU Loïc
CENCI Thomas
RAZAFINDRABE Noah
GOSSELIN Rémi
'''
from Configuration import *


# test commit


def init_pieces(configuration):
    """
    @RG @RN
    Initialisation des pièces de jeu
    Les noms en masjuscule représentent les pièces blanches, et ceux en minuscule les pièces noires
    """
    # Pieces blanches
    configuration.add_piece(Pion("P", [8, 1]))
    configuration.add_piece(Pion("P", [8, 2]))
    configuration.add_piece(Pion("P", [8, 3]))
    configuration.add_piece(Pion("P", [8, 4]))
    configuration.add_piece(Pion("P", [8, 5]))
    configuration.add_piece(Pion("P", [8, 6]))
    configuration.add_piece(Pion("P", [8, 7]))
    configuration.add_piece(Pion("P", [8, 8]))

    configuration.add_piece(Tour("T", [9, 1]))
    configuration.add_piece(Tour("T", [9, 8]))

    configuration.add_piece(Cavalier("C", [9, 2]))
    configuration.add_piece(Cavalier("C", [9, 7]))

    configuration.add_piece(Fou("F", [9, 3]))
    configuration.add_piece(Fou("F", [9, 6]))

    configuration.add_piece(Dame("D", [9, 4]))

    roiB = Roi("R", [9, 5])
    configuration.add_piece(roiB)
    configuration.init_roi(roiB)

    # Pieces noires
    configuration.add_piece(Pion("p", [3, 1]))
    configuration.add_piece(Pion("p", [3, 2]))
    configuration.add_piece(Pion("p", [3, 3]))
    configuration.add_piece(Pion("p", [3, 4]))
    configuration.add_piece(Pion("p", [3, 5]))
    configuration.add_piece(Pion("p", [3, 6]))
    configuration.add_piece(Pion("p", [3, 7]))
    configuration.add_piece(Pion("p", [3, 8]))

    configuration.add_piece(Tour("t", [2, 1]))
    configuration.add_piece(Tour("t", [2, 8]))

    configuration.add_piece(Cavalier("c", [2, 2]))
    configuration.add_piece(Cavalier("c", [2, 7]))

    configuration.add_piece(Fou("f", [2, 3]))
    configuration.add_piece(Fou("f", [2, 6]))

    configuration.add_piece(Dame("d", [2, 4]))

    roiN = Roi("r", [2, 5])
    configuration.add_piece(roiN)
    configuration.init_roi(roiN)


def affichage_plateau(matrice_affichage):
    """
    @RG
    Mise en forme de la matrice d'affichage pour l'affichage utilisateur
    Ajout repère
    Composition des lignes du plateau
    """
    ligne_valeurs = '   a b c d e f g h'
    colonne_valeurs = ['8', '7', '6', '5', '4', '3', '2', '1']
    ligne = 0

    for i in matrice_affichage:
        ch = str(colonne_valeurs[ligne] + '  ')
        ligne += 1
        for j in i:
            ch += str(j)
        print(ch)
    print('\n' + ligne_valeurs)


def decision_joueur(decision, configuration):
    """
    @RG
    :param decision: Choix de jeu du joueur en str
    :return list: Choix de jeu du joueur en list
    """

    # Conversion des coordonnées utilisateur en coordonnées matricielles

    decision = decision.split(" ")
    pos_depart = configuration.board.position_piece_mat([decision[0][0], decision[0][1]])
    pos_arrivee = configuration.board.position_piece_mat([decision[1][0], decision[1][1]])

    pos_depart = [int(pos) for pos in pos_depart]
    pos_arrivee = [int(pos) for pos in pos_arrivee]

    return [pos_depart, pos_arrivee]


def game_pvp():
    """
    @RG @NR
    """
    configuration = GeneralConf()

    # Crée les joueurs
    configuration.init_joueurs()

    # Crée les pièces de jeu
    new_game = input("Voulez-vous charger une partie existante ? Y/N ")

    if new_game == 'Y':
        configuration.charger_partie()
        joueur = configuration.joueur_sauvegarde
        print("Partie chargée !")
    else:
        init_pieces(configuration)
        joueur = 1

    # Attribution pièces de chaque joueur
    configuration.pieces_joueurs()

    # Affiche le palteau de jeu initial
    affichage_plateau(configuration.matrice_affichage())

    game = True

    while game:  # Rajouter option echec et mat + afficher pièces mangées
        if configuration.avantage_joueur():
            print('\n', configuration.avantage_joueur())

        if joueur == 1:
            configuration.affiche_case_cible()
            print("\nAu tour du joueur blanc")
            if configuration.est_en_echec(joueur):
                print("")
                print('\x1b[0;30;41m' + 'ATTENTION !' + '\x1b[0m') #couleur rouge
                print("Le roi blanc est en echec \nProtegez le !")

        else:
            print('\nAu tour du joueur noir')
            if configuration.est_en_echec(joueur):
                print("")
                print('\x1b[0;30;41m' + 'ATTENTION !' + '\x1b[0m')
                print("Le roi noir est en echec \nProtegez le !")

        input_decision = input("\nEntrer x1,y1 x2,y2  ou sauvegarde pour sauvegarder la partie et quitter: ")
        if input_decision == 'sauvegarde':
            configuration.sauvegarde_partie(joueur)
            print('Partie sauvegardée !')
            break
        else:
            decision = decision_joueur(input_decision, configuration)
            print('\n')
            if joueur == 1:
                configuration.deplacement_piece(decision[0], decision[1], True)
            else:
                configuration.deplacement_piece(decision[0], decision[1], False)

        affichage_plateau(configuration.matrice_affichage())

        for piece in configuration.pieces_joueurB:
            if piece.get_piece_position()[0] == 2 and piece.nom == 'P' and piece.promotion:
                configuration.promotion(piece)
                piece.promotion = False

        for piece in configuration.pieces_joueurN:
            if piece.get_piece_position()[0] == 9 and piece.nom == 'p' and piece.promotion:
                configuration.promotion(piece)
                piece.promotion = False

        if len(configuration.msg_error):
            for msg in configuration.msg_error:
                print("")
                print('\x1b[0;30;41m' + 'ATTENTION !' + '\x1b[0m')  # couleur rouge
                print(msg)

        if not len(configuration.msg_error):
            joueur = -joueur

        configuration.msg_error = list()


game_pvp()
