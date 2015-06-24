__author__ = 'Andrew'

from tkinter import *
from datatypes.Sink import *
from core.Controller import *
from gui.MainFrame import *


class SinkEditFrame(Frame):

    master = None

    sink = None

    id_edit = None
    x_edit = None
    y_edit = None

    cols = []

    submit_button = None

    def __init__(self, master=None):
        super(SinkEditFrame, self).__init__(master)

        self.master = master

        self.sink = Controller.get_sink()

        self.init_window()
        self.set_widgets()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        self.master.update_idletasks()

        self.master.title('Sink Information')

    def exit(self):
        self.master.destroy()

    def set_widgets(self):
        self.sink = Controller.get_sink()

        id_text = Entry(self.master, relief=RIDGE)
        x_text = Entry(self.master, relief=RIDGE)
        y_text = Entry(self.master, relief=RIDGE)

        id_text.grid(row=0, column=0, sticky=NSEW)
        x_text.grid(row=0, column=1, sticky=NSEW)
        y_text.grid(row=0, column=2, sticky=NSEW)

        id_text.insert(END, 'ID')
        x_text.insert(END, 'X')
        y_text.insert(END, 'Y')

        id_text.configure(state=DISABLED)
        x_text.configure(state=DISABLED)
        y_text.configure(state=DISABLED)

        self.id_edit = Entry(self.master, relief=RIDGE)
        self.id_edit .grid(row=1, column=0)
        self.id_edit .insert(END, self.sink.get_id())

        self.x_edit = Entry(self.master, relief=RIDGE)
        self.x_edit.grid(row=1, column=1)
        self.x_edit.insert(END, self.sink.get_x())

        self.y_edit = Entry(self.master, relief=RIDGE)
        self.y_edit.grid(row=1, column=2)
        self.y_edit.insert(END, self.sink.get_y())

        submit_button = Button(self.master, text='Submit', command=self.submit)
        submit_button.grid(row=3, column=1, pady=10)

    def submit(self):
        e = Sink(self.id_edit.get(), self.x_edit.get(), self.y_edit.get())
        Controller.set_sink(e)

        self.exit()
