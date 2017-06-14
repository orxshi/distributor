from Tkinter import *
import ttk
import main as mn
import tkSimpleDialog

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
        self.aMenu.add_command(label="Edit student name", command=self.edit_student_name)
        self.aMenu.add_command(label="Edit excluded subject", command=self.edit_exc)
        self.aMenu.add_command(label="Delete", command=self.delete)

    def edit_student_name(self):
        item = self.tree.selection()[0]
        name = self.tree.item(item, "values")[0]
        exc = self.tree.item(item, "values")[1]
        name = tkSimpleDialog.askstring("Edit student name", "Name:", parent=self, initialvalue=name)
        if name:
            name = name.strip()
            mn.students[self.tree.index(item)].edit_name(name)
            self.tree.item(item, values=(name, exc))

    def edit_exc(self):
        item = self.tree.selection()[0]
        name = self.tree.item(item, "values")[0]
        exc = self.tree.item(item, "values")[1]
        exc = tkSimpleDialog.askstring("Edit excluded subject", "Subject:", parent=self, initialvalue=exc)
        if exc:
            exc = exc.strip()
            mn.students[self.tree.index(item)].edit_exc(exc)
            self.tree.item(item, values=(name, exc))

    def type(self, event):
        event.widget.config(fg='black')
        if event.keysym == 'Return':
            if len(event.widget.get()) != 0:
                self.add_student()

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


    def on_entry_unclick_ne(self, event):
        if event.widget.get() == "Name" or event.widget.get() == "Excluded subject" or len(event.widget.get()) == 0:
            event.widget.delete(0, "end")
            event.widget.insert(END, "Name")
            event.widget.config(fg='gray')
        else:
            event.widget.config(fg='black')

    def on_entry_unclick_ee(self, event):
        if event.widget.get() == "Name" or event.widget.get() == "Excluded subject" or len(event.widget.get()) == 0:
            event.widget.delete(0, "end")
            event.widget.insert(END, "Excluded subject")
            event.widget.config(fg='gray')
        else:
            event.widget.config(fg='black')

    def quit(self):
        self.withdraw();

    def add_student(self):
        if self.name_entry.get() == "Name":
            tkMessageBox.showerror("Error", "Student name must be given")
            return
        excsub = self.exc_entry.get()
        if self.exc_entry.get() == "Excluded subject":
            excsub = ""
        self.tree.insert("", len(mn.students), text=self.name_entry.get(), values=(self.name_entry.get(), excsub))
        mn.students.append(mn.Student(name=self.name_entry.get(), exc=excsub))
        self.name_entry.delete(0, "end")
        #self.name_entry.config(fg='gray')
        self.exc_entry.delete(0, "end")
        self.exc_entry.config(fg='gray')
        #self.name_entry.insert(END, "Name")
        self.exc_entry.insert(END, "Excluded subject")
        #self.tree.focus_set()
        self.name_entry.focus_set()

    def delete(self):
        selected_item = self.tree.selection()[0]
        del mn.students[self.tree.index(selected_item)]
        self.tree.delete(selected_item)

    def delete_all(self):
        del mn.students[:]
        self.tree.delete(*self.tree.get_children())

    def popup(self, event):
        item = self.tree.identify("item", event.x, event.y)
        if item:
            self.aMenu.tk_popup(event.x_root, event.y_root)
