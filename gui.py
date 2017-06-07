from Tkinter import *
import ttk
import main as mn
import tkSimpleDialog
import tkMessageBox
import subprocess

class QuestionList(Toplevel):
    def __init__(self, master, index):
	Toplevel.__init__(self)
        self.index = index
        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.resizable(0,0)
	self.title('Question List')
        self.frame = []
        self.text = []
        self.shift = 0
        for i,que in enumerate(mn.subjects[index].q):
            self.frame.append(Frame(self))
            self.frame[-1].grid(row=i, column=0)
            b = Button(self.frame[-1], text='X', command=lambda i=i: self.delete(i))
            b.grid(row=0, column=0, sticky=W, pady=4)
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
        self.frame[i-self.shift].destroy()
        del self.frame[i-self.shift]
        del mn.subjects[self.index].q[i-self.shift]
        self.shift = 1
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


class Student(Toplevel):
    name_entry = None
    exc_entry = None
    def __init__(self, master):
	Toplevel.__init__(self)
	self.title('Student')
        self.resizable(0,0)
        self.upperframe = Frame(self, pady=10)
        self.upperframe.grid(row=1, column=0)
        self.name_entry = Entry(self.upperframe)
        self.name_entry.grid(row=1, column=0)
        self.exc_entry = Entry(self.upperframe)
        self.exc_entry.grid(row=1, column=1)
        Label(self.upperframe, text="Name").grid(row=0, column=0)
        Label(self.upperframe, text="Excluded subject").grid(row=0, column=1)
        self.protocol('WM_DELETE_WINDOW', self.quit)
	Button(self.upperframe, text='Add', command=self.add_student).grid(row=1, column=2, sticky=W, pady=4)
	#Button(self, text='Delete', command=self.delete).grid(row=1, column=1, sticky=W, pady=4)
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree["columns"]=("name", "exc")
        self.tree.heading("name", text="Name")
        self.tree.heading("exc", text="Excluded subject")
        self.tree.grid(row=2, column=0)
        self.tree.bind("<Button-3>", self.popup)
	Button(self, text='Close', command=self.withdraw).grid(row=3, column=0, sticky=W, pady=4)

        self.aMenu = Menu(self, tearoff=0)
        self.aMenu.add_command(label="Delete", command=self.delete)

    def quit(self):
        self.withdraw();

    def add_student(self):
        self.tree.insert("", len(mn.students), text=self.name_entry.get(), values=(self.name_entry.get(), self.exc_entry.get()))
        mn.students.append(mn.Student(name=self.name_entry.get(), exc=self.exc_entry.get()))

    def delete(self):
        selected_item = self.tree.selection()[0]
        del mn.students[self.tree.index(selected_item)]
        self.tree.delete(selected_item)

    def popup(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            self.aMenu.tk_popup(event.x_root, event.y_root)


class Subject(Toplevel):
    nsubject = 3
    entry = None
    subject = [None] * nsubject
    question_button = None
    list_size = 0

    def __init__(self, master):
	Toplevel.__init__(self)
	self.title('Subject')
        self.resizable(0,0)
        self.upperframe = Frame(self, pady=10)
        self.upperframe.grid(row=0, column=0)
        Label(self.upperframe, text="Subject: ").grid(row=0, column=0)
        self.protocol('WM_DELETE_WINDOW', self.quit)

        self.entry = Entry(self.upperframe)
        self.entry.grid(row=0, column=1)
        self.question_button = Button(self.upperframe, text='Add', command=self.add_subject)
        self.question_button.grid(row=0, column=2)

	Button(self, text='Close', command=self.withdraw).grid(row=2, column=0, sticky=W, pady=4)

        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree["columns"]=("sub", "nq")
        self.tree.heading("sub", text="Subject")
        self.tree.heading("nq", text="# of questions")
        self.tree.grid(row=1, column=0)
        #self.existing_subjects = Listbox(self, selectmode=SINGLE)
        #self.existing_subjects.grid(row=self.nsubject+2, column=0)
        self.tree.bind("<Button-3>", self.popup)

        self.aMenu = Menu(self, tearoff=0)
        self.aMenu.add_command(label="Edit subject name", command=self.edit_subject_name)
        self.aMenu.add_command(label="Remove subject", command=self.remove_subject)
        self.aMenu.add_command(label="Add question", command=self.add_question)
        self.aMenu.add_command(label="See questions", command=self.see_questions)

    def edit_subject_name(self):
        item = self.tree.selection()[0]
        name = self.tree.item(item, "values")[0]

        name = tkSimpleDialog.askstring("Edit subject name", "Subject:", parent=self, initialvalue=name)
        if name:
            name = name.strip()
            mn.subjects[self.tree.index(item)].name = name
            second_val = self.tree.item(item, "values")[1]
            self.tree.item(item, values=(name, second_val))


    def popup(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            self.aMenu.tk_popup(event.x_root, event.y_root)

    def see_questions(self):
        item = self.tree.selection()[0]
        if len(mn.subjects[self.tree.index(item)].q) == 0:
            tkMessageBox.showinfo("Information", "There is no question in this subject")
            return
        ql = QuestionList(self, self.tree.index(item))
        ql.wait_window()
        first_val = self.tree.item(item, "values")[0]
        self.tree.item(item, values=(first_val, len(mn.subjects[self.tree.index(item)].q)))

    def add_subject(self):
        mn.add_subject(mn.subjects, self.entry.get())
        #self.existing_subjects.insert(END, self.entry.get())
        self.tree.insert("", len(mn.subjects), text='', values=(self.entry.get(), 0))
        self.list_size = self.list_size + 1

    def remove_subject(self):
        #index = self.existing_subjects.curselection()
        #del mn.subjects[index[0]]
        #self.existing_subjects.delete(ANCHOR)
        selected_item = self.tree.selection()[0]
        del mn.subjects[self.tree.index(selected_item)]
        self.tree.delete(selected_item)

    def add_question(self):
        #index = self.existing_subjects.curselection()
        selected_item = self.tree.selection()[0]
        self.question_window = Question(self, self.tree.index(selected_item))
        self.question_window.wait_window()
        item = self.tree.selection()[0]
        #item(values=(item.values[0], len(mn.subjects[self.tree.index(selected_item)].q)))
        first_val = self.tree.item(item, "values")[0]
        self.tree.item(item, values=(first_val, len(mn.subjects[self.tree.index(selected_item)].q)))

    def quit(self):
        self.withdraw();


class MainWindow(Tk):
    subject_window = None
    student_window = None

    def __init__(self):
	Tk.__init__(self)
	self.title('Main')
        self.resizable(0,0)
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Load", command=self.load)
        filemenu.add_command(label="Generate", command=self.generate)
        filemenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        windowmenu = Menu(self.menubar, tearoff=0)
        windowmenu.add_command(label="Subject", command=self.open_subject_window)
        windowmenu.add_command(label="Student", command=self.open_student_window)
        self.menubar.add_cascade(label="Window", menu=windowmenu)
        self.config(menu=self.menubar)

    def generate(self):
        mn.distribute()
        mn.generate_latex()
        cmd = ['pdflatex', '-interaction', 'nonstopmode', 'jav.tex']
        proc = subprocess.Popen(cmd)
        proc.communicate()

    def open_subject_window(self):
        if self.subject_window is None:
            self.subject_window = Subject(self)
        else:
            self.subject_window.deiconify()

    def open_student_window(self):
        if self.student_window is None:
            self.student_window = Student(self)
        else:
            self.student_window.deiconify()

    def load(self):
        del mn.subjects[:]
        del mn.students[:]
        f = open('save.dat', 'r')
        size = int(f.readline().strip())
        for i in range(size):
            name = f.readline().strip()
            exc = f.readline().strip()
            mn.students.append(mn.Student(name=name, exc=exc))
        size = int(f.readline().strip())
        for i in range(size):
            name = f.readline().strip()
            mn.subjects.append(mn.Subject(name=name))
            size = int(f.readline().strip())
            for i in range(size):
                q = f.readline().strip()
                s = f.readline().strip()
                mn.subjects[-1].q.append(mn.Question(q=q, s=s))
        #
        self.open_subject_window()
        self.subject_window.tree.delete(*self.subject_window.tree.get_children())
        for sub in mn.subjects:
            self.subject_window.tree.insert("", 'end', text='', values=(sub.name, len(sub.q)))
        self.open_student_window()
        self.student_window.tree.delete(*self.student_window.tree.get_children())
        for stu in mn.students:
            self.student_window.tree.insert("", 'end', text='', values=(stu.name, stu.exc))


    def save(self):
        f = open('save.dat', 'w')
        f.write(str(len(mn.students))+"\n")
        for stu in mn.students:
            f.write(stu.name+"\n")
            f.write(stu.exc+"\n")
        f.write(str(len(mn.subjects))+"\n")
        for sub in mn.subjects:
            f.write(sub.name+"\n")
            f.write(str(len(sub.q))+"\n")
            for que in sub.q:
                f.write(que.q+"\n")
                f.write(que.s+"\n")


app = MainWindow()
app.mainloop()
