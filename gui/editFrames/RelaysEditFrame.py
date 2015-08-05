__author__ = 'Andrew'

from tkinter import *
from core.Controller import *


class RelaysEditFrame(Frame):

    master = None
    relays = None

    submit_button = None

    rows = []
    cols = []

    def __init__(self, master=None):
        super(RelaysEditFrame, self).__init__(master)

        self.master = master
        self.relays = Inventory.RELAYS

        self.init_window()
        self.set_widgets()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        self.master.update_idletasks()

        self.master.title('Relays Information')

    def exit(self):
        self.master.destroy()

    def set_widgets(self):
        id_text = Entry(self.master, relief=RIDGE)
        x_text = Entry(self.master, relief=RIDGE)
        y_text = Entry(self.master, relief=RIDGE)
        range_text = Entry(self.master, relief=RIDGE)
        battery_text = Entry(self.master, relief=RIDGE)
        e_use_in_text = Entry(self.master, relief=RIDGE)
        e_use_out_text = Entry(self.master, relief=RIDGE)
        parent_text = Entry(self.master, relief=RIDGE)

        id_text.grid(row=0, column=0, sticky=NSEW)
        x_text.grid(row=0, column=1, sticky=NSEW)
        y_text.grid(row=0, column=2, sticky=NSEW)
        range_text.grid(row=0, column=3, sticky=NSEW)
        battery_text.grid(row=0, column=4, sticky=NSEW)
        e_use_in_text.grid(row=0, column=5, sticky=NSEW)
        e_use_out_text.grid(row=0, column=6, sticky=NSEW)
        parent_text.grid(row=0, column=7, sticky=NSEW)

        id_text.insert(END, 'ID')
        x_text.insert(END, 'X')
        y_text.insert(END, 'Y')
        range_text.insert(END, 'Range')
        battery_text.insert(END, 'Battery')
        e_use_in_text.insert(END, 'Energy use in')
        e_use_out_text.insert(END, 'Energy use out')
        parent_text.insert(END, 'Parent')

        id_text.configure(state=DISABLED)
        x_text.configure(state=DISABLED)
        y_text.configure(state=DISABLED)
        range_text.configure(state=DISABLED)
        battery_text.configure(state=DISABLED)
        e_use_in_text.configure(state=DISABLED)
        e_use_out_text.configure(state=DISABLED)
        parent_text.configure(state=DISABLED)

        self.rows = []
        for i in range(len(self.relays)):
            self.cols = []

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=0)
            tmp.insert(END, self.relays[i].get_id())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=1)
            tmp.insert(END, self.relays[i].get_x())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=2)
            tmp.insert(END, self.relays[i].get_y())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=3)
            tmp.insert(END, self.relays[i].get_range())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=4)
            tmp.insert(END, self.relays[i].get_battery())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=5)
            tmp.insert(END, self.relays[i].get_e_use_in())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=6)
            tmp.insert(END, self.relays[i].get_e_use_out())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=7)
            tmp.insert(END, self.relays[i].get_parent())
            self.cols.append(tmp)

            self.rows.append(self.cols)

        self.submit_button = Button(self.master, text='Submit', command=self.submit)
        self.submit_button.grid(row=len(self.relays)+1, column=3, pady=10, columnspan=2)

    def submit(self):
        tmp = []
        for r in self.rows:
            e = Relay(r[0].get(), r[1].get(), r[2].get(), r[3].get(), r[4].get(), r[5].get(), r[6].get(), r[7].get())
            tmp.append(e)

        Controller.set_relays(tmp)

        self.exit()
