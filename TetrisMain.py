import time
from TetrisClass import Tetrimino, Gamefield, Score
from TetrisVar import TERRAIN, NEXT_GRID
from TetrisFunc import getColor, speed
from tkinter import *
import datetime
import sys

# animation des pieces du jeu master
def anime(manuel=False):
    global goOn
    try:
        global X, Y
        global piece
        global next_piece
        global terrain
        global score
        Y+=1
        goOn = piece.display(X, Y, terrain, 'D', score)
        if goOn == 0:
            Y=1
            score.points = 200
            leftPanel = Label(cadre, text='SCORE:\n{}'.format(score.points), anchor='n')
            leftPanel.grid(column=0, row=0)
            piece.swap(next_piece)
            next_piece.__init__()
            next_piece.display_next(nextPiece_cell)
            X = piece.Xinit
            Y = piece.Yinit
        assert goOn != -1 
    except AssertionError:
        displayGame.quit
    else:
        if not manuel:
            displayGame.after(speed(score),anime)

# déclenchement des mouvements suite aux captations des instructions clavier
def instr_move(event=None):
    global X, Y
    global piece
    global terrain
    try:
        if event.char == "w":
            tempX=X+1
            autorized = piece.display(tempX, Y, terrain, 'R', None)
            if autorized==1:
                X=tempX
        if event.char == "q":
            tempX=X-1
            autorized = piece.display(tempX, Y, terrain, 'L', None)
            if autorized==1:
                X=tempX
        if event.char == "p":
            piece.turn(terrain)
        if event.char == " ":
            anime(True)
    except:
        pass

# init : affichage du terrain de jeu
master = Tk()
master.title = ('Tetris')
cadre = Frame(master, width=768, height=576, borderwidth=2)
cadre.pack()

# init du score
score = Score()

# positionnement et affichage du score
leftPanel = Label(cadre, text='SCORE:\n{}'.format(score.points), anchor='n')
leftPanel.grid(column=0, row=0)

# positionnement et affichage du terrain de jeu
displayGame = Canvas(cadre, width=275, height=470)
displayGame.grid(column=1, row=1)
terrain = Gamefield(TERRAIN)
terrain.init_display(displayGame)

# positionnement et affichage du Tetri suivant
displayNext = Canvas(cadre, width=100, height=80)
displayNext.grid(column=0, row=1)
nextPiece_cell = Gamefield(NEXT_GRID)

next_piece = Tetrimino()
nextPiece_cell.init_display(displayNext)
next_piece.display_next(nextPiece_cell)

# init : affichage premier Tetrimino
piece = Tetrimino()

X, Y = piece.X, piece.Y

piece.display(piece.X, piece.Y,terrain, 'D', None)

# lancement de la boucle d'affichage et captation des instructions clavier
goOn = 1
anime()
displayGame.bind_all('<w>', instr_move) 
displayGame.bind_all('<q>', instr_move)  
displayGame.bind_all('<p>', instr_move)
displayGame.bind_all('<space>', instr_move)  

displayGame.mainloop()
