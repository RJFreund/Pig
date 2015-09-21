#!/usr/bin/env python3

'''
R.J. Freund
Monday, September 21, 2015
CS 300 - Artificial Intelligence
Assignment 0
Professor George Thomas
'''

import tkinter as tk
import random
import startingPlayerDialog as spDialog
import selectOpponentDialog as soDialog
from tkinter import messagebox
import json
from Player import *

'''
Game class
'''
class Game(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.master.geometry("+%d+%d" % (self.winfo_rootx()+50, self.winfo_rooty()+50))
		self.master.title("Pig")
		'''
		Set game winning maximum points here.
		'''
		self.maximumPoints = tk.IntVar()
		self.maximumPoints.set(100)

		self.initializeVariables()
		self.resetGame()

		self.createWidgets()
		self.executePlayerTurn()

	def initializeVariables(self):
		self.hasPlayerWon = BooleanVar()
		self.player1 = Player()
		self.player2 = Player()
		self.isCancelButtonPressed = tk.BooleanVar()
		self.opponentType = tk.StringVar()
		self.playerTurn = tk.IntVar()

	'''
	Allows the user to save a game to a file from the point where it was stopped.
	'''
	def saveGameToFile(self):
		gameJson = {
			"player1Score" : self.player1.score.get(),
			"player1DieRoll" : self.player1.dieRoll.get(),
			"player1TurnCounter" : self.player1.turnCounter.get(),
			"player1TurnTotal" : self.player1.turnTotal.get(),

			"player2Score": self.player2.score.get(),
			"player2DieRoll": self.player2.dieRoll.get(),
			"player2TurnCounter": self.player2.turnCounter.get(),
			"player2TurnTotal": self.player2.turnTotal.get(),

			"playerTurn": self.playerTurn.get()
		}

		with open('saveGame.json', 'w') as outfile:
			json.dump(gameJson, outfile)

	'''
	Allows the user to load a game from a file from the point where it was stopped.
	Use of exception: ValueError exception when parsing int.
	'''
	def loadGameFromFile(self):
		with open('saveGame.json') as json_file:
			json_data = json.load(json_file)
			try:
				int(json_data['player1Score'])
				int(json_data['player1DieRoll'])
				int(json_data['player1TurnCounter'])
				int(json_data['player1TurnTotal'])
				int(json_data['player2Score'])
				int(json_data['player2DieRoll'])
				int(json_data['player2TurnCounter'])
				int(json_data['player2TurnTotal'])
				int(json_data['playerTurn'])
				self.player1.score.set(int(json_data['player1Score']))
				self.player1.dieRoll.set(int(json_data['player1DieRoll']))
				self.player1.turnCounter.set(int(json_data['player1TurnCounter']))
				self.player1.turnTotal.set(int(json_data['player1TurnTotal']))
				self.player2.score.set(int(json_data['player2Score']))
				self.player2.dieRoll.set(int(json_data['player2DieRoll']))
				self.player2.turnCounter.set(int(json_data['player2TurnCounter']))
				self.player2.turnTotal.set(int(json_data['player2TurnTotal']))
				self.playerTurn.set(int(json_data['playerTurn']))
			except ValueError:
				messagebox.showerror(title="Game Load Error", message="Some game data is invalid or corrupt and cannot be loaded correctly.")

	def isCancelPressed(self):
		return self.isCancelButtonPressed.get()

	def checkIfHasPlayerWon(self):
		if self.player1.score.get() >= self.maximumPoints.get():
			messagebox.showinfo(title="Winner!", message="Player 1 Wins!")
			self.hasPlayerWon.set(True)
			self.player1RollButton.config(state="disabled")
			self.player1HoldButton.config(state="disabled")
			self.player2RollButton.config(state="disabled")
			self.player2HoldButton.config(state="disabled")
			return
		if self.player2.score.get() >= self.maximumPoints.get():
			messagebox.showinfo(title="Winner!", message="Player 2 Wins!")
			self.hasPlayerWon.set(True)
			self.player1RollButton.config(state="disabled")
			self.player1HoldButton.config(state="disabled")
			self.player2RollButton.config(state="disabled")
			self.player2HoldButton.config(state="disabled")
			return

	def switchPlayers(self):
		self.checkIfHasPlayerWon()
		if self.hasPlayerWon.get():
			return
		if self.playerTurn.get() == 1:
			self.playerTurn.set(2)
		elif self.playerTurn.get() == 2:
			self.playerTurn.set(1)
		self.executePlayerTurn()

	'''
	Computer chooses randomly whether to hold or play during its turn.
	'''
	def executeComputerTurn(self):
		shouldRoll = True
		while shouldRoll:
			self.player2.turnCounter.set(self.player2.turnCounter.get() + 1)
			self.player2.dieRoll.set(self.getDieRollValue())
			if self.player2.dieRoll.get() == 1:
				self.player2.turnTotal.set(0)
				self.switchPlayers()
				break
			self.player2.turnTotal.set(self.player2.turnTotal.get() + self.player2.dieRoll.get())
			if random.randint(1, 10) > 5:
				self.player2Hold()
				break;

	'''
	Use of Exception
	'''
	def executePlayerTurn(self):
		if self.playerTurn.get() == 1:
			self.player2RollButton.config(state="disabled")
			self.player2HoldButton.config(state="disabled")
			self.player1RollButton.config(state="normal")
			self.player1HoldButton.config(state="normal")
		elif self.playerTurn.get() == 2:
			self.player1RollButton.config(state="disabled")
			self.player1HoldButton.config(state="disabled")

			if self.opponentType.get() == "computer":
				self.executeComputerTurn()
				return

			self.player2RollButton.config(state="normal")
			self.player2HoldButton.config(state="normal")

	def createWidgets(self):
		tk.Label(self, text="Player 1 Score: ").grid(row=0, column=0, sticky=tk.W)
		tk.Label(self, textvariable=self.player1.score).grid(row=0, column=1, sticky=tk.W)
		tk.Label(self, text="Player 1 Turn Total: ").grid(row=1, column=0, sticky=tk.W)
		tk.Label(self, textvariable=self.player1.turnTotal).grid(row=1, column=1, sticky=tk.W)
		tk.Label(self, text="Player 1 Die Roll: ").grid(row=2, column=0, sticky=tk.W)
		tk.Label(self, textvariable=self.player1.dieRoll).grid(row=2, column=1, sticky=tk.W)
		tk.Label(self, text="Player 1 Turn Counter: ").grid(row=3, column=0, sticky=tk.W)
		tk.Label(self, textvariable=self.player1.turnCounter).grid(row=3, column=1, sticky=tk.W)

		self.player1RollButton = tk.Button(self, text="Player 1 Roll", command=self.player1RollDie)
		self.player1RollButton.grid(row=4, column=0, sticky=tk.E)
		self.player1HoldButton = tk.Button(self, text="Player 1 Hold", command=self.player1Hold)
		self.player1HoldButton.grid(row=4, column=1, sticky=tk.W)

		tk.Label(self, text="Player 2 Score: ").grid(row=0, column=2, sticky=tk.W)
		tk.Label(self, textvariable=self.player2.score).grid(row=0, column=3, sticky=tk.W)
		tk.Label(self, text="Player 2 Turn Total: ").grid(row=1, column=2, sticky=tk.W)
		tk.Label(self, textvariable=self.player2.turnTotal).grid(row=1, column=3, sticky=tk.W)
		tk.Label(self, text="Player 2 Die Roll: ").grid(row=2, column=2, sticky=tk.W)
		tk.Label(self, textvariable=self.player2.dieRoll).grid(row=2, column=3, sticky=tk.W)
		tk.Label(self, text="Player 2 Turn Counter: ").grid(row=3, column=2, sticky=tk.W)
		tk.Label(self, textvariable=self.player2.turnCounter).grid(row=3, column=3, sticky=tk.W)

		self.player2RollButton = tk.Button(self, text="Player 2 Roll", command=self.player2RollDie)
		self.player2RollButton.grid(row=4, column=2, sticky=tk.E)
		self.player2HoldButton = tk.Button(self, text="Player 2 Hold", command=self.player2Hold)
		self.player2HoldButton.grid(row=4, column=3, sticky=tk.W)

		self.saveGameButton = tk.Button(self, text="Save Game", command=self.saveGameToFile)
		self.saveGameButton.grid(row=5, column=0, sticky=tk.E)
		self.loadGameButton = tk.Button(self, text="Load Game", command=self.loadGameFromFile)
		self.loadGameButton.grid(row=5, column=1, sticky=tk.W)
		self.newGameButton = tk.Button(self, text="New Game", command=self.resetGame)
		self.newGameButton.grid(row=5, column=3, sticky=tk.E)

	'''
	Sets players' scores to zero,
	allows the user to play against the computer or another user,
	and gives the user the option to choose who starts the game
	'''
	def resetGame(self):
		'''
		Sets players' scores to zero,
		'''
		self.hasPlayerWon.set(False)
		self.player1.score.set(0)
		self.player1.dieRoll.set(0)
		self.player1.turnCounter.set(0)
		self.player1.turnTotal.set(0)
		self.player2.score.set(0)
		self.player2.dieRoll.set(0)
		self.player2.turnCounter.set(0)
		self.player2.turnTotal.set(0)
		self.isCancelButtonPressed.set(False)

		'''
		Allows the user to play against the computer or another user.
		'''
		selectOpponentDialog = soDialog.SelectOpponentDialog(self)
		self.opponentType.set(selectOpponentDialog.getOpponentType())

		if selectOpponentDialog.isCancelButtonPressed():
			self.isCancelButtonPressed.set(True)
			self.master.quit()
			return

		'''
		Gives the user the option to choose who starts the game
		'''
		startingPlayerDialog = spDialog.StartingPlayerDialog(self)
		self.playerTurn.set(startingPlayerDialog.getStartingPlayer())

		if startingPlayerDialog.isCancelButtonPressed() or selectOpponentDialog.isCancelButtonPressed():
			self.isCancelButtonPressed.set(True)
			self.master.quit()
			return

	def player2RollDie(self):
		self.player2.turnCounter.set(self.player2.turnCounter.get() + 1)
		self.player2.dieRoll.set(self.getDieRollValue())
		if self.player2.dieRoll.get() == 1:
			self.player2.turnTotal.set(0)
			self.switchPlayers()
			return;
		self.player2.turnTotal.set(self.player2.turnTotal.get() + self.player2.dieRoll.get())

	def player2Hold(self):
		self.player2.score.set(self.player2.score.get() + self.player2.turnTotal.get())
		self.player2.turnTotal.set(0)
		self.switchPlayers()

	def player1RollDie(self):
		self.player1.turnCounter.set(self.player1.turnCounter.get() + 1)
		self.player1.dieRoll.set(self.getDieRollValue())
		if self.player1.dieRoll.get() == 1:
			self.player1.turnTotal.set(0)
			self.switchPlayers()
			return;
		self.player1.turnTotal.set(self.player1.turnTotal.get() + self.player1.dieRoll.get())

	def player1Hold(self):
		self.player1.score.set(self.player1.score.get() + self.player1.turnTotal.get())
		self.player1.turnTotal.set(0)
		self.switchPlayers()

	def getDieRollValue(self):
		return random.randint(1, 6)

app = Game()
if app.isCancelPressed():
	app.destroy()
else:
	app.mainloop()
