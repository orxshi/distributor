class Question:
    def __init__(self, s=None, mulChoice=False, q=None):
        self.s = s
        self.f = 0
        self.mulChoice = mulChoice
        self.q = q

class Subject:
    def __init__(self, name=None):
        self.f = 0
        self.q = list()
        self.name = name

    def add_question(self, mulChoice, que=None):
        #self.q.append(Question(q=que, s='{\\' + str(self.name) + chr(len(self.q) + ord('a')) + '}', mulChoice=mulChoice))
        self.q.append(Question(q=que, s='\\' + str(self.name) + chr(len(self.q) + ord('a')), mulChoice=mulChoice))

    def addmulq(self, *arg):
        for i in range(0,len(arg)):
            self.q.append(Question(s='{\\' + str(self.name) + chr(len(self.q) + ord('a')) + '}', mulChoice=arg[i]))

def add_subject(subjects, *arg):
    for i in range(0, len(arg)):
        subjects.append(Subject(name=arg[i]))
