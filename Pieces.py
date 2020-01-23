class Piece:  # Classe mère
    def __init__(self, nom, pos_initiale):
        self.nom = nom
        self.position = pos_initiale

    def get_piece_position(self):
        """
        @TC
        """
        return self.position

    def set_piece_position(self, position):
        """
        :param position type (int, int): Coordonnees de la destination
        Met à jour la position du pion
        @TC
        """
        self.position = position


###########################################################################################################
###########################################################################################################

class Pion(Piece):                                          ############################################################
    def __init__(self, nom, pos_initiale):   #####ATTENTION: est ce que c'est checker le fait que #######
        super().__init__(nom, pos_initiale)  # la piece ne peut pas sauter par dessus les autres pieces##
        self.firstMove = True                               ############################################################
        self.promotion = True
        self.pos_initiale = pos_initiale

    def firstMoveOver(self):
        """
        Permet de mettre à jour l'etat du 1er tour du pion
        @TC
        """
        self.firstMove = False

    def PossibleMoves(self):
        """
        :return type list: Liste des moves possibles pour le pion
        @TC
        """
        moves, capture = [], []

        if self.nom == 'p':
            moves.append([self.position[0] + 1, self.position[1]])

            if self.position == self.pos_initiale: #pour eviter tout problemes, le bug vu avec thomas
                moves.append([self.position[0] + 2, self.position[1]])
                self.firstMoveOver()

            capture.append([self.position[0] + 1, self.position[1] - 1])
            capture.append([self.position[0] + 1, self.position[1] + 1])

        if self.nom == 'P':
            moves.append([self.position[0] - 1, self.position[1]])

            if self.position == self.pos_initiale: #pour eviter tout problemes, le bug vu avec thomas
                moves.append([self.position[0] - 2, self.position[1]])
                self.firstMoveOver()

            capture.append([self.position[0] - 1, self.position[1] - 1])
            capture.append([self.position[0] - 1, self.position[1] + 1])

        destination = [moves, capture]

        return destination


###########################################################################################################
###########################################################################################################


class Roi(Piece):

    def __init__(self, nom, pos_initiale):
        """@NR
        :type nom: string
        """
        super().__init__(nom, pos_initiale)
        self.pos_intiale = pos_initiale
        self.check = False
        self.checkMate = False

    def PossibleMoves(self):
        """ return une liste des moves possibles pour le roi @NR"""
        # je teste avec les coordonnees carstesiennes pas avec les coordonnes de l'echiquer

        x = self.position[0]
        y = self.position[1]

        # pour moi move et capture sont les meme

        moves = []  # list de move qui sont aussi des listes
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    moves.append([x + i, y + j])
        return [moves, moves]


###########################################################################################################
###########################################################################################################

class Tour(Piece):                                          ############################################################
    def __init__(self, nom, pos_initiale):                  #####ATTENTION: est ce que c'est checker le fait que #######
        super().__init__(nom, pos_initiale)                 # la piece ne peut pas sauter par dessus les autres pieces##
        self.pos_intiale = pos_initiale


    def PossibleMoves(self):
        '''
        Retourne la liste possible pour un tour
        @LV
        '''
        x = self.position[1]
        y = self.position[0]
        x1 = x
        y1 = y
        listC = []
        
        #D
        while x1 <8:
            x1 = x1+1
            y1 = y1
            listC.append([y1,x1])
            
        x1 = x
        y1 = y
        #G    
        while x1 >1 :
            x1 = x1-1
            y1 = y1
            listC.append([y1,x1])
        
        x1 = x
        y1 = y    
        #H    
        while y1 > 2:
            x1 = x1
            y1 = y1-1
            listC.append([y1,x1])
            
        x1 = x
        y1 = y    
        #B
        while y1 < 9:
            x1 = x1
            y1 = y1+1
            listC.append([y1,x1])

        return [listC, listC]


###########################################################################################################
###########################################################################################################

