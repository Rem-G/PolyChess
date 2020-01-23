class Mat64():
	def __init__(self):
		pass

	def matrice_init(self):
		"""
		-1 représente une zone non accessible par une pièce de jeu
		:return list: Renvoie la matrice initiale de taille 12*10
		"""
		return [[-1]*10 for i in range(12)]

	def matrice_jeu(self):
		"""
		-1 représente une zone non accessible par une pièce de jeu
		:return new_board: Echequier de taille 12*10 pour une surface de jeu de 8*8 permettant de gêrer les débordements. Les emplacements jouables sont représentés par un entier différent de -1
		"""
		board = self.matrice_init()
		new_board = list()
		#Ajout 2 premières lignes de -1
		[new_board.append([-1]*10) for k in range(2)]
		pos = 0
		for i in board[2:len(board)-2]:
			k = i[:len(i)-1]
			for j in range(1,len(k)):
				k[j] = pos
				pos += 1
			k.append(-1)
			new_board.append(k)

		#Ajout 2 dernières lignes de -1
		[new_board.append([-1]*10) for k in range(2)]

		return new_board


	def position_piece_mat(self, piece_pos):
		"""
		Passe du référentiel joueur ex : a,2 au référentiel matriciel du plateau de jeu ex : 4,7
		:return list: Renvoie la position de la pièce dans le référentiel de la matrice de l'échéquier
		"""
		lignes_matrice = {'8' : 2, '7' : 3, '6' : 4, '5' : 5, '4': 6, '3' : 7, '2' : 8, '1' : 9}
		colonnes_matrice = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8 }

		if piece_pos[0] in colonnes_matrice.keys() and piece_pos[1] in lignes_matrice.keys():
			return [lignes_matrice[piece_pos[1]], colonnes_matrice[piece_pos[0]]]
		return [0,0]


	def valeur_position_piece_mat(self, piece_pos):
		"""
		:param piece_pos: Position de l'élément à retourner
		:return int: Renvoie d'une case de la matrice de jeu définie par rapport à sa position
		"""
		matrice = self.matrice_jeu()
		return matrice[piece_pos[0]][piece_pos[1]]

