# module needed to communicate with spreadsheet file
import xlrd, xlwt, CourseClass
# module responsible for gui
from Tkinter import *
# import for the error message
import tkMessageBox as Messagebox

# global variable for the major, classes required for the major, and taken_classes
major = None
major_courses = []
taken_classes = []
major_curriculum = []

# the main class for the app
class App(Tk):

    num_hours = None

    def __init__(self):
        # inherits from the Tkinter library
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(ChooseMaj)

    # this function switches between the different frames of the window
    def switch_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0, sticky="nsew")

    # the app will quit if the user presses the cancel button
    def quit(self):
        # this prompts the user with a question asking if they would like to quit
        answer = str(Messagebox.askquestion("", "Are you sure you want to quit?"))
        # it will quit if the user says "yes"
        if answer == "yes":
            exit(0)

# first page shows the choices for major (currently, CSC and CYEN)
class ChooseMaj(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.majors = self.countMaj()

        # this label asks the user which major they are, either Cyber Engineering or Computer Science
        label = Label(self, text="Please Select Your Major", font=("Helvetica", 10), anchor=CENTER)
        label.grid(row=0, column=1, columnspan=5, sticky="nsew", padx=10, pady=5)

        listbox = Listbox(self, selectmode=SINGLE)
        # add each valid major to the listbox
        for i in self.majors:
            listbox.insert(END, i)
        listbox.grid(row=1, rowspan=4, column=2, sticky="ew", padx=10, pady=5)

        # this asks if the student has a double major, which will change what classes they take
        checkbutton = Checkbutton(self, text="Double Major?", command=lambda: self.update(), state=DISABLED)
        checkbutton.grid(row=5, rowspan=1, column=2, columnspan=2)

        # this button takes the user to the next page
        button1 = Button(self, text="Submit", command=lambda: self.submit(listbox))
        button1.grid(row=6, column=4, sticky="ew", padx=10, pady=10)

        # this button quits the application
        button2 = Button(self, text="Cancel", command=lambda: master.quit())
        button2.grid(row=6, column=1, sticky="ew", padx=10, pady=10)

    # this function accesses the spreadsheet module and use
    def countMaj(self):
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")
        majors = book.sheet_by_index(book.nsheets-1)

        # add the majors w/ completed curriculums to a list to be displayed
        majList = []
        for i in range(majors.ncols):
            # this takes the classes for the majors from the spreadsheet
            if majors.cell_value(rowx=1, colx=i) != "":
                majList.append(majors.cell_value(rowx=0, colx=i))
            # it doesn't do anything with the blank cells from the document
            else:
                pass

        return majList

    # this will be the default message for whenever the user does something that we have not implemented yet
    def update(self):
        update = Messagebox.showinfo("", "I'm sorry, but we have not yet implemented this feature.")

    def submit(self, listbox):
        # refer to the global variable major to change it
        global major, major_courses, taken_classes, major_curriculum

        # reset the lists any previously chosen classes
        major_courses, taken_classes, major_curriculum = [], [], []

        # major = listbox.get(listbox.curselection()) throws an error if no major is chosen
        # display an error message if this occurs
        try:
            # set major to be the chosen major from the listbox
            major = listbox.get(listbox.curselection())
            # switch_frame to ChooseClasses frame
            self.master.switch_frame(ChooseClasses)
        except:
            Messagebox.showerror("Error", "Please select a major.")

# this class displays the page that asks the user to put in the classes they have completed
class ChooseClasses(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        # this label asks user to put in the classes they have done
        label1 = Label(self, text="Please Select the Classes You Have Credit For", font=("Helvetica", 10))
        label1.grid(row=0, rowspan=1, column=0, columnspan=6, sticky=W)
        label2 = Label(self, text="Note: The only classes listed are those on your chosen major's curriculum.", font=("Helvetica", 8), fg="darkgrey")
        label2.grid(row=1, rowspan=1, column=0, columnspan=6, sticky=W)
        label3 = Label(self, text="All Courses:", font=("Helvetica", 8))
        label3.grid(row=2, rowspan=1, column=0, columnspan=2, padx=5)
        label4 = Label(self, text="Completed Courses:", font=("Helvetica", 8))
        label4.grid(row=2, rowspan=1, column=4, columnspan=2, padx=5)

        # listbox to display all courses in curriculum on the left
        listbox1 = Listbox(self, selectmode=SINGLE)
        listbox1.grid(row=3, rowspan=4, column=0, columnspan=2, padx=2.5, pady=2.5)
        # these statements retrieve the possible major courses
        if len(major_courses) > 0:
            pass
        else:
            self.getCourses()
        for i in major_courses:
            listbox1.insert(END, i)

        # listbox to hold the completed courses
        listbox2 = Listbox(self, selectmode=SINGLE)
        listbox2.grid(row=3, rowspan=4, column=5, columnspan=2, padx=2.5, pady=2.5)
        # these statements insert the courses competed into the second listbox
        if len(taken_classes) > 0:
            for i in taken_classes:
                listbox2.insert(END, i)

        # this button removes the selected course from the first listbox and inserts it into the second listbox
        button1 = Button(self, text=">>>", command=lambda: self.addCourse(listbox1, listbox2))
        button1.grid(row=3, rowspan=1, column=2, columnspan=1, padx=1.25, pady=2.5)
        # this button removes the selected course from the second listbox and inserts it back into the first
        button2 = Button(self, text="<<<", command=lambda: self.delCourse(listbox2, listbox1))
        button2.grid(row=3, rowspan=1, column=3, columnspan=1, padx=1.25, pady=2.5)
        # this button submits the selected "taken" classes and continues to the next page
        button3 = Button(self, text="Submit", command=lambda: self.submit(listbox2))
        button3.grid(row=5, rowspan=1, column=2, columnspan=2, padx=2.5, pady=2.5)
        # this button returns to the previous page
        button4 = Button(self, text="Go Back", command=lambda: master.switch_frame(ChooseMaj))
        button4.grid(row=7, rowspan=2, column=0, columnspan=2, padx=2.5, pady=2.5)
        # this button quits the application
        button5 = Button(self, text="Cancel", command=lambda: master.quit())
        button5.grid(row=7, rowspan=2, column=4, columnspan=2, padx=1.25, pady=2.5)

    def getCourses(self):
        global major_courses, major_curriculum
        # accesses the spreadsheet at given directory
        book = xlrd.open_workbook(sys.argv[1], "r")
        majors = book.sheet_by_index(book.nsheets-1)

        major_courses, major_curriculum = [], []
        # find the index of the chosen major
        for i in range(majors.ncols-1):
            if majors.cell_value(rowx=0, colx=i) == major:
                index = i
                break

        # add each course for the given major (cells beneath the chosen major)
        for i in range(1, majors.nrows):
            if (majors.cell_value(rowx=i, colx=index)) != '':
                major_courses.append(majors.cell_value(rowx=i, colx=index))
                major_curriculum.append(majors.cell_value(rowx=i, colx=index))

        major_courses = sorted(major_courses)


    def addCourse(self, take_from, give_to):
        global taken_classes, major_courses
        temp = take_from.curselection()
        taken_classes.append(take_from.get(temp))
        major_courses.remove(take_from.get(temp))
        give_to.insert(END, take_from.get(temp))
        take_from.delete(temp)
        self.sortList(take_from)
        self.sortList(give_to)
        taken_classes, major_courses = sorted(taken_classes), sorted(major_courses)

    def delCourse(self, take_from, give_to):
        global taken_classes, major_courses
        temp = take_from.curselection()
        taken_classes.remove(take_from.get(temp))
        major_courses.append(take_from.get(temp))
        give_to.insert(END, take_from.get(temp))
        take_from.delete(temp)
        self.sortList(take_from)
        self.sortList(give_to)
        taken_classes, major_courses = sorted(taken_classes), sorted(major_courses)

    def sortList(self, list):
        sortedList = []
        for i in range(list.size()):
            sortedList.append(list.get(i))
        list.delete(0, END)
        for i in sorted(sortedList):
            list.insert(END, i)

    def submit(self, listbox):
        global major_curriculum

        if listbox.size() == 0:
            if str(Messagebox.askquestion("", "Did you mean to choose no classes?")) == 'yes':
                pass
            else:
                return

        self.checkCourses()
        for i in taken_classes:
            try:
                major_curriculum.remove(i)
            except:
                pass
        self.master.switch_frame(OtherPrefs)

    def checkCourses(self):
        global taken_classes, major_courses

        for taken in taken_classes:
            for course in CourseClass.all_list:
                if taken == course.id and course.preReq != None:
                    for preReq in course.preReq:
                        if preReq not in taken_classes:
                            answer = Messagebox.askquestion("", "Do you have credit for {}?".format(preReq))
                            if answer == 'no':
                                Messagebox.showinfo("", "Removed {} from taken classes.".format(taken))
                                major_courses.append(preReq)
                                taken_classes.remove(taken)
                                break
                            else:
                                taken_classes.append(preReq)
                                try:
                                    major_courses.remove(preReq)
                                except:
                                    pass

        taken_classes, major_courses = sorted(taken_classes), sorted(major_courses)

class OtherPrefs(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        label1 = Label(self, text="More information.", font=("Helvetica", 10, "bold"))
        label1.grid(row=0, rowspan=1, column=0, columnspan=8, sticky=W)

        sliderVar = IntVar()
        label2 = Label(self, text="How many hours would you like to take per quarter?", font=("Helvetica", 9))
        label2.grid(row=1, rowspan=1, column=0, columnspan=8, sticky=W)
        slider1 = Scale(self, from_=1, to=20, orient=HORIZONTAL, length=300, variable=sliderVar)
        slider1.set(8)
        slider1.grid(row=2, rowspan=1, column=0, columnspan=4, sticky=W)

        summerVar = IntVar()
        label3 = Label(self, text="Will you go to Summer school?", font=("Helvetica", 9))
        label3.grid(row=3, rowspan=1, column=0, columnspan=8, sticky=W)
        radio1 = Radiobutton(self, text="No", variable=summerVar, value=0)
        radio1.grid(row=4, rowspan=1, column=0, columnspan=1, sticky=W)
        radio2 = Radiobutton(self, text="Yes", variable=summerVar, value=1)
        radio2.grid(row=4, rowspan=1, column=1, columnspan=1, sticky=W)

        quarterVar = IntVar()
        label4 = Label(self, text="What will be the next quarter for your classes?", font=("Helvetica", 9))
        label4.grid(row=5, rowspan=1, column=0, columnspan=8, sticky=W)
        radio3 = Radiobutton(self, text="Fall", variable=quarterVar, value=0)
        radio3.grid(row=6, rowspan=1, column=0, columnspan=1, sticky=W)
        radio4 = Radiobutton(self, text="Winter", variable=quarterVar, value=1)
        radio4.grid(row=6, rowspan=1, column=1, columnspan=1, sticky=W)
        radio5 = Radiobutton(self, text="Spring", variable=quarterVar, value=2)
        radio5.grid(row=6, rowspan=1, column=2, columnspan=1, sticky=W)
        radio6 = Radiobutton(self, text="Summer", variable=quarterVar, value=3)
        radio6.grid(row=6, rowspan=1, column=3, columnspan=1, sticky=W)

        button1 = Button(self, text="Submit", command=lambda: self.submit(sliderVar, summerVar))
        button1.grid(row=7, rowspan=1, column=6, columnspan=1, padx=2.5, pady=2.5)
        button2 = Button(self, text="Cancel", command=lambda: master.quit())
        button2.grid(row=7, rowspan=1, column=0, columnspan=1, padx=2.5, pady=2.5, sticky=W)
        button3 = Button(self, text="Go Back", command=lambda: master.switch_frame(ChooseClasses))
        button3.grid(row=7, rowspan=1, column=2, columnspan=1, padx=2.5, pady=2.5)

    def submit(self, slider, summerVar):
        self.master.num_hours = slider.get()
        self.master.switch_frame(ShowSched)

class ShowSched(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        label1 = Label(self, text="Here is a potential schedule:", font=("Helvetica", 10, "bold"))
        label1.grid(row=0, rowspan=1, column=0, columnspan=6, sticky=W)

        self.layoutQuarters()

    def layoutQuarters(self):
        k = 0
        while len(major_courses) > 0:
            broke = False
            i = 0
            list = []
            hours = 0
            while hours < self.master.num_hours:
                for course in major_curriculum:
                    added = False
                    for check in range(len(CourseClass.all_list)):
                        if CourseClass.all_list[check].id == course:
                            test = CourseClass.all_list[check]
                            break
                    if len(taken_classes) > 0:
                        for j in taken_classes:
                            added = False
                            if (test.preReq == None and course not in list and hours+test.hrs <= self.master.num_hours) or (test.preReq == None and test not in list and i > 30 and hours < self.master.num_hours):
                                added = True
                                print "first if"
                                list.append(course)
                                taken_classes.append(course)
                                major_curriculum.remove(course)
                                hours += test.hrs
                                break
                            elif test.preReq != None:
                                if (j in test.preReq and j not in list and hours+test.hrs <= self.master.num_hours) or (test.preReq == None and test not in list and i > 30 and hours < self.master.num_hours):
                                    keep_checking = True
                                    list.append(course)
                                    taken_classes.append(course)
                                    major_curriculum.remove(course)
                                    hours += test.hrs
                                    break
                    if (test.preReq == None and course not in list and hours+test.hrs <= self.master.num_hours) or (test.preReq == None and test not in list and i > 10 and hours < self.master.num_hours):
                        added = True
                        print "first if"
                        list.append(course)
                        taken_classes.append(course)
                        major_curriculum.remove(course)
                        hours += test.hrs
                        break
                    if added:
                        break
                if hours >= self.master.num_hours:
                    break
                if i > 1000:
                    broke = True
                    break
                i += 1
            print hours
            print list

            h = k
            h = Listbox(self)
            h.grid(row=(2+k/4), rowspan=1, column=(k%4)*2, columnspan=1)
            for i in list:
                h.insert(END, i)
            k += 1
            if broke:
                break
        fails = Label(self, text="Classes not added:", font=('Helvetica', 8))
        fails.grid(row=3+k/4, rowspan=1, column=0, columnspan=1)
        failed = Listbox(self)
        for failure in major_curriculum:
            failed.insert(END, failure)
        failed.grid(row=4+k/4, rowspan=1, column=0, columnspan=1)

if __name__ == "__main__":
    app = App()
    app.title("Map-My-Major")
    app.resizable(False, False)
    app.mainloop()
