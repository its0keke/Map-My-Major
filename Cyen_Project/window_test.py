from Tkinter import *

# the main GUI
class PageOne(Frame):

	# the constructor
	def __init__(self, parent):

		# initialize the window withe white background
		Frame.__init__(self, parent, bg="white")
		# run the setupGUI() function
		self.setupGUI()

	# sets up the GUI
	def setupGUI(self):
		# setup the grid
		for row in range(8):
			Grid.rowconfigure(self, row, weight=1)
		for col in range(8):
			Grid.columnconfigure(self, col, weight=1)

		major = Label(text="Select Your Major:")
		major.grid(column=0, row=0)

		maj_var = StringVar()
		cyen = Radiobutton(text="Cyber Engineering", variable=maj_var, value="cyen")
		cyen.grid(column=0, row=1, sticky=W)

		math = Radiobutton(text="Mathematics", variable=maj_var, value="math")
		math.grid(column=0, row=2, sticky=W)

		bme = Radiobutton(text="Biomedical Engineering", variable=maj_var, value="bme")
		bme.grid(column=0, row=3, sticky=W)

		submit = Button(text="Submit", command=lambda: controller.show_frame(PageTwo))
		submit.grid(column=0, row=8, sticky=W)

		quit = Button(text="Quit", command=self.quit)
		quit.grid(column=8, row=8, sticky=E)

	def sub(self, val):
		print val.get()
		controller.show_frame(PageTwo)

class PageTwo(Frame):

	# the constructor
	def __init__(self, parent):

		# initialize the window withe white background
		Frame.__init__(self, parent, bg="white")

# create the window
window = Tk()
# restrict resizing
window.resizable(0,0)
# get screen resolution to set window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# set window size to a third of the screen resolution
window.geometry("{}x{}".format(screen_width/2, screen_height/2))
# set the window title
window.title("Schedule Me Please.")
# generate the GUI
p = PageOne(window)
# displat the GUI and wait for user interaction
window.mainloop()
