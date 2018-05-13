# module needed to communicate with spreadsheet file
import xlrd, xlwt
# module responsible for gui
from Tkinter import *
# import for the error message
import tkMessageBox as Messagebox

# global variable for major and taken_classes
major = None
taken_classes = None

# the general class for the app
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(ChooseMaj)

    def switch_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nsew")

    def quit(self):
        answer = str(Messagebox.askquestion("", "Are you sure you want to quit?"))
        if answer == "yes":
            exit(0)

class ChooseMaj(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.majors = self.countMaj()

        label = Label(self, text="Please Select Your Major", font=("Helvetica", 10), anchor=CENTER)
        label.grid(row=0, column=1, columnspan=5, sticky="nsew", padx=10, pady=5)

        listbox = Listbox(self, selectmode=SINGLE)
        # add each valid major to the listbox
        for i in self.majors:
            listbox.insert(END, i)
        listbox.grid(row=1, rowspan=4, column=2, sticky="ew", padx=10, pady=5)

        button1 = Button(self, text="Submit", command=lambda: self.submit(listbox))
        button1.grid(row=5, column=4, sticky="ew", padx=10, pady=10)
        button2 = Button(self, text="Cancel", command=lambda: master.quit())
        button2.grid(row=5, column=1, sticky="ew", padx=10, pady=10)

    def countMaj(self):
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")
        majors = book.sheet_by_index(3)

        # add the majors w/ completed curriculums to a list to be displayed
        majList = []
        for i in range(majors.ncols):
            if majors.cell_value(rowx=1, colx=i) != "":
                majList.append(majors.cell_value(rowx=0, colx=i))
            else:
                pass

        return majList

    def submit(self, listbox):
        # refer to the global cariable major to change it
        global major

        # major = listbox.get(listbox.curselection()) throws an error if no major is chosen
        # display an error message if this occurs
        try:
            # set major to be the chosen major from the listbox
            major = listbox.get(listbox.curselection())
            # switch_frame to ChooseClasses frame
            self.master.switch_frame(ChooseClasses)
        except:
            alert = Messagebox.showerror("Error", "Please select a major.")

class ChooseClasses(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.courses = self.getCourses()

        label1 = Label(self, text="Please Select the Classes You Have Completed", font=("Helvetica", 10))
        label1.grid(row=0, rowspan=1, column=0, columnspan=6, sticky=W)
        label2 = Label(self, text="Note: The only classes listed are those on your chosen major's curriculum.", font=("Helvetica", 8), fg="darkgrey")
        label2.grid(row=1, rowspan=1, column=0, columnspan=6, sticky=W)
        label3 = Label(self, text="All Courses:", font=("Helvetica", 8))
        label3.grid(row=2, rowspan=1, column=0, columnspan=2, padx=5)
        label4 = Label(self, text="Completed Courses:", font=("Helvetica", 8))
        label4.grid(row=2, rowspan=1, column=4, columnspan=2, padx=5)

        # listbox to display all courses in curriculum
        listbox1 = Listbox(self, selectmode=SINGLE)
        for i in self.courses:
            listbox1.insert(END, i)
        listbox1.grid(row=3, rowspan=4, column=0, columnspan=2, padx=2.5, pady=2.5)

        # listbox to hold the completed courses
        listbox2 = Listbox(self, selectmode=SINGLE)
        listbox2.grid(row=3, rowspan=4, column=5, columnspan=2, padx=2.5, pady=2.5)

        button1 = Button(self, text="Submit", command=lambda: self.submit(listbox2))
        button1.grid(row=5, rowspan=1, column=2, columnspan=2, padx=2.5, pady=2.5)
        button2 = Button(self, text="Go Back", command=lambda: master.switch_frame(ChooseMaj))
        button2.grid(row=7, rowspan=2, column=0, columnspan=2, padx=2.5, pady=2.5)
        button3 = Button(self, text=">>>", command=lambda: self.moveCourse(listbox1, listbox2))
        button3.grid(row=3, rowspan=1, column=2, columnspan=1, padx=1.25, pady=2.5)
        button4 = Button(self, text="<<<", command=lambda: self.moveCourse(listbox2, listbox1))
        button4.grid(row=3, rowspan=1, column=3, columnspan=1, padx=1.25, pady=2.5)
        button5 = Button(self, text="Cancel", command=lambda: master.quit())
        button5.grid(row=7, rowspan=2, column=4, columnspan=2, padx=1.25, pady=2.5)

    def getCourses(self):
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")
        majors = book.sheet_by_index(3)

        courses = []
        # find the index of the chosen major
        for i in range(majors.ncols-1):
            if majors.cell_value(rowx=0, colx=i) == major:
                index = i
                break

        # add each course for the given major (cells beneath the chosen major)
        for i in range(1, majors.nrows):
            courses.append(majors.cell_value(rowx=i, colx=index))

        return sorted(courses)

    def moveCourse(self, take_from, give_to):
        temp = take_from.curselection()
        give_to.insert(END, take_from.get(temp))
        take_from.delete(temp)
        self.sortList(take_from)
        self.sortList(give_to)

    def sortList(self, list):
        sortedList = []
        for i in range(list.size()):
            sortedList.append(list.get(i))
        list.delete(0, END)
        for i in sorted(sortedList):
            list.insert(END, i)

    def submit(self, list):
        global taken_classes
        taken_classes = []
        for i in range(list.size()):
            taken_classes.append(list.get(i))
        self.master.switch_frame(OtherPrefs)

class OtherPrefs(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        label1 = Label(self, text="More information.", font=("Helvetica", 10))
        label1.grid(row=0, rowspan=1, column=1, columnspan=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()