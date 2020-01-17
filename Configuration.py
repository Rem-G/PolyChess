from Board import *
from Pieces import *
from Bot import *
import os


class Joueur():
    def __init__(self, couleur, points=0):
        self.points = points
        self.couleur = couleur
        self.pieces_mangees = list()
        self.BOT = False

    def init_bot(self, configuration):
        """
        :param couleur:
        :param configuration:
        :return:
        """
        self.BOT = Bot(self.couleur, configuration)

    def add_point(self, piece):
        """
        @RG
        """
        points_pieces = {'p': 1, 'P': 1, 'f': 3, 'F': 3, 'c': 3, 'C': 3, 't': 5, 'T': 5, 'd': 9, 'D': 9}
        self.points += points_pieces[piece.nom]
        self.pieces_mangees.append(piece.nom)


class GeneralConf():
    def __init__(self):
        self.pieces = list()
        self.msg_error = list()
        self.board = Mat64()
        self.pieces_joueurB = list()
        self.pieces_joueurN = list()
        self.avantage = None
        self.died_pieces_B = list()
        self.died_pieces_N = list()
        self.in_promotion = False

    def sauvegarde_partie(self, joueur):
        """
        @RG
        Sauvegarde la partie (pièces, tour du joueur, avantage)
        """
        os.remove('sauvegarde.txt')
        for piece in self.pieces:
            with open('sauvegarde.txt', 'a+') as file:
                file.write(str([piece.nom, piece.position]) + '/')

        with open('sauvegarde.txt', 'a+') as file:
            file.write(str(self.died_pieces_B) + '/')
            file.write(str(self.died_pieces_N) + '/')
            file.write(str([self.joueurB.couleur, self.joueurB.points]) + '/')
            file.write(str([self.joueurN.couleur, self.joueurN.points]) + '/')

            file.write(str(joueur))

    def charger_partie(self):
        """
        @RG
        Charge une partie existante si le fichier sauvegade.txt existe
        """
        try:
            with open('sauvegarde.txt', 'r') as file:
                elements = file.readlines()
        except:
            elements = None
            print('Impossible de charger la sauvegarde')

        if elements:
            elements = elements[0].split("/")

            for element in elements[:len(elements) - 5]:
                element = element[1:len(element) - 1]
                nom_piece = element[1]
                coordonnees_pieces = [int(element[6]), int(element[9])]
                if nom_piece == 'p' or nom_piece == 'P':
                    self.add_piece(Pion(nom_piece, coordonnees_pieces))
                elif nom_piece == 'c' or nom_piece == 'C':
                    self.add_piece(Cavalier(nom_piece, coordonnees_pieces))
                elif nom_piece == 'f' or nom_piece == 'F':
                    self.add_piece(Fou(nom_piece, coordonnees_pieces))
                elif nom_piece == 't' or nom_piece == 'T':
                    self.add_piece(Tour(nom_piece, coordonnees_pieces))
                elif nom_piece == 'd' or nom_piece == 'D':
                    self.add_piece(Dame(nom_piece, coordonnees_pieces))
                elif nom_piece == 'r' or nom_piece == 'R':
                    roi = Roi(nom_piece, coordonnees_pieces)
                    self.add_piece(roi)
                    self.init_roi(roi)

            self.died_pieces_B =[e[1:len(e)-1] for e in elements[len(elements) - 5][1:len(elements[len(elements) - 5])-1].split(',')]#Récupération des pièces blanches mangées et mise en page de celles-ci sous forme de liste composée des noms des pièces
            self.died_pieces_N = [e[1:len(e)-1] for e in elements[len(elements) - 4][1:len(elements[len(elements) - 4])-1].split(',')]

            self.joueurB.couleur = elements[len(elements) - 3][2]
            self.joueurB.points = int(elements[len(elements) - 3][6])

            self.joueurN.couleur = elements[len(elements) - 2][2]
            self.joueurN.points = int(elements[len(elements) - 2][6])

            self.joueur_sauvegarde = int(elements[len(elements) - 1])

    def add_piece(self, piece):
        """
        @RG
        Ajoute une nouvelle pièce à la liste de pièces existantes
        """
        self.pieces.append(piece)

    def del_piece(self, piece):
        """
        @RG
        """
        if piece.nom.isupper() and self.in_promotion is False:
            self.died_pieces_B.append(piece.nom)
        elif piece.nom.islower() and self.in_promotion is False:
            self.died_pieces_N.append(piece.nom)
        self.pieces.pop(self.pieces.index(piece))

    def add_msg_error(self, msg):
        """
        @RG
        """
        if msg not in self.msg_error:
            self.msg_error.append(msg)

    def init_joueurs(self):
        """
        @RG
        Crée les joueurs (couleur, points à 0)
        """
        self.joueurB = Joueur('B')
        self.joueurN = Joueur('N')

    def avantage_joueur(self):
        """
        @RG
        :return str or None: Si un joueur a l'avantage, renvoie sa couleur et son score
        """
        if self.joueurB.points > self.joueurN.points:
            self.avantage = 'Avantage joueur blanc ' + str(self.joueurB.points - self.joueurN.points)

        elif self.joueurB.points < self.joueurN.points:
            self.avantage = 'Avantage joueur noir ' + str(self.joueurN.points - self.joueurB.points)

        else:
            self.avantage = None

        return self.avantage

    def pieces_joueurs(self):
        """
        """
        for piece in self.pieces:
            if piece.nom.isupper():
                self.pieces_joueurB.append(piece)  # NR il a oublié les self
            else:
                self.pieces_joueurN.append(piece)  # NR il a oublié les self

    def matrice_affichage(self):
        """
        @RG
        Génère la matrice d'interface utilisateur en supprimant les lignes de -1 et affichant le nom de chaque pièce en fonction de leur emplacement
        sur l'échiquier 
        :return matrice_screen: Matrice 8*8 avec le nom des pièces affiché sur leur position, les -1 de la matrice initiale sont convertis en '.'
        """
        matrice = self.board.matrice_init()

        for piece in self.pieces:
            pos = piece.get_piece_position()
            matrice[pos[0]][pos[1]] = piece.nom + ' '

        for index_i, i in enumerate(matrice):
            matrice[index_i] = i[1:len(
                i) - 1]  # Suppression du premier et dernier élément de la ligne -> suppression des -1
            for index_j, j in enumerate(i):
                try:  # Chaque ligne de la matrice étant redéfinie au dessus en supprimant la première et la dernière valeur
                    # le maximum d'index_i est plus élevé que la taille de la nouvelle ligne
                    if matrice[index_i][index_j] == -1:
                        matrice[index_i][index_j] = '. '
                except:
                    pass

        matrice_screen = matrice[2:len(matrice) - 2]
        pieces_mangees_B = '            Pieces blanches mangées ' + str(self.died_pieces_B)
        pieces_mangees_N = '            Pieces noires mangées ' + str(self.died_pieces_N)

        matrice_screen[len(matrice_screen)-5].append(pieces_mangees_B)
        matrice_screen[len(matrice_screen)-4].append(pieces_mangees_N)

        return matrice_screen


    def chemin_parcouru_piece(self, piece):
        """
        @RG
        """
        #Sauf Cavalier et Roi
        pass
        #if piece.__class__ is Cavalier:
            #for p in self.pieces:
                #if p.position in piece[0]:
                   #piece[0].pop(p.position)


    def verification_deplacement(self, moves, pos_arrivee):
        """
        @RG
        Vérifie si pour les mouvements d'une pièce donnée, sa position d'arrivée est autorisée
        Prend en compte les déplacements classiques ainsi que les déplacements pour manger une pièce adverse
        :param moves: Déplacements autorisés de la pièce
        :param pos_arrivee: Destination voulue par le joueur pour la pièce
        :return bool: Renvoie vrai si le déplacement est autorisé, faux sinon
        """
        possible_moves = moves[0]
        possible_eat = moves[1]

        emplacements_pieces = list()
        [emplacements_pieces.append(piece.position) for piece in self.pieces]

        if pos_arrivee in possible_moves and pos_arrivee not in emplacements_pieces or pos_arrivee in possible_eat:
            # Vérification si la position d'arrivee correspond à un mouvement autorisé et qu'elle n'est pas à l'emplacement d'une pièce existante
            # Si la position d'arrivée correspond à l'emplacement d'une pièce existante, on vérifie si elle peut être mangée
            if self.board.matrice_jeu()[pos_arrivee[0]][pos_arrivee[1]] != -1:
                # Vérification si la position d'arrivée voulue est sur le plateau de jeu
                return True
        return False


    def mange_piece(self, piece, possible_eat, pos_arrivee):
        """
        @RG @NR
        """
        for p in self.pieces:
            # Supprime une pièce adverse si la position d'arrivée voulue correspond à l'emplacement d'une pièce adverse
            if pos_arrivee == p.position and not(self.sameTeam(p, piece)) and pos_arrivee in possible_eat:
                if p.nom.islower():
                    self.joueurB.add_point(p)
                else:
                    self.joueurN.add_point(p)
                self.del_piece(p)
                piece.set_piece_position(pos_arrivee)




    def tour_joueur(self, piece, pos_arrivee):
        """
        @RG @NR
        Si le déplacement est autorisé, la position de la pièce change sinon affiche une erreur
        :param piece: Piece à vérifier
        :param pos_arrivee: Position d'arrivée désirée par le joueur pour la pièce
        """

        if piece.__class__ is Roi:  # on regarde si la piece en question en roi, au quel cas on doit verifier si le move entraine un echec ou echec et matt
            roque_roi_fait = False
            if piece.firstMove() == True:  # roi n'a pas encore joue son premier tour
                # on essaie le roque
                roque_roi_fait = self.roqueRoi(piece, pos_arrivee)

            if not (roque_roi_fait) and self.verification_deplacement_roi(piece, piece.PossibleMoves(), pos_arrivee):
                if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                    self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
                else:
                    piece.set_piece_position(pos_arrivee)
            else:
                if not (roque_roi_fait):
                    self.add_msg_error("déplacement interdit ou mise en échec du roi")

        if piece.__class__ is Tour:
            if self.verification_deplacement_tour(piece, piece.PossibleMoves(), pos_arrivee):
                if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                    self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
                else:
                    piece.set_piece_position(pos_arrivee)

            else:
                self.add_msg_error("Déplacement interdit")

        if piece.__class__ is Fou:
            if self.verification_deplacement_fou(piece, piece.PossibleMoves(), pos_arrivee):
                if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                    self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
                else:
                    piece.set_piece_position(pos_arrivee)

            else:
                self.add_msg_error("Déplacement interdit")

        if piece.__class__ is Dame:
            if self.verification_deplacement_dame(piece, piece.PossibleMoves(), pos_arrivee):
                if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                    self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
                else:
                    piece.set_piece_position(pos_arrivee)

            else:
                self.add_msg_error("Déplacement interdit")

        # NOTE : faire un verfification deplacement pour le pion

        if piece.__class__ is Pion:
            if self.verification_deplacement_pion(piece, piece.PossibleMoves(), pos_arrivee):
                if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                    self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
                else:
                    piece.set_piece_position(pos_arrivee)

            else:
                self.add_msg_error("Déplacement interdit")

        if piece.__class__ is Cavalier:
            if self.verification_deplacement_cavalier(piece, piece.PossibleMoves(), pos_arrivee):
                if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                    self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
                else:
                    piece.set_piece_position(pos_arrivee)

            else:
                self.add_msg_error("Déplacement interdit")

        # if (piece.__class__ != Roi) and (piece.__class__ != Tour) and (piece.__class__ != Fou) and(piece.__class__ != Dame) and((piece.__class__ != Pion)):
        #     print("cavalier")
        #     if self.verification_deplacement(piece.PossibleMoves(), pos_arrivee):
        #         print("1")
        #         if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
        #             self.mange_piece(piece, piece.PossibleMoves()[1], pos_arrivee)
        #         else:
        #             piece.set_piece_position(pos_arrivee)
        #
        #     else:
        #         self.add_msg_error("Déplacement interdit")

    def deplacement_piece(self, pos_depart, pos_arrivee, upper):
        """
        @RG
        Change de position une pièce selon la décision du joueur

        :param pos_depart: Position initiale de la pièce à bouger
        :param pos_depart: Position de destination de la pièce à bouger
        :param upper: Vérification du joueur faisant la requête : upper == True -> joueur blanc
        """
        coordonnees_pieces = list()
        # Vérification que la valeur de la position de départ dans la matrice de jeu est différente de 1
        if self.board.valeur_position_piece_mat(pos_depart) != -1 and self.board.valeur_position_piece_mat(
                pos_arrivee) != -1:
            for piece in self.pieces:
                ###########
                if piece.__class__ is Cavalier:
                    self.chemin_parcouru_piece(piece)
                ###########
                # Récupération et conversion des coordonnées utilisateur de la pièce en coordonnées de la matrice de jeu
                piece_x, piece_y = piece.get_piece_position()[0], piece.get_piece_position()[1]
                coordonnees_pieces.append([piece_x, piece_y])

                if piece_x == pos_depart[0] and piece_y == pos_depart[1]:
                    # Vérification de la position actuelle de la pièce et de la position de départ demandée par l'utilisateur
                    if upper is True:
                        # Tour du joueur blanc
                        if piece.nom.isupper():
                            # Vérification nom piece, affiche un message d'erreur si ce déplacement est interdit
                            self.tour_joueur(piece, pos_arrivee)

                        else:
                            self.add_msg_error("Cette pièce appartient à l'adversaire !")

                    else:
                        # Tour du joueur noir
                        if piece.nom.islower():
                            # Vérification nom piece, affiche un message d'erreur si ce déplacement est interdit
                            self.tour_joueur(piece, pos_arrivee)

                        else:
                            self.add_msg_error("Cette pièce appartient à l'adversaire !")

            if pos_depart not in coordonnees_pieces:
                # Vérifie si la position de départ entrée par le joueur correspond à l'emplacement d'une pièce
                self.add_msg_error("Aucune pièce ne correspond à ces coordonnées")

        else:
            # Si le joueur entre des coordonnées en dehor du plateau de jeu
            self.add_msg_error("Merci de jouer sur le plateau")

    ###############################################################
    ###FONCTIONS pour ROI et pour le jeu @NR
    ###############################################################
    def init_roi(self, roi):
        """
        init le roi au joueur, on crée un nouvel attribut a la classe joueur (roi)
        :param roi: piece roi
        """
        if roi.nom.isupper():
            self.joueurB.roi = roi
        else:
            self.joueurN.roi = roi

    def sameTeam(self, piece1, piece2):
        """ @NR
        verifie si piece 1 et piece 2 sont dans le meme equipe
        :param piece1 : une piece
        :param piece2 : une piece
        :return bool : renvoie vrai si piece 1 et piece 2 sont dans la meme equipe
        """
        if (piece1.nom.isupper() and piece2.nom.isupper()) or (piece1.nom.islower() and piece2.nom.islower()):
            return True
        return False

    def verification_deplacement_new(self, piece, moves, pos_arrivee):
        """
        @NR
        execute les verfication deplacement en fonction du type de la piece
        """
        if piece.__class__ is Roi:
            return self.verification_deplacement_roi(piece, moves, pos_arrivee)
        if piece.__class__ is Tour:
            return self.verification_deplacement_tour(piece, moves, pos_arrivee)
        if piece.__class__ is Fou:
            return self.verification_deplacement_fou(piece, moves, pos_arrivee)
        if piece.__class__ is Dame:
            return self.verification_deplacement_dame(piece, moves, pos_arrivee)
        if piece.__class__ is Pion:
            return self.verification_deplacement_pion(piece, moves, pos_arrivee)
        if piece.__class__ is Cavalier:
            return self.verification_deplacement_cavalier(piece, moves, pos_arrivee)

    def verification_deplacement_roi(self, roi, moves, pos_arrivee):  # OK marche
        """ @NR
        Verifie si le deplacement du roi est possible, sans l'emmener en echec
        :param roi: le roi
        :param moves: deplacements autorisés du roi
        :param pos_arrivee: Destination voulue par le joueur pour le roi
        :return bool : renvoie vrai si le deplacement est possible et faux sinon
        """

        possible_moves = moves[0]
        # pas de list possible_eat car c'est la même chose que possible moves pour le roi

        # modification des moves en prenant en compte l'etat de l'echiquier (postion des pieces)
        for piece in self.pieces:
            if piece.position in possible_moves and self.sameTeam(piece, roi):  # si sur l'emplacement ou
                # l'on veut se déplacer il y a déja un piece allié, on l'èleve de la liste
                possible_moves.remove(piece.position)
        # pas de probleme si l'emplacement est vide ou il y a un ennemi
        # erbo pour voir si sur ce coup le roi se met en echec

        # emplacements_reachable_by_opponent = list()  # emplacement que les ennemis peuvent atteindre
        # for piece in self.pieces:
        #     if not (self.sameTeam(piece, roi)):  # si la piece courante n'est pas dans la meme equipe que le roi
        #         for erbo in piece.PossibleMoves()[1]:  # emplacement de capture de la piece enemie
        #             if erbo not in emplacements_reachable_by_opponent:  # Pour ne pas avoir de doublon
        #                 emplacements_reachable_by_opponent.append(
        #                     erbo)  # on ajoute les emplacements de capture de chaque piece

        # emplacements_reachable_by_opponent = self.emplacements_reachable_by_opponent(roi)

        if (pos_arrivee in possible_moves) and not (self.case_menace(pos_arrivee[0], pos_arrivee[1],
                                                                     roi)):  # and (pos_arrivee not in emplacements_reachable_by_opponent)
            # verification si la position d'arrivee est dans les moves possibles et qu'il n'y pas de piece à cette emplacement ou que on peut manger une piece a cet emplacement
            # et que dans les deux cas la position d'arrivee ne soit pas un emplacement que pourrait prendre l'ennemi
            if self.board.matrice_jeu()[pos_arrivee[0]][pos_arrivee[1]] != -1:
                # Vérification si la position d'arrivée voulue est sur le plateau de jeu
                return True
        return False

    def verification_deplacement_tour(self, tour, moves, pos_arrivee):
        """
        @NR
        Verifie si le deplacement de la tour est possible
        :param tour: la tour
        :param moves: deplacements autorisés du tour
        :param pos_arrivee: Destination voulue par le joueur pour la tour
        :return bool : renvoie vrai si le deplacement est possible et faux sinon
        """
        possible_moves = moves[0]
        # pas de list possible_eat car c'est la même chose que possible moves pour le tour

        # NOTE : on ne verifie pas si pos_arrivee est dans les possibles moves car les if le font indirectement,
        # si pos arrivee est sur la même ligne ou sur la même colonne alors pos_arrivee est dans les PossibleMoves il
        # faut aussi gerer que la tour ne mange pas une piece allie OK
        # faut aussi le gerer pour le roi OK

        for piece in self.pieces:
            if piece.position == pos_arrivee and self.sameTeam(piece, tour): #on verfie si la case ou lon veut se deplacer n'est pas occupe par un allie
                return False

        # modification des moves en prenant en compte l'etat de l'echiquier (postion des pieces)
        if tour.position[0] == pos_arrivee[0] and tour.position[1]<pos_arrivee[1]: #même ligne, parcours de gauche vers la droite
            for posCol in range(tour.position[1] +1,pos_arrivee[1] ):
                if self.case_occupe(tour.position[0], posCol): #on regarde si les cases entre la tour et la pos arrivee son occupes
                    return False
            return True

        if tour.position[0] == pos_arrivee[0] and tour.position[1] > pos_arrivee[1]:  # même ligne, parcours de droite vers la gauche
            for posCol in range(tour.position[1]-1, pos_arrivee[1], -1):
                if self.case_occupe(tour.position[0],posCol):  # on regarde si les cases entre la tour et la pos arrivee son occupes
                    return False
            return True

        if tour.position[1] == pos_arrivee[1] and tour.position[0]<pos_arrivee[0]: #meme colonne, parcours du haut vers le bas
            for posLine in range(tour.position[0]+1, pos_arrivee[0]):
                if self.case_occupe(posLine, tour.position[1]):
                    return False
            return True

        if tour.position[1] == pos_arrivee[1] and tour.position[0]>pos_arrivee[0]: #meme colonne, parcours du bas vers le haut
            for posLine in range(tour.position[0]-1, pos_arrivee[0],-1):
                if self.case_occupe(posLine, tour.position[1]):
                    return False
            return True

        return False # car pos arrivee n'est pas dans les PossibleMoves (sur meme ligne ou meme colonne)

    def verification_deplacement_fou(self, fou, moves, pos_arrivee):
        """
         @NR
        Verifie si le deplacement du fou est possible
        :param fou: le fou
        :param moves: deplacements autorisés du tour
        :param pos_arrivee: Destination voulue par le joueur pour le fou
        :return bool : renvoie vrai si le deplacement est possible et faux sinon
        """
        possible_moves = moves[0]
        # pas de list possible_eat car c'est la même chose que possible moves pour le fou

        # NOTE : on ne verifie pas si pos_arrivee est dans les possibles moves car les if le font indirectement,(je verfie finalement)
        # si pos arrivee est sur une des diagonales alors pos_arrivee est dans les PossibleMoves du fou

        for piece in self.pieces:
            if piece.position == pos_arrivee and self.sameTeam(piece,
                                                               fou):  # on verfie si la case ou lon veut se deplacer n'est pas occupe par un allie
                return False

        if not(pos_arrivee in possible_moves):
            return False

        posLine = fou.position[0] #y de loic
        posCol = fou.position[1] #x de loic

        # modification des moves en prenant en compte l'etat de l'echiquier (postion des pieces)

        if fou.position[0] > pos_arrivee[0] and fou.position[1] > pos_arrivee[1]: #on parcours de droite a gauche et du bas vers le haut (diagonale)
            posCol = posCol - 1 #on commence apres et on s'arrete avant comme boucle for dans verification deplacement tour
            posLine = posLine - 1
            while (posLine >= pos_arrivee[0]+1) and (posCol >= pos_arrivee[1]+1):
                if posLine<1 or posCol<1 or self.case_occupe(posLine, posCol): #on verifie si on sort de lechiquier
                    return False
                posCol = posCol - 1  # bizarre incrementation
                posLine = posLine - 1
            return True

        if fou.position[0] > pos_arrivee[0] and fou.position[1] < pos_arrivee[1]: #on parcours  de gauche a droite et du bas vers le haut (diagonale)
            posCol = posCol + 1
            posLine = posLine - 1
            while (posLine >= pos_arrivee[0]+1) and (posCol <= pos_arrivee[1]-1):
                if posLine<1 or posCol >8 or self.case_occupe(posLine, posCol):
                    return False
                posCol = posCol + 1
                posLine = posLine - 1
            return True

        if fou.position[0] < pos_arrivee[0] and fou.position[1] > pos_arrivee[1]: #on parcours de droite a gauche et du haut vers le bas (diagonale)
            posCol = posCol - 1
            posLine = posLine + 1
            while (posLine <= pos_arrivee[0]-1) and (posCol >= pos_arrivee[1]+1):
                if posLine>9 or posCol<1 or self.case_occupe(posLine, posCol):
                    return False
                posCol = posCol - 1
                posLine = posLine + 1
            return True

        if fou.position[0] < pos_arrivee[0] and fou.position[1] < pos_arrivee[1]: #on parcours  de gauche a droite et du haut vers le bas (diagonale)
            posCol = posCol + 1
            posLine = posLine + 1
            while (posLine <= pos_arrivee[0]-1) and (posCol <= pos_arrivee[1]-1):
                if posCol>8 or posLine >9 or self.case_occupe(posLine, posCol):
                    return False
                posCol = posCol+1
                posLine = posLine+1
            return True

        return False #pos_arrivee n'est pas sur une diagonale

    def verification_deplacement_dame(self, dame, moves, pos_arrivee):
        """
         @NR
        Verifie si le deplacement de la dame est possible
        :param dame: la dame
        :param moves: deplacements autorisés du tour
        :param pos_arrivee: Destination voulue par le joueur pour la dame
        :return bool : renvoie vrai si le deplacement est possible et faux sinon
        """
        if self.verification_deplacement_tour(dame,moves, pos_arrivee) or self.verification_deplacement_fou(dame,moves, pos_arrivee):
            return True
        return False

    def verification_deplacement_pion(self, pion, moves, pos_arrivee):
        """
         @NR
        Verifie si le deplacement du pion est possible
        :param pion: le pion
        :param moves: deplacements autorisés du pion
        :param pos_arrivee: Destination voulue par le joueur pour le pion
        :return bool : renvoie vrai si le deplacement est possible et faux sinon
        """
        possible_moves = moves[0]
        possible_eat = moves[1]

        if pos_arrivee in possible_eat: #pour verifier l'attaque, on verifie si la position d'arrivee est dans les attaques du pion et si la position arrivee est occup par une piece enemi
            if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                for piece in self.pieces:
                    if piece.position == pos_arrivee and not(self.sameTeam(piece, pion)):
                        return True
            return False

        if pos_arrivee in possible_moves or (pos_arrivee in possible_eat): #on ne fait pas l'attaque ici mais dans la fonction mange_piece

            if pion.position[0]<pos_arrivee[0]:
                for posLine in (pion.position[0]+1, pos_arrivee[0]): #parours du haut vers le bas
                    if self.case_occupe(posLine, pion.position[1]):
                        return False
                return True
            if pion.position[0]>pos_arrivee[0]:
                for posLine in (pion.position[0]-1, pos_arrivee[0],-1):
                    if self.case_occupe(posLine, pion.position[1]): #parcrous du bas vers le heut
                        return False
                return True
        return False

    def verification_deplacement_cavalier(self, cavalier, moves, pos_arrivee):
        """
         @NR
        Verifie si le deplacement du cavalier est possible
        :param cavalier: le cavalier
        :param moves: deplacements autorisés du cavalier
        :param pos_arrivee: Destination voulue par le joueur pour le cavailier
        :return bool : renvoie vrai si le deplacement est possible et faux sinon
        """
        possible_moves = moves[0]

        if pos_arrivee in possible_moves:
            if self.case_occupe(pos_arrivee[0], pos_arrivee[1]):
                for piece in self.pieces:
                    if piece.position == pos_arrivee and self.sameTeam(piece, cavalier): #mouvement n'est pas possible si la pos arrivee est occupe par une piece allie
                        return False
            return True
        return False

    def roqueRoi(self, roi, pos_arrivee):
        """
        @NR
        applique le roque depuis le roi vers la tour
        :param roi : une piece roi
        :param pos_arrivee : la position d'arrivee, sur cette emplacement doit etre un roi ou une tour
        :return bool: true si le roque reussi, false sinon
        """
        tour_allie = list()  # tour_allie : list des tours de tour allie
        for piece1 in self.pieces:
            if piece1.__class__ is Tour and self.sameTeam(roi, piece1):
                tour_allie.append(piece1)
        for tour in tour_allie:
            if tour.position == pos_arrivee:
                if tour.firstMove():
                    for posCol in range(roi.get_piece_position()[1]+1, tour.get_piece_position()[1]):  # on parcours
                        # l'echiquier sur l'horizontale entre les 2 pieces (de gauche à droite)
                        if  self.case_occupe(roi.position[0], posCol) or self.case_menace(roi.position[0], posCol, roi):  # on
                            # ne peut pas faire le roque, si les cases entre le roi et la tour sont occupees ou menacees.
                            return False
                    #ou
                    for posCol in range(tour.get_piece_position()[1]+1, roi.get_piece_position()[1]):  # on parcours
                        # l'echiquier sur l'horizontale entre les 2 pieces (de doite à gauche)
                        if self.case_occupe(roi.position[0], posCol) or self.case_menace(roi.position[0], posCol, roi):
                            return False
                    # on fait le roque avec une permutation
                    line_roi = roi.get_piece_position()[0]
                    col_roi = roi.get_piece_position()[1]
                    line_tour = tour.get_piece_position()[0]
                    col_tour = tour.get_piece_position()[1]


                    if col_roi < col_tour:  # petit roque
                        col_roi = col_roi + 2
                        col_tour = col_tour - 2
                    else:  # grand roque
                        col_roi = col_roi - 2
                        col_tour = col_tour + 3

                    roi.set_piece_position([line_roi, col_roi])
                    tour.set_piece_position([line_tour, col_tour])
                    return True
        return False

    def case_occupe(self, posLine, posCol):
        """
        @NR
        :param posLine: position ligne
        :param posCol: position colonne
        :return bool: True si la case est occupe, False sinon
        """
        for piece in self.pieces:
            if piece.get_piece_position() == [posLine, posCol]:
                return True
        return False

    def case_menace(self, posLine, posCol, piece):
        """
        @NR vérifier si la case est menace par ennemi
        :param posLine:  position ligne INT
        :param posCol: position colonne INT
        :param piece: piece appartenant à l'équipe ami
        :return: True si la case est menace, False sinon
        """
        pos_arrivee = [posLine, posCol]
        for piece1 in self.pieces:
            if not self.sameTeam(piece, piece1):
                if self.verification_deplacement_new(piece1, piece1.PossibleMoves(),
                                                     pos_arrivee):  # si la piece enemi peut se deplacer sur cette case alors la case est menace
                    return True
        return False

    def est_en_echec(self, joueur):
        """
        @NR verifie si le joueur est en echec (mise en echec)
        :param joueur: INT 1 si joueur blanc sinon joueur noir
        :return: True si le joueur est en echec, False sinon
        """
        if joueur == 1:
            roi = self.joueurB.roi
        else:
            roi = self.joueurN.roi

        # for piece in self.pieces:
        #     #if piece.__class__ is Roi and not piece.nom == 'R'
        #     if not(self.sameTeam(piece, roi)): ## normalement a enlever piece.__class__ is Roi car on ne regarde pas que pour le roi mais tous les autres types de pieces
        #         if roi.position in piece.PossibleMoves()[1]: #Attention probleme avec possiblesMoves de la reine, et la tour, c'est pour ca que je mis le roi ennemi
        #             return True
        # return False

        if self.case_menace(roi.position[0], roi.position[1], roi):  # on regarde si la position du roi est menace
            return True
        return False

    def est_en_eche_et_mat(self,
                           joueur):  # si le roi est en echec et en echec aussi au prochain coup et aucune parade ne peut-etre faite
        """
        @NR verifie si le joueur est en echec et mat
        :param joueur:  INT 1 si joueur blanc sinon joueur noir
        :return: True si le joueur est en echec et mat, False sinon
        """
        if joueur == 1:
            roi = self.joueurB.roi
        else:
            roi = self.joueurN.roi

        if self.est_en_echec(joueur):
            # on test si le roi peut bouger
            for move_arrive in roi.PossibleMoves()[1]:
                if self.verification_deplacement_roi(roi, roi.PossibleMoves(),
                                                     move_arrive):  ### verfie si pour chaque coup du roi, il ne se met pas en echec
                    return False
            # il faut aussi verfier si une piece allie peut le sauver
            # Pour cela on test pour chaque piece, tout les coups possibles et on regarde si apres le roi n'est plus en echec
            for piece in self.pieces:
                if (piece is not roi) and (self.sameTeam(piece, roi)):
                    for move_allie in piece.PossibleMoves()[1]:
                        if self.verification_deplacement(piece.PossibleMoves(), move_allie):
                            # il faut maintenant tester: si on fait le coup, le roi est sauve ou pas
                            liste_pseudo_echiquier = self.pseudo_mange_piece(piece, piece.PossibleMoves()[1],
                                                                             move_allie)
                            if not (self.est_en_echec(joueur)):
                                piece.set_piece_position(liste_pseudo_echiquier[
                                                             0].position)  # on remet l'ancienne position de la piece (l'ancienne configuration)
                                if liste_pseudo_echiquier[1] is not None:
                                    self.add_piece(liste_pseudo_echiquier[
                                                       1])  # on rajoute la piece que l'on vient de supprimer, comme si il n'y avait pas eu de coup
                                return False
                            # on remet l'etat precedent de l'echiquier
                            piece.set_piece_position(
                                liste_pseudo_echiquier[0].position)  # on remet l'ancienne position de la piece
                            if liste_pseudo_echiquier[1] is not None:
                                self.add_piece(liste_pseudo_echiquier[
                                                   1])  # on rajoute la piece que l'on vient de supprimer, comme si il n'y avait pas eu de coup
            return True  # si il n'y pas de solution, on est en echec et mat
        return False

    def pseudo_mange_piece(self, piece, possible_eat, pos_arrivee):
        """
        pseudo bouge la piece a une nouvelle position
        :param piece: une piece
        :param possible_eat: emplacement ou la piece peut bouger
        :param pos_arrivee: emplacement ou la piece veut aller
        :return: une liste composé de la piece pseudo bouge et de la piece pseudo mange s'il y a
        """

        piece_pseudo_mange = None
        for p in self.pieces:
            # Supprime une pièce adverse si la position d'arrivée voulue correspond à l'emplacement d'une pièce adverse
            if pos_arrivee == p.position and pos_arrivee in possible_eat:
                piece_pseudo_mange = p
                self.del_piece(p)

        piece_pseudo_bouge = piece
        piece.set_piece_position(pos_arrivee)

        return [piece_pseudo_bouge, piece_pseudo_mange]

    def pat(self, joueur): # c'est a dire le roi du joueur n'est pas en echec mais il ne peut plus jouer de coup sans mettre son roi en echec
        """
        verifie si nous avons un pat
        :param joueur: INT 1 si joueur blanc sinon joueur noir
        :return: true si c'est le cas, false sinon
        """
        if joueur == 1:
            roi = self.joueurB.roi
        else:
            roi = self.joueurN.roi

        if not(self.est_en_echec(joueur)):
            # on test si le roi peut bouger
            for move_arrive in roi.PossibleMoves()[1]:
                if self.verification_deplacement_roi(roi, roi.PossibleMoves(),
                                                     move_arrive):  ### verfie si pour chaque coup du roi, il ne se met pas en echec
                    return False
            # il faut aussi verfier si une piece allie peut le sauver
            # Pour cela on test pour chaque piece, tout les coups possibles et on regarde si apres le roi n'est plus en echec
            for piece in self.pieces:
                if (piece is not roi) and (self.sameTeam(piece, roi)):
                    for move_allie in piece.PossibleMoves()[1]:
                        if self.verification_deplacement(piece.PossibleMoves(), move_allie):
                            # il faut maintenant tester: si on fait le coup, le roi est sauve ou pas
                            liste_pseudo_echiquier = self.pseudo_mange_piece(piece, piece.PossibleMoves()[1],
                                                                             move_allie)
                            if not (self.est_en_echec(joueur)):
                                piece.set_piece_position(liste_pseudo_echiquier[
                                                             0].position)  # on remet l'ancienne position de la piece (l'ancienne configuration)
                                if liste_pseudo_echiquier[1] is not None:
                                    self.add_piece(liste_pseudo_echiquier[
                                                       1])  # on rajoute la piece que l'on vient de supprimer, comme si il n'y avait pas eu de coup
                                return False
                            # on remet l'etat precedent de l'echiquier
                            piece.set_piece_position(
                                liste_pseudo_echiquier[0].position)  # on remet l'ancienne position de la piece
                            if liste_pseudo_echiquier[1] is not None:
                                self.add_piece(liste_pseudo_echiquier[
                                                   1])  # on rajoute la piece que l'on vient de supprimer, comme si il n'y avait pas eu de coup
            return True  # si il n'y pas de solution, on est en echec et mat
        return False



