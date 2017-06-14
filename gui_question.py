from Tkinter import *
import main as mn

class QuestionList(Toplevel):
    def __init__(self, master, index):
	Toplevel.__init__(self)
        self.index = index
        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.resizable(0,0)
        self.geometry("+%d+%d" % (master.winfo_rootx()+50,
                                  master.winfo_rooty()+50)) 
	self.title('Question List')
        self.frame = []
        self.text = []
        self.button = []
        self.shift = 0
        for i,que in enumerate(mn.subjects[index].q):
            self.frame.append(Frame(self))
            self.frame[-1].grid(row=i, column=0)
            b = Button(self.frame[-1], text='X', command=lambda i=i: self.delete(i))
            b.grid(row=0, column=0, sticky=W, pady=4)
            self.button.append(b)
            t = Text(self.frame[-1], wrap=WORD, height=5) # wrap=CHAR, wrap=NONE
            t.grid(row=0, column=1, sticky=N+S+E+W)
            t.insert(END, que.q)
            self.text.append(t)
            s = Scrollbar(self.frame[-1], command=t.yview)
            s.grid(row=0, column=2, sticky='nsew')

        f = Frame(self)
        f.grid(row=len(mn.subjects[index].q), column=0, sticky=W)
        Button(f, text='OK', command=self.ok).grid(row=0, column=0, sticky=W)
        Button(f, text='Cancel', command=self.cancel).grid(row=0, column=1, sticky=W)

    def delete(self, i):
        for i in range(i, len(self.frame)):
            self.button[i].configure(command=lambda i=i: self.delete(i-1))
        self.frame[i-self.shift].destroy()
        del self.frame[i-self.shift]
        del mn.subjects[self.index].q[i-self.shift]
        #self.shift = 1
        if not self.frame:
            self.destroy()

    def ok(self):
        for i,que in enumerate(mn.subjects[self.index].q):
            t = self.text[i].get("1.0", END)
            if t.isspace():
                tkMessageBox.showwarning("Information", "Question is empty.")
                return
            t = t.strip()
            que.q = t
        self.destroy()

    def cancel(self):
        self.destroy()



class Question(Toplevel):
    def __init__(self, master, subject_index):
	Toplevel.__init__(self)
        self.subject_index = subject_index
        self.resizable(0,0)
	self.title('Question')
        self.entry = Text(self, wrap=WORD) # wrap=CHAR, wrap=NONE
        #self.entry = Entry(self)
        self.entry.grid(row=0, column=0)
        #self.protocol('WM_DELETE_WINDOW', self.quit)
	Button(self, text='Add', command=self.add_question).grid(row=1, column=0, sticky=W, pady=4)

    #def quit(self):
        #self.withdraw();

    def add_question(self):
        t = self.entry.get("1.0", END)
        if t.isspace():
            tkMessageBox.showwarning("Information", "There is no question to add.")
            return
        t = t.strip()
        mn.subjects[self.subject_index].add_question(False, t);
        self.destroy()
