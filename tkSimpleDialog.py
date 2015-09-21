from tkinter import *

'''
Since Tkinter does not support
native complex dialog boxes,
this Dialog code was taken from:
http://effbot.org/tkinterbook/tkinter-dialog-windows.htm .
'''
class Dialog(Toplevel):

	def __init__(self, parent, title=None):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		if title:
			self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)
		self.buttonbox()
		self.isCancelPressed = BooleanVar()
		self.isCancelPressed.set(False)
		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (self.winfo_rootx()+50,
								  self.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = Frame(self)

		self.okButton = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		self.okButton.pack(side=LEFT, padx=5, pady=5)
		self.cancelButton = Button(box, text="Cancel", width=10, command=self.cancel)
		self.cancelButton.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def ok(self, event=NONE):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()
		self.parent.focus_set()
		self.destroy()

	def cancel(self, event=NONE):

		# put focus back to the parent window
		self.parent.focus_set()
		self.isCancelPressed.set(True)
		self.destroy()

	def isCancelButtonPressed(self):
		return self.isCancelPressed.get()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override