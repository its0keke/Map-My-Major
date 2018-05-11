from Tkinter import *
import xlrd

class MainGUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)


        self.frames = {}
        for F in (ChooseMaj, ChooseClass, ShowSched):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ChooseMaj")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def sub_switch(self, var):
        selection = var
        print selection
        self.show_frame("ChooseClass")

class ChooseMaj(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        majs = self.countMaj()

        # setup the grid
        for row in range(len(majs)+2):
            Grid.rowconfigure(self, row, weight=1)
        for col in range(2):
            Grid.columnconfigure(self, col, weight=1)

    	label = Label(text="Select Your Major:")
    	label.grid(column=0, row=0, sticky=E+W)

    	self.chosen_maj = StringVar()

        i = 1
        buttons = {}
        for major in majs:
            buttons[major] = Radiobutton(text=major, value=major, variable=self.chosen_maj, command=self.setMaj)
            buttons[major].grid(column=0, row=i, sticky=W)
            i += 1

        submit = Button(text="Submit", command=lambda: controller.show_frame("ChooseClass"))
        submit.grid(column=1, row=1)

        quit = Button(text="Quit", command=self.quit)
        quit.grid(column=1, row=2)

    def setMaj(self):
        global major
        major = self.chosen_maj.get()
        print major

    def countMaj(self):
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")

        majors = book.sheet_by_index(3)

        majs = []
        for i in range(majors.ncols):
            majs.append(majors.cell_value(rowx=0, colx=i))

        return majs

class ChooseClass(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        button1 = Button(self, text="Show Schedule!", command=lambda: controller.show_frame("ShowSched"))
        button1.pack()

class ShowSched(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        button1 = Button(self, text="Close.", command=lambda: app.quit())
        button1.pack()

if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