class Cavalier(Piece):
    def __init__(self, nom, pos_initiale):
        super().__init__(nom, pos_initiale)

    def PossibleMoves(self):
        """
		:return list: retourne la liste des mobves possibles pour le cavalier
		@TC
		"""
        moves = []

        x, y = self.position[0], self.position[1]

        moves.append([x + 2, y + 1])  # il a oublié les accolades pour dire que c'est une liste
        moves.append([x + 2, y - 1])
        moves.append([x + 1, y + 2])
        moves.append([x + 1, y - 2])
        moves.append([x - 2, y + 1])
        moves.append([x - 2, y - 1])
        moves.append([x - 1, y + 2])
        moves.append([x - 1, y - 2])

        return [moves, moves]


###########################################################################################################
###########################################################################################################


class Fou(Piece):                                           ############################################################
    def __init__(self, nom, pos_initiale):   #####ATTENTION: est ce que c'est checker le fait que #######
        super().__init__(nom, pos_initiale)  # la piece ne peut pas sauter par dessus les autres pieces##
                                                            ############################################################

    def PossibleMoves(self):
        '''
        Retourne la liste des mouvements d'un fou en connaissant  sa position initial
        @LV
        '''
        x = self.position[1]
        y = self.position[0]
        x1 = x
        y1 = y
        listeC = []
        
        #B-D
        while x1 >1 and y1 < 9:
            x1 = x1-1
            y1 = y1+1
            listeC.append([y1,x1])
        
        x1 = x
        y1 = y
        #B -G    
        while x1 <8 and y1 < 9:
            x1 = x1+1
            y1 = y1+1
            listeC.append([y1,x1])
        
        x1 = x
        y1 = y    
        #H - D    
        while x1 > 1 and y1 > 2:
            x1 = x1-1
            y1 = y1-1
            listeC.append([y1,x1])
            
        x1 = x
        y1 = y    
        #H - G
        while x1 < 8 and y1 > 2:
            x1 = x1+1
            y1 = y1-1
            listeC.append([y1,x1])
            
        return ([listeC,listeC])


###########################################################################################################
###########################################################################################################


class Dame(Piece):                                          
    def __init__(self, nom, pos_initiale):   
        super().__init__(nom, pos_initiale)  
                                                           

    def PossibleMoves(self):
        '''
        Retourne la liste des mouvements d'un fou en connaissant  sa position initial
        @LV
        '''
        x = self.position[1]
        y = self.position[0]
        listC = []
        x1 = x
        y1 = y        
        while x1 >1 and y1 < 9:
            x1 = x1-1
            y1 = y1+1
            listC.append([y1,x1])
        
        x1 = x
        y1 = y
        #B -G    
        while x1 <8 and y1 < 9:
            x1 = x1+1
            y1 = y1+1
            listC.append([y1,x1])
        
        x1 = x
        y1 = y    
        #H - D    
        while x1 > 1 and y1 > 2:
            x1 = x1-1
            y1 = y1-1
            listC.append([y1,x1])
            
        x1 = x
        y1 = y    
        #H - G
        while x1 < 8 and y1 > 2:
            x1 = x1+1
            y1 = y1-1
            listC.append([y1,x1])
            
#--------------------------------------------------------------            
        x1 = x
        y1 = y
        
        #D
        while x1 <8:
            x1 = x1+1
            y1 = y1
            listC.append([y1,x1])
            
        x1 = x
        y1 = y
        #G    
        while x1 >1 :
            x1 = x1-1
            y1 = y1
            listC.append([y1,x1])
        
        x1 = x
        y1 = y    
        #H    
        while y1 > 2:
            x1 = x1
            y1 = y1-1
            listC.append([y1,x1])
            
        x1 = x
        y1 = y    
        #B
        while y1 < 9:
            x1 = x1
            y1 = y1+1
            listC.append([y1,x1])

        return [listC, listC]
