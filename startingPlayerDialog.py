import tkSimpleDialog
import tkinter as tk


class StartingPlayerDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		tk.Label(master, text="Select the starting player: ").grid(row=0, column=0)
		self.startingPlayer = tk.IntVar()
		tk.Radiobutton(master, text="Player 1", variable=self.startingPlayer, value=1, command=self.setOkButtonStatus).grid(row=1, column=0, sticky=tk.W)
		tk.Radiobutton(master, text="Player 2", variable=self.startingPlayer, value=2, command=self.setOkButtonStatus).grid(row=2, column=0, sticky=tk.W)

	def buttonbox(self):
		box = tk.Frame(self)

		self.okButton = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		self.okButton.pack(side=tk.LEFT, padx=5, pady=5)
		self.cancelButton = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		self.cancelButton.pack(side=tk.LEFT, padx=5, pady=5)

		self.okButton.config(state="disabled")

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	def setOkButtonStatus(self):
		if self.startingPlayer.get() == 0:
			return
		self.okButton.config(state="normal")

	def getStartingPlayer(self):
		return self.startingPlayer.get()
