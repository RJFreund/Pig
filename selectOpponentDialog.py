import tkSimpleDialog
import tkinter as tk

class SelectOpponentDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		tk.Label(master, text="Select your opponent type: ").grid(row=0, column=0)
		self.opponentType = tk.StringVar()
		self.opponentType.set("none")
		tk.Radiobutton(master, text="Computer", variable=self.opponentType, value="computer", command=self.setOkButtonStatus).grid(row=1, column=0, sticky=tk.W)
		tk.Radiobutton(master, text="Human", variable=self.opponentType, value="human", command=self.setOkButtonStatus).grid(row=2, column=0, sticky=tk.W)

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
		if self.opponentType.get() == "none":
			return
		self.okButton.config(state="normal")

	def getOpponentType(self):
		return self.opponentType.get()
