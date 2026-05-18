class person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
    
    def printname(self):
        print(self.fname, self.lname)

x = person("Alwin", "C B")
x.printname()

class student(person):
    pass

x = student("Adil", "Joby")
x.printname()