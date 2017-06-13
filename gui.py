from Tkinter import *
import ttk
import main as mn
import tkSimpleDialog
import tkMessageBox
import subprocess
import tkFileDialog
import os as os

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


#class Student(Toplevel):
class Student(LabelFrame):
    name_entry = None
    exc_entry = None
    def __init__(self, master):
	#Toplevel.__init__(self)
	LabelFrame.__init__(self, master, text="Student")
	#self.title('Student')
        #self.resizable(0,0)
        self.upperframe = Frame(self, pady=0)
        self.upperframe.grid(row=0, column=0)
        self.name_entry = Entry(self.upperframe, name="nameentry")
        self.name_entry.grid(row=0, column=0)
        #self.name_entry.bind('<FocusIn>', lambda event, n=self.name_entry: self.on_entry_click(event, n))
        #self.name_entry.bind('<FocusOut>', lambda event, n=self.name_entry: self.on_entry_unclick(event, n))
        #self.name_entry.bind("<Key>", lambda event, n=self.name_entry: self.type(event, n))
        self.name_entry.bind('<FocusIn>', self.on_entry_click)
        self.name_entry.bind('<FocusOut>', self.on_entry_unclick_ne)
        self.name_entry.bind("<Key>", self.type)
        self.name_entry.config(fg='gray')
        self.name_entry.insert(END, "Name")
        self.exc_entry = Entry(self.upperframe, name="excentry")
        self.exc_entry.grid(row=0, column=1)
        #self.exc_entry.bind('<FocusIn>', lambda event, n=self.exc_entry: self.on_entry_click(event, n))
        #self.exc_entry.bind('<FocusOut>', lambda event, n=self.exc_entry: self.on_entry_unclick(event, n))
        #self.exc_entry.bind("<Key>", lambda event, n=self.exc_entry: self.type(event, n))
        self.exc_entry.bind('<FocusIn>', self.on_entry_click)
        self.exc_entry.bind('<FocusOut>', self.on_entry_unclick_ee)
        self.exc_entry.bind("<Key>", self.type)
        self.exc_entry.config(fg='gray')
        self.exc_entry.insert(END, "Excluded subject")
        #self.protocol('WM_DELETE_WINDOW', self.quit)
	Button(self.upperframe, text='Add', command=self.add_student).grid(row=0, column=2, sticky=W, pady=10)
	#Button(self, text='Delete', command=self.delete).grid(row=1, column=1, sticky=W, pady=4)
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree["columns"]=("name", "exc")
        self.tree.heading("name", text="Name")
        self.tree.heading("exc", text="Excluded subject")
        self.tree.grid(row=1, column=0)
        self.tree.bind("<Button-3>", self.popup)
	#Button(self, text='Close', command=self.withdraw).grid(row=3, column=0, sticky=W, pady=4)

        self.aMenu = Menu(self, tearoff=0)
        self.aMenu.add_command(label="Delete", command=self.delete)

    def type(self, event):
        event.widget.config(fg='black')

    #def on_entry_click(self, event, entry):
    def on_entry_click(self, event):
        #if entry.get() == "Name" or entry.get() == "Excluded subject":
        if event.widget.get() == "Name" or event.widget.get() == "Excluded subject":
        #if (entry.name() == "nameentry" and entry.get() == "Name") or (entry.name() == "excentry" and entry.get() == "Excluded subject"):
        #if entry.get() == "Name":
        #if self.firstclick: # if this is the first time they clicked it
            #self.firstclick = False
            event.widget.delete(0, "end") # delete all the text in the entry
            event.widget.config(fg='gray')
        else:
            event.widget.config(fg='black')


    #def on_entry_unclick(self, event, entry):
    def on_entry_unclick_ne(self, event):
        if len(event.widget.get()) == 0:
            event.widget.insert(END, "Name")
            event.widget.config(fg='gray')
        else:
            event.widget.config(fg='black')

    def on_entry_unclick_ee(self, event):
        if len(event.widget.get()) == 0:
            event.widget.insert(END, "Excluded subject")
            event.widget.config(fg='gray')
        else:
            event.widget.config(fg='black')

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


