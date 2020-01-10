from random import *

class Bot():

	def __init__(self, couleur, configuration):
		self.couleur = couleur
		self.configuration = configuration

	def PossibleMoves(self, pieces):
		"""
		:param pieces: listes des pièces attribuées au bot
		:return: la liste des déplacement que le bot peut effectuer
		@TC
		"""
		moves, capture = list(), list()

		for piece in self.configuration.pieces: # Création des listes de déplacements possibles et de captures possibles
			moves += piece.PossibleMoves()[0]	# pour toutes les pièces du BOT
			capture += piece.PossibleMoves()[1]

		return [moves, capture]

	def randomChoice(self):
		"""
		:return: une liste contenant la position initiale de la pièce aléatoirement choisie
		et sa destination
		@TC
		"""
		piece = choice(self.configuration.pieces)						# Choix d'une pièce aléatoire
		moves = piece.PossibleMoves()[0] + piece.PossibleMoves()[1]		# Regroupement de l'ensemble des déplacements
																		## de la pièce en question
		return (piece.get_piece_position(), choice(moves))