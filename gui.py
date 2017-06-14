import main as mn
import tkMessageBox
import subprocess
import os as os
from gui_subject import *
from gui_status_bar import *
import tkFileDialog

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
        filemenu.add_command(label="New", command=self.new)
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
	    #os.system('rm *.tex *.log *.aux')
	    os.system('evince jav.pdf')
	elif os.name == 'nt':
	    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'jav.tex']
	    proc = subprocess.Popen(cmd)
	    proc.communicate()
	    os.system('del *.tex *.log *.aux')
	    os.system('explorer.exe "jav.pdf"')
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

    def new(self):
        self.subject_window.delete_all()
        self.student_window.delete_all()
        self.saveasdialog = None
        self.filename = ""
        self.status.set("New file opened")
        self.after(3000, self.status.clear())



app = MainWindow()
app.mainloop()
