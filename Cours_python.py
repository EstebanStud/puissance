
import numpy as np
import pygame
import sys
import math

# Les lignes suivantes servent à définir les couleurs des différents éléments de jeu en hexadecimal

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)

# Les 5 lignes en dessous permet de set up le tableau avec les différentes carractéristiques qu'on lui donne

RANGEE = 6 # Le nombre de rangée
COLONNE = 7 # le nombre de colonne
# Si on le souhaite nous pouvons mettre le nombre de rangée et colonne que l'on veut mais ici nous restons sur les dimension classiques d'un puissance

def creation_tableau():
	board = np.zeros((RANGEE,COLONNE))
	return board # le tableau est return avec 6 rangée et 7 colonne remplis de 0


# On init la fonctionalité du jeton ce qui va nous permettre de commencer à remplir le tableau
def jeton(board, row, col, piece):
	board[row][col] = piece

# Le but ici est de vérifier si l'emplacement où nous souhaitons mettre la pièce est disponible 
# Pour cela nous allons vérifier le nombre rangée rentrée -1 car nous commençons de 0 et si cette enplacement est libre donc égale à 0 alors la on pourra mettre le jeton
def validation_emplacement(board, col):
	return board[RANGEE-1][col] == 0

def prochain_tour(board, col):
	for r in range(RANGEE):
		if board[r][col] == 0:
			return r
 # De base numpy considére le point 0 - 0 comment la case qui est en haut à gauche et pas en bas à gauche ducoup cette fonction sert à inverser le tableau
def creation_board(board):
	print(np.flip(board, 0))


# Voila la partie la plus importante, le fait de vérifier après chaque fin de tour de tour si il y a une condition de victoire

def condition_victoire(board, piece):

	# Le système de verification de victoire pour la manière horrizontal et verticale est la même 
	# Le but ici est de trouver tous les emplacements où le premier jeton d'une suite de 4 pourrait commencer. C'est pour cela qu'on effectue un -3 sur les colonne pour le système horizontal 
	# et un -3 sur les rangées quand il s'agit de la verification verticale car il est impossible qu'une suite de jeton gagnant commence à jeton de la bordure.
	# La ligne suivante sert à chercher sur la totalité de la hauteur mais que sur la largeur -3  si une suite de jeton existe tout ca en ce regardant à chaque fois sur la case de droite
	# si il y a un jeton
	# C'est le meme fonctionnement pour la verticale sauf que c'est inversé


	# Verification de la condition de victoire à l'horizontal
	for c in range(COLONNE-3):
		for r in range(RANGEE):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Verification de la condition de victoire à la verticale
	for c in range(COLONNE):
		for r in range(RANGEE-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Pour ici c'est le même fonctionement sauf que pour la diagonale il faut prendre en compte plusieurs choses en plus 
	# 1/ il y'a moins de place pour effectuer une suite de 4 en diagonale car maintenant il faut retirer -3 à la hauteur ainsi que la largeur pour commencer une suite 
	# 2/ Maintenant il ne faut plus de déplacer dans l'axe X ou y mais maintenant il faut le faire en diagonal, logique. Cependant il faut diviser cette technique en 2 
	# car pour commencer une suite nous pouvons le faire de maniére croissante ou décroissante. Ce qui restreint encore la place


	# Verification de la condition de victoire en diagonale montante
	for c in range(COLONNE-3):
		for r in range(RANGEE-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece: #verification en diagonal
				return True

	# Verification de la condition de victoire en diagonale descendante
	for c in range(COLONNE-3):
		for r in range(3, RANGEE):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def mie_tableau(board):
	for c in range(COLONNE):
		for r in range(RANGEE):
			pygame.draw.rect(screen, BLACK, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS) # Creation des cercles à l'interieur de chaque petit carré 
	
	for c in range(COLONNE):
		for r in range(RANGEE):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = creation_tableau()
creation_board(board)
game_over = False
turn = 0

pygame.init() #initialisation de pygame

# Creation des dimentions du tableau 

# En dessous on definit la taille en pixel de toutes les zones où on pourra mettre une pièce 

SQUARESIZE = 100 # Chaque carré fera la taille de 100 px

# Ici on crée l'ensemble de l'espace de jeu en multipliant le nombre colonne par la taille de chaque zone pour créer la largeur
width = COLONNE * SQUARESIZE

# Cependant c'est différent pour la hauteur car il faut ajouter un de hauteur pour avoir la place de deplacé le jeton 
height = (RANGEE+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

# Ici on render l'espace de jeu pour que ca s'affiche
screen = pygame.display.set_mode(size)
mie_tableau(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	# Boucle pour fermer la page et le jeu quand on appuie sur la croix de fermeture
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	# Fonctionalité permetant de reconnaitre le tracking de la souris 
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

	# Fonctionalité permetant de reconnaitre le click de la souris 
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
			

			# Au tour du premier joueur de jouer 
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				# Mise en place de toutes les def expliqué au dessus

				if validation_emplacement(board, col):
					row = prochain_tour(board, col)
					jeton(board, row, col, 1)

					# Verification des différentes manières de gagner si elles sont rassemblés affiche le message de victoire

					if condition_victoire(board, 1):
						label = myfont.render("Le joueur 1 gagne!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True # On passe le game_over en true pour arréter le jeu


			# Au tour du deuxième joueur de jouer
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				# Mise en place de toutes les def expliqué au dessus

				if validation_emplacement(board, col):
					row = prochain_tour(board, col)
					jeton(board, row, col, 2)

				# Verification des différentes manières de gagner si elles sont rassemblés affiche le message de victoire

					if condition_victoire(board, 2):
						label = myfont.render("Le joueur 2 gagne!!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True # On passe le game_over en true pour arréter le jeu

			creation_board(board)
			mie_tableau(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)
