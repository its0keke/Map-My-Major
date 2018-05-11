import xlrd, xlwt, sys

class Major(object):
    def __init__(self, college, hrs, course_list):
        self.college = college
        self.hrs = hrs
        self.course_list = course_list

class Course(object):
    def __init__(self, id, hrs, coReq, preReq):
        self.id = id
        self.hrs = hrs
        self.preReq = preReq
        self.coReq = coReq

    def __str__(self):
        return "Course: {}; \tHours: {}; \tCoReqs: {}; \tPreReqs: {};".format(self.id, self.hrs, self.coReq, self.preReq)

def getCoReqs(sh, i):
    coReqs = []
    cell = sh.cell_value(rowx=i, colx=2)
    try:
        coReqs.append(cell.split(", "))
    except:
        return None
    return coReqs

def getPreReqs(sh, i):
    preReqs = []
    cell = sh.cell_value(rowx=i, colx=3)
    try:
        preReqs.append(cell.split(", "))
    except:
        return None
    return preReqs


def create_list(sh, nrows):
    # create a list to store the course
    list = []

    for i in range(1, nrows-1):
        id = sh.cell_value(rowx=i, colx=0)
        hrs = sh.cell_value(rowx=i, colx=1)
        coReq = getCoReqs(sh, i)
        preReq = getPreReqs(sh, i)

        list.append(Course(id, hrs, coReq, preReq))

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
book = xlrd.open_workbook(sys.argv[1], "r")

CSC_list = CSC()
list_courses(CSC_list)
# MATH_list = MATH()
# list_courses(MATH_list)
