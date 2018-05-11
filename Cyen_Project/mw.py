import sys, xlrd, xlwt
from Tkinter import *
import tkFont as tkfont  # python 2

setMaj = None

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ChooseMaj, ChooseClasses, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ChooseMaj")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if page_name == "ChooseClasses":
            pass
        frame = self.frames[page_name]
        frame.tkraise()

class ChooseMaj(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label1 = Label(self, text="Please Select Your Major.", font=("Helvetica", 12))
        label1.grid(column=0, row=0, columnspan=2, sticky=W)

        majList, majDict = self.countMaj()

        self.buttonVar = StringVar()

        for i in range(len(majList)):
            name = majList[i]
            if majDict[name]:
                status = "active"
            else:
                status = "disabled"
            name = Radiobutton(self, text=name, value=name, variable=self.buttonVar, command=self.setMaj, state=status,font=("Helvetica", 10))
            name.grid(column=0, row=i+1, sticky=W)

        button1 = Button(self, text="Submit", command=lambda: controller.show_frame("ChooseClasses"))
        button1.grid(column=1, row=1, sticky=E)
        button2 = Button(self, text="Cancel", command=self.quit)
        button2.grid(column=1, row=2, sticky=E)

        label2 = Label(self, text="Greyed out options have not yet been implemented.", fg="darkgrey", font=("Helvetica", 8))
        label2.grid(column=0, row=len(majList)+1, columnspan=2)

    def countMaj(self):
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")

        majors = book.sheet_by_index(3)

        majList = []
        majDict = {}
        for i in range(majors.ncols):
            if majors.cell_value(rowx=1, colx=i) != "":
                status = True
            else:
                status = False
            majList.append(majors.cell_value(rowx=0, colx=i))
            majDict[majors.cell_value(rowx=0, colx=i)] = status

        return majList, majDict

    def setMaj(self):
        global selMaj
        selMaj = self.buttonVar.get()
        print selMaj

class ChooseClasses(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Please Select The Classes You've Taken", font=("Helvetica", 12), wraplength=500, justify=LEFT)
        label.grid(column=0, row=0, columnspan=2, sticky=W)

        courses = self.getCourses()

        listbox = Listbox(self)
        for course in courses:
            listbox.insert(END, course)
        listbox.grid(column=0, row=1, rowspan=4)

        button = Button(self, text="Go Back", command=lambda: controller.show_frame("ChooseMaj"))
        button.grid(column=2, row=6, sticky=E+W)

    def getCourses(self):
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")

        majors = book.sheet_by_index(3)

        courses = []
        for i in range(majors.ncols):
            if majors.cell_value(rowx=0, colx=i) != setMaj:
                index = i
                break
        for i in range(1, majors.nrows):
            courses.append(majors.cell_value(rowx=i, colx=index))

        return courses

class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
