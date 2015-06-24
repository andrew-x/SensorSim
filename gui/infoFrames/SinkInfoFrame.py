__author__ = 'Andrew'

from tkinter import *
from datatypes.Sink import *
from core.Controller import *
from gui.MainFrame import *


class SinkInfoFrame(Frame):

    master = None

    sink = None

    id_view= None
    x_view = None
    y_view = None

    cols = []

    submit_button = None

    def __init__(self):
        self.master = Tk()
        super(SinkInfoFrame, self).__init__(self.master)

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

        self.id_view = Entry(self.master, relief=RIDGE)
        self.id_view.grid(row=1, column=0)
        self.id_view.insert(END, self.sink.get_id())
        self.id_view.configure(state=DISABLED)

        self.x_view = Entry(self.master, relief=RIDGE)
        self.x_view.grid(row=1, column=1)
        self.x_view.insert(END, self.sink.get_x())
        self.x_view.configure(state=DISABLED)

        self.y_view = Entry(self.master, relief=RIDGE)
        self.y_view.grid(row=1, column=2)
        self.y_view.insert(END, self.sink.get_y())
        self.y_view.configure(state=DISABLED)