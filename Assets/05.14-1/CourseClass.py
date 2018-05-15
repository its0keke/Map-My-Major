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

def MATH():
    # access the sheet
    MATH_sh = book.sheet_by_index(0)
    MATH_list = []

    for num in range(1, MATH_sh.nrows):
        num = Course(MATH_sh, num)
        MATH_list.append(num)

    return MATH_list

def CSCCYEN():
    # access the sheet
    CSCCYEN_sh = book.sheet_by_index(1)
    CSCCYEN_list = []

    for num in range(1, CSCCYEN_sh.nrows):
        num = Course(CSCCYEN_sh, num)
        CSCCYEN_list.append(num)

    return CSCCYEN_list

def ENGR():
    # access the sheet
    ENGR_sh = book.sheet_by_index(2)
    ENGR_list = []

    for num in range(1, ENGR_sh.nrows):
        num = Course(ENGR_sh, num)
        ENGR_list.append(num)

    return ENGR_list

def PHYSSCI():
    PHYSSCI_sh = book.sheet_by_index(3)
    PHYSSCI_list = []

    for num in range(1, PHYSSCI_sh.nrows):
        num = Course(PHYSSCI_sh, num)
        PHYSSCI_list.append(num)

    return PHYSSCI_list

def ENGLCOMM():
    ENGLCOMM_sh = book.sheet_by_index(4)
    ENGLCOMM_list = []

    for num in range(1, ENGLCOMM_sh.nrows):
        num = Course(ENGLCOMM_sh, num)
        ENGLCOMM_list.append(num)

    return ENGLCOMM_list

# accesses the spreadsheet at given directory
book = xlrd.open_workbook(sys.argv[1], "r")

def combineLists():
    all_list = []

    MATH_list = MATH()
    CSCCYEN_list = CSCCYEN()
    ENGR_list = ENGR()
    PHYSSCI_list = PHYSSCI()
    ENGLCOMM_list = ENGLCOMM()

    for i in MATH_list:
        all_list.append(i)
    for i in CSCCYEN_list:
        all_list.append(i)
    for i in ENGR_list:
        all_list.append(i)
    for i in PHYSSCI_list:
        all_list.append(i)
    for i in ENGLCOMM_list:
        all_list.append(i)

    return all_list

all_list = combineLists()
