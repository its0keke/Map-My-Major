import xlrd, xlwt, sys

class Course(object):
    def __init__(self, sheet, num):
        self.id = sheet.cell_value(rowx=num, colx=0)
        self.hrs = sheet.cell_value(rowx=num, colx=1)
        self.coReq = self.getCoReqs(sheet, num)
        self.preReq = self.getPreReqs(sheet, num)

    def getCoReqs(self, sh, i):
        coReqs = None
        cell = sh.cell_value(rowx=i, colx=2)

        if (cell != ''):
            coReqs = cell.split(", ")
        else:
            coReqs = None

        return coReqs

    def getPreReqs(self, sh, i):
        preReqs = None
        cell = sh.cell_value(rowx=i, colx=3)

        if cell != '':
            preReqs = cell.split(", ")
        else:
            preReqs = None

        return preReqs

    def __str__(self):
        return "Course: {}; \tHours: {}; \tCoReqs: {}; \tPreReqs: {};".format(self.id, self.hrs, self.coReq, self.preReq)

def CSCCYEN():
    # access the sheet
    CSCCYEN_sh = book.sheet_by_index(1)

    for num in range(1, CSCCYEN_sh.nrows):
        num = Course(CSCCYEN_sh, num)
        print num

def MATH():
    # access the sheet
    MATH_sh = book.sheet_by_index(0)

    for num in range(1, MATH_sh.nrows):
        num = Course(MATH_sh, num)
        print num

# accesses the spreadsheet at given directory
book = xlrd.open_workbook(sys.argv[1], "r")

CSCCYEN()
MATH()