#######################################################################################################################
### FONTION POUR DEBUGGAGE  ##### @NR
#######################################################################################################################

###############################################################
###FONCTIONS PION @TC
###############################################################

    def promotion(self, piece):
        """
        promeut un pion en une piece choisie par l'utilisateur
        @TC
        """
        self.in_promotion = True
        position = piece.get_piece_position()
        if piece.nom.isupper:
            nom_piece = str(input(
                'Votre pion peut être promu, merci de choisir la nouvelle pièce :\nCavalier (C)\nFou (F)\nTour (T)\nDame (D)\n')).upper()
        else:
            nom_piece = str(input(
                'Votre pion peut être promu, merci de choisir la nouvelle pièce :\nCavalier (c)\nFou (f)\nTour (t)\nDame (d)\n')).lower()
        self.del_piece(piece)

        if nom_piece == 'C' or nom_piece == 'c':
            self.add_piece(Cavalier(nom_piece, position))

        elif nom_piece == 'F' or nom_piece == 'f':
            self.add_piece(Fou(nom_piece, position))

        elif nom_piece == 'T' or nom_piece == 't':
            self.add_piece(Tour(nom_piece, position))

        elif nom_piece == 'D' or nom_piece == 'd':
            self.add_piece(Dame(nom_piece, position))
        self.in_promotion = False
