import datetime
import time
import random
from tkinter import Label, Tk
from TetrisFunc import getColor, lost_procedure
from TetrisVar import DIM_BRIQUES, TERRAIN, TETRIMINOS

class Brick:
    """gestion de l'affichage des briques"""
    def __init__(self, widget, X, Y, color=""):
        self.X = X
        self.Y = Y
        self.H = DIM_BRIQUES
        self.L = DIM_BRIQUES
        self.widget=widget
        self.fig=widget.create_rectangle(self.X,self.Y,self.X+self.L,self.Y+self.H,fill=color, width=1, dash=(3, 5))

    def turnOn(self, color):
        self.widget.itemconfig(self.fig, fill=color)

class Gamefield:
    """Gestion du terrain de jeu"""
    def __init__(self, input_field):
        self._field = input_field['rep'] # liste de virtualisation du terrain de jeu
        self.L = input_field['L']   # Largeur du terrain
        self.H = input_field['H']   # Hauteur du terrain

    # initialisation du terrain dans l'interface graphique    
    def init_display(self, widget):
        self.widget = widget
        self.case = {}
        for j in range(1, self.H):
            for i in range(1, self.L-1):
                if self._field[j][i]!='0':
                    color = getColor(int(self._field[j][i]))
                else:
                    color = ''
                self.case[(i, j)] = Brick(self.widget, i*DIM_BRIQUES, j*DIM_BRIQUES, color) 

    def _getField(self):
        return self._field

    # mise à jour du terrain pour intégrer les Tetri immobilisés
    def _setField(self, pos_et_modif):
        compt_delete = 0

        Y = pos_et_modif[0]
        modified_field = pos_et_modif[1]
        score = pos_et_modif[2]

        # intégration dans le terrain du dernier Tetri immobilisé
        for rowNum, line in enumerate(modified_field):
            self._field[Y+rowNum] = line

        # suppression des lignes completes
        for num, line in enumerate(self._field[1:self.H-1], 1):
            delete = 1            
            for column in line[2:self.L-2]:
                if column == '0':
                    delete = 0
            if delete == 1:
                del self._field[num]
                self._field.insert(1, '11000000000011')
                compt_delete +=1

        score.points = (0, 50, 100, 150, 250)[compt_delete]

        # update affichage graphique du terrain
        for lineNb in range(1, self.H):
            for colNb in range(1, self.L-1):
                if colNb != "0":
                    color = getColor(int(self.field[lineNb][colNb]))
                    self.case[(colNb,lineNb)].turnOn(color)
                else:
                    color = getColor(int(self.field[lineNb][colNb]))
                    self.case[(colNb,lineNb)].turnOn(color)

        return self._field

    field = property(_getField, _setField)

