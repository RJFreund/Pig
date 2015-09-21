from tkinter import *

'''
Player class
'''
class Player:
    def __init__(self):
        self.score = IntVar()
        self.dieRoll = IntVar()
        self.turnCounter = IntVar()
        self.turnTotal = IntVar()