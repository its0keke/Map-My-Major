class Course(object):

    def __init__(self, id, hrs, dif):
        self.id = id
        self.hrs = hrs
        self.dif = dif

    def __str__(self):
        return "ID: {}; Hours: {}; Difficulty: {}".format(self.id, self.hrs, self.dif)

csc130 = Course("CSC130", 3, "6/10")
print csc130