#class Subject(Toplevel):
class Subject(LabelFrame):
    nsubject = 3
    entry = None
    subject = [None] * nsubject
    question_button = None
    list_size = 0

    def __init__(self, master):
	#Toplevel.__init__(self)
	LabelFrame.__init__(self, master, text="Subject")
	#self.title('Subject')
        #self.resizable(0,0)
        self.upperframe = Frame(self, pady=0)
        self.upperframe.grid(row=0, column=0)
        #Label(self.upperframe, text="Subject: ").grid(row=0, column=0)
        #self.protocol('WM_DELETE_WINDOW', self.quit)

        self.entry = Entry(self.upperframe)
        self.entry.insert(END, "Subject")
        self.entry.grid(row=0, column=0)
        self.entry.bind('<FocusIn>', self.on_entry_click)
        self.entry.bind('<FocusOut>', self.on_entry_unclick)
        self.entry.bind("<Key>", self.type)
        self.entry.config(fg='gray')
        self.question_button = Button(self.upperframe, text='Add', command=self.add_subject)
        self.question_button.grid(row=0, column=1, sticky=W, pady=10)

	#Button(self, text='Close', command=self.withdraw).grid(row=2, column=0, sticky=W, pady=4)

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

    def type(self, event):
        self.entry.config(fg='black')

    def on_entry_click(self, event):
        if self.entry.get() == "Subject":
        #if self.firstclick: # if this is the first time they clicked it
            #self.firstclick = False
            self.entry.delete(0, "end") # delete all the text in the entry
            self.entry.config(fg='gray')
        else:
            self.entry.config(fg='black')

    def on_entry_unclick(self, event):
        if len(self.entry.get()) == 0:
            self.entry.insert(END, "Subject")
            self.entry.config(fg='gray')
        else:
            self.entry.config(fg='black')

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
        ql.grab_set()
        ql.wait_window()
        first_val = self.tree.item(item, "values")[0]
        self.tree.item(item, values=(first_val, len(mn.subjects[self.tree.index(item)].q)))

    def add_subject(self):
        mn.add_subject(mn.subjects, self.entry.get())
        #self.existing_subjects.insert(END, self.entry.get())
        self.tree.insert("", len(mn.subjects), text='', values=(self.entry.get(), 0))
        self.list_size = self.list_size + 1
        self.entry.delete(0, "end") # delete all the text in the entry
        self.entry.config(fg='gray')

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


class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


class MainWindow(Tk):
    subject_window = None
    student_window = None
    saveasdialog = None
    filename = ""

    def __init__(self):
	Tk.__init__(self)
	self.title('Distributor')
        self.resizable(0,0)
        w = 900 # width for the Tk root
        h = 345 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #self.geometry("900x500")
        #self.fr_menu = Frame(self)
        #self.fr_menu.grid(row=0, column=0)
        #self.menubar = Menu(self.fr_menu)
        #self.fr_subject = Frame(self)
        #self.fr_student = Frame(self)
        #self.fr_subject.grid(row=0, column=0)
        #self.fr_student.grid(row=0, column=1)

        self.subject_window = Subject(self)
        self.subject_window.grid(row=0, column=0, padx=(30,15), pady=(20,20))

        self.student_window = Student(self)
        self.student_window.grid(row=0, column=1, padx=(15,30), pady=(20,20))

        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save as", command=self.saveas)
        filemenu.add_command(label="Load", command=self.load)
        filemenu.add_command(label="Generate", command=self.generate)
        filemenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        #windowmenu = Menu(self.menubar, tearoff=0)
        #windowmenu.add_command(label="Subject", command=self.open_subject_window)
        #windowmenu.add_command(label="Student", command=self.open_student_window)
        #self.menubar.add_cascade(label="Window", menu=windowmenu)
        self.config(menu=self.menubar)
        self.status = StatusBar(self)
        self.status.grid(row=1, column=0, columnspan=2, sticky=W+E)
        #self.status.pack(side=BOTTOM, fill=X)

    def generate(self):
        mn.distribute()
        mn.generate_latex()
	if os.name == 'posix':
	    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'jav.tex']
	    proc = subprocess.Popen(cmd)
	    proc.communicate()
	    #cmd = ['rm *.tex *.log *.aux']
	    #proc = subprocess.Popen(cmd)
	    os.system('rm *.tex *.log *.aux')
	    os.system('evince jav.pdf')
	    self.status.set("Generated jav.pdf successfully")

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
        ftypes = [('Data files', '*.dat'), ('All files', '*')]
        self.filename = tkFileDialog.askopenfilename(filetypes=ftypes, defaultextension=".dat")
        if not self.filename:
            return
        del mn.subjects[:]
        del mn.students[:]
        f = open(self.filename, "r+")
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
        f.close()
        #
        #self.open_subject_window()
        self.subject_window.tree.delete(*self.subject_window.tree.get_children())
        for sub in mn.subjects:
            self.subject_window.tree.insert("", 'end', text='', values=(sub.name, len(sub.q)))
        #self.open_student_window()
        self.student_window.tree.delete(*self.student_window.tree.get_children())
        for stu in mn.students:
            self.student_window.tree.insert("", 'end', text='', values=(stu.name, stu.exc))
        self.status.set("Loaded " + os.path.basename(os.path.normpath(self.filename)))

    def write(self, f):
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
        f.close()

    def saveas(self):
        ftypes = [('Data files', '*.dat'), ('All files', '*')]
        self.filename = tkFileDialog.asksaveasfilename(filetypes=ftypes, defaultextension=".dat")
        if not self.filename:
            return
        dirname = os.path.dirname(self.filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(self.filename, "w+")
        self.write(f)
        self.status.set("Saved as " + os.path.basename(os.path.normpath(self.filename)))

    def save(self):
        if not self.filename:
            self.saveas()
        else:
            f = open(self.filename, "w+")
            f.seek(0)
            f.truncate()
            self.write(f)
        self.status.set("Saved to " + os.path.basename(os.path.normpath(self.filename)))


app = MainWindow()
app.mainloop()
