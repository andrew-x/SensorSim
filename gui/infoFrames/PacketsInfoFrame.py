__author__ = 'Andrew'
from tkinter import *
from datatypes.Sink import *
from core.Controller import *


class PacketsInfoFrame(Frame):

    master = None
    base = 0
    packets = None

    rows = []
    cols = []

    def __init__(self, master=None, base=0):
        self.master = master
        self.base = base
        super(PacketsInfoFrame, self).__init__(self.master)

        self.init_window()
        self.set_widgets()

    def init_window(self):
        self.master.update_idletasks()

    def set_widgets(self):
        self.packets = Controller.get_packets()

        id_text = Entry(self.master, relief=RIDGE)
        origin_text = Entry(self.master, relief=RIDGE)
        current_text = Entry(self.master, relief=RIDGE)

        id_text.grid(row=self.base, column=0, sticky=NSEW)
        origin_text.grid(row=self.base, column=1, sticky=NSEW)
        current_text.grid(row=self.base, column=2, sticky=NSEW)

        id_text.insert(END, 'ID')
        origin_text.insert(END, 'Origin')
        current_text.insert(END, 'Current')

        id_text.configure(state=DISABLED)
        origin_text.configure(state=DISABLED)
        current_text.configure(state=DISABLED)

        for i in range(len(self.packets)):
            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(self.base+i+1), column=0)
            tmp.insert(END, self.packets[i].get_id())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(self.base+i+1), column=1)
            tmp.insert(END, self.packets[i].get_origin())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(self.base+i+1), column=2)
            tmp.insert(END, self.packets[i].get_current())
            tmp.configure(state=DISABLED)