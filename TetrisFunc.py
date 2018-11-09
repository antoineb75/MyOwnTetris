from tkinter import Tk, Label
from TetrisVar import COLOR, POINTS_SPEED
import datetime
import math


def getColor(num):
    return COLOR[num]

def lost_procedure(widget):
    widget.create_rectangle(60,60,220,200, fill="white", width=2)
    widget.create_text(137, 115, text = 'Game Over')
   
def speed(score):
    mult = math.trunc(score.points/1000) * 1000
    return POINTS_SPEED[mult]