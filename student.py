class Student:
    def __init__(self, exc=None, name=None):
        self.q = list()
        self.t = list()
        self.exc = exc
        self.name = name

def add_mul_students(students, count, *arg):
    if len(arg) == 1:
        for i in range(0,count):
            students.append(Student(exc=arg[0]))
        return
    for i in range(0,len(arg)):
        students.append(Student(exc=arg[i]))
