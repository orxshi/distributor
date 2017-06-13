from gui_question import *
from gui_student import *

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
        event.widget.config(fg='black')
        if event.keysym == 'Return':
            if len(event.widget.get()) != 0:
                self.add_subject()

    #def type(self, event):
        #self.entry.config(fg='black')

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
