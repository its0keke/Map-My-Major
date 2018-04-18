# you have to install these modules to manipulate spreadsheet files
import xlrd, xlwt

class Major(object):
    def __init__(self, college, hrs, course_list):
        self.college = college
        self.hrs = hrs
        self.course_list = course_list

class Course(object):
    def __init__(self, id, hrs, diff):
        self.id = id
        self.hrs = hrs
        self.diff = diff

    def __str__(self):
        return "Course: {}; Hours: {}; Difficulty {};".format(self.id, self.hrs, self.diff)

def create_list(sh, nrows):
    # create a list to store the course
    list = [0]*nrows

    for i in range(nrows):
        id = sh.cell_value(rowx=i, colx=0)
        hrs = sh.cell_value(rowx=i, colx=1)
        diff = sh.cell_value(rowx=i, colx=2)

        list[i] = Course(id, hrs, diff)

    return list

def CSC():
    # access the sheet
    CSC_sh = book.sheet_by_index(0)
    # variable to store the number of rows
    nrows = CSC_sh.nrows

    return create_list(CSC_sh, nrows)

def MATH():
    # access the sheet
    MATH_sh = book.sheet_by_index(1)
    # variable to store the number of rows
    nrows = MATH_sh.nrows

    return create_list(MATH_sh, nrows)

def list_courses(list):
    for i in range(len(list)):
        print list[i]

# accesses the spreadsheet at given directory
book = xlrd.open_workbook("Courses.xlsx")

CSC_list = CSC()
list_courses(CSC_list)
MATH_list = MATH()
list_courses(MATH_list)
