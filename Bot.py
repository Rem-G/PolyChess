from random import *

class Bot():

	def __init__(self, couleur, configuration):
		self.couleur = couleur
		self.configuration = configuration

	def randomChoice(self):
		"""
		:return: une liste contenant la position initiale de la pièce aléatoirement choisie
		et sa destination
		"""
		piece = choice(self.configuration.pieces_joueurN)						# Choix d'une pièce aléatoire
		moves = piece.PossibleMoves()[0] + piece.PossibleMoves()[1]		# Regroupement de l'ensemble des déplacements
																		## de la pièce en question
		return [piece.get_piece_position(), choice(moves)]