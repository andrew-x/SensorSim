__author__ = 'Andrew'

from tkinter import *
from core.Controller import *


class EnergizersInfoFrame(Frame):

    master = None
    energizers = None

    def __init__(self):
        self.master = Tk()
        super(EnergizersInfoFrame, self).__init__(self.master)

        self.init_window()
        self.set_widgets()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.update_idletasks()
        self.master.title('Energizers Information')

    def exit(self):
        self.master.destroy()

    def set_widgets(self):
        self.energizers = Inventory.ENERGIZERS

        id_text = Entry(self.master, relief=RIDGE)
        x_text = Entry(self.master, relief=RIDGE)
        y_text = Entry(self.master, relief=RIDGE)
        range_text = Entry(self.master, relief=RIDGE)
        battery_text = Entry(self.master, relief=RIDGE)
        rate_text = Entry(self.master, relief=RIDGE)
        gather_text = Entry(self.master, relief=RIDGE)

        id_text.grid(row=0, column=0, sticky=NSEW)
        x_text.grid(row=0, column=1, sticky=NSEW)
        y_text.grid(row=0, column=2, sticky=NSEW)
        range_text.grid(row=0, column=3, sticky=NSEW)
        battery_text.grid(row=0, column=4, sticky=NSEW)
        rate_text.grid(row=0, column=5, sticky=NSEW)
        gather_text.grid(row=0, column=6, sticky=NSEW)

        id_text.insert(END, 'ID')
        x_text.insert(END, 'X')
        y_text.insert(END, 'Y')
        range_text.insert(END, 'Range')
        battery_text.insert(END, 'Battery')
        rate_text.insert(END, 'Recharge Rate')
        gather_text.insert(END, 'Gather Rate')

        id_text.configure(state=DISABLED)
        x_text.configure(state=DISABLED)
        y_text.configure(state=DISABLED)
        range_text.configure(state=DISABLED)
        battery_text.configure(state=DISABLED)
        rate_text.configure(state=DISABLED)
        gather_text.configure(state=DISABLED)

        for i in range(len(self.energizers)):
            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=0)
            tmp.insert(END, self.energizers[i].get_id())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=1)
            tmp.insert(END, self.energizers[i].get_x())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=2)
            tmp.insert(END, self.energizers[i].get_y())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=3)
            tmp.insert(END, self.energizers[i].get_range())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=4)
            tmp.insert(END, Inventory.f_str(self.energizers[i].get_battery()))
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=5)
            tmp.insert(END, self.energizers[i].get_recharge_rate())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=6)
            tmp.insert(END, self.energizers[i].get_gather_rate())
            tmp.configure(state=DISABLED)
