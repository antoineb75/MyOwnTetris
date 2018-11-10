from tkinter import Tk, Label
from TetrisVar import COLOR, POINTS_SPEED
import datetime
import math
import re


def getColor(num):
    return COLOR[num]

def lost_procedure(widget):
    widget.create_rectangle(60,60,220,200, fill="white", width=2)
    widget.create_text(137, 115, text = 'Game Over')
   
def speed(score):
    mult = math.trunc(score.points/1000) * 1000
    return POINTS_SPEED[mult]

def crop(list):
    list_crop = []
    for i in list:
        val = i[2:12]
        list_crop.append(re.sub(r'[1-9]','1', val))
    return list_crop

