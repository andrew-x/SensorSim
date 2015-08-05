__author__ = 'Andrew'

from tkinter import *
from datatypes.Sink import *
from core.Controller import *
from gui.MainFrame import *


class SinkInfoFrame(Frame):

    master = None

    sinks = None

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
        self.sinks = Inventory.SINKS

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

        for i in range(len(self.sinks)):
            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=0)
            tmp.insert(END, self.sinks[i].get_id())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=1)
            tmp.insert(END, self.sinks[i].get_x())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=2)
            tmp.insert(END, self.sinks[i].get_y())
            tmp.configure(state=DISABLED)