class Tetrimino:
    """Gestion des Tetri jusqu'à immobilisation"""
    def __init__(self):
        self.type = random.choice(['barre', 'pistLeft', 'pistRight', 'cube', 'escRight', 'tripod', 'escLeft']) 
        self.Xinit = TETRIMINOS[self.type]['xInit']
        self.Yinit = 1
        self.X, self.Y = self.Xinit, self.Yinit
        self.pos = 1
        self.displayObj =  TETRIMINOS[self.type]['pos{}'.format(self.pos)]
        self.L = TETRIMINOS[self.type]['L']
        self.H = TETRIMINOS[self.type]['H']
    
    def swap(self, alter):
        self.type = alter.type 
        self.Xinit = alter.Xinit
        self.Yinit = alter.Yinit
        self.X, self.Y = alter.X, alter.Y
        self.pos = alter.pos
        self.displayObj =  alter.displayObj
        self.L = alter.L
        self.H = alter.H

    def display(self, X, Y, gamefield, event, score):
        autorized, cellTetri = self.move(X, Y, gamefield, event, score)
        if autorized:
            self.hide(gamefield, event)
            self.X, self.Y = X, Y
            for j in range(self.Y, self.Y+self.H):
                if j < gamefield.H:
                    for i in range(max(self.X,1), self.X+self.L):
                        if cellTetri[(i, j)] != "0":
                            color = getColor(int(cellTetri[(i, j)]))
                            gamefield.case[(i, j)].turnOn(color)
                        else:
                            color = getColor(int(gamefield.field[j][i]))
                            gamefield.case[(i,j)].turnOn(color)
            return 1
        elif cellTetri == []:
            return -1
        else:
            return 0

    def display_next(self, gamefield):
        for j in range(1, gamefield.H-1):
            for i in range(1, gamefield.L-1):
                color = getColor(int(gamefield.field[j][i]))
                gamefield.case[(i,j)].turnOn(color)

        for j in range(0, self.H):
            for i in range(0, self.L):
                if self.displayObj[j][i] != "0":
                    color = getColor(int(self.displayObj[j][i]))
                    gamefield.case[(i+1, j+1)].turnOn(color)
                else:
                    color = getColor(int(gamefield.field[j+1][i+1]))
                    gamefield.case[(i+1,j+1)].turnOn(color)

    def hide(self, gamefield, event):
        for j in range(self.Y, min(self.Y+self.H, gamefield.H-1)):
            for i in range(max(self.X,2), min(self.X+self.L, gamefield.L-2)):
                if gamefield.field[j][i] == "0":
                    gamefield.case[(i, j)].turnOn("")
            
    def move(self, X, Y, gamefield, event, score):
        cell = {}
        if self.detect_collision(X, Y, self.L, self.H, gamefield.field, self.displayObj) == []:
            for j in range(Y, Y+self.H):
                for i in range(X, X+self.L):
                    cell[(i,j)] = self.displayObj[j-Y][i-X]
            return True, cell
        else:
            if event == 'D':
                try:
                    assert self.Y != 1
                    newGF =  []
                    for j in range(self.Y, min(self.Y+self.H, gamefield.H-1)):
                        ligne = ''
                        for i in range(0, gamefield.L):
                            if i < self.X or i >= self.X+self.L:
                                ligne += gamefield.field[j][i]
                            elif i >= self.X and i < self.X+self.L:
                                if self.displayObj[j-self.Y][i-self.X] != '0':
                                    ligne += self.displayObj[j-self.Y][i-self.X]
                                else:
                                    ligne += gamefield.field[j][i]
                        newGF.append(ligne)
                    gamefield.field = [self.Y, newGF, score]
                    return False, gamefield.field
                except AssertionError:
                    lost_procedure(gamefield.widget)
                    return False, []

    def turn(self, gamefield, event = ''):
        if self.pos==4:
            self.pos=1
        else:
            self.pos+=1        
        try:
            self.displayObjTemp = TETRIMINOS[self.type]['pos{}'.format(self.pos)]
            assert self.detect_collision(self.X, self.Y, self.L, self.H, gamefield.field, self.displayObjTemp) == []
        except:
            pass
        else:
            self.hide(gamefield, event)
            self.displayObj = TETRIMINOS[self.type]['pos{}'.format(self.pos)]
            for j in range(self.Y, self.Y+self.H):
                if j < gamefield.H:
                    for i in range(self.X, self.X+self.L):
                        if self.displayObj[j-self.Y][i-self.X] != "0":
                            color = getColor(int(self.displayObj[j-self.Y][i-self.X]))
                            gamefield.case[(i, j)].turnOn(color)
                        else:
                            color = getColor(int(gamefield.field[j][i]))
                            gamefield.case[(i,j)].turnOn(color)

    def detect_collision(self, X, Y, L, H, display_gamefield, display_tetri):
        gamefield_cells = [int(display_gamefield[j][i]) for j in range(Y, Y+H) for i in range(X, X+L)]
        piece_cells = [int(display_tetri[j][i]) for j in range(0, H) for i in range(0, L)]
        collision = [(i, j)  for i, j in zip(gamefield_cells, piece_cells) if i != 0 and j != 0]
        return collision

class Score:
    def __init__(self):
        self._points = 0

    def _get_points(self):
        return self._points

    def _set_points(self, n):
        self._points += n

    points = property(_get_points, _set_points)