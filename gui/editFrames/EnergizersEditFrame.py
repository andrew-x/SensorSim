__author__ = 'Andrew'

from tkinter import *
from core.Controller import *


class EnergizersEditFrame(Frame):

    master = None
    energizers = None

    submit_button = None

    rows = []
    cols = []

    def __init__(self, master=None):
        super(EnergizersEditFrame, self).__init__(master)

        self.master = master

        self.energizers = Controller.get_energizers()

        self.init_window()
        self.set_widgets()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

        self.master.update_idletasks()

        self.master.title('Energizers Information')

    def exit(self):
        self.master.destroy()

    def set_widgets(self):
        id_text = Entry(self.master, relief=RIDGE)
        x_text = Entry(self.master, relief=RIDGE)
        y_text = Entry(self.master, relief=RIDGE)
        range_text = Entry(self.master, relief=RIDGE)
        battery_text = Entry(self.master, relief=RIDGE)
        rate_text = Entry(self.master, relief=RIDGE)

        id_text.grid(row=0, column=0, sticky=NSEW)
        x_text.grid(row=0, column=1, sticky=NSEW)
        y_text.grid(row=0, column=2, sticky=NSEW)
        range_text.grid(row=0, column=3, sticky=NSEW)
        battery_text.grid(row=0, column=4, sticky=NSEW)
        rate_text.grid(row=0, column=5, sticky=NSEW)

        id_text.insert(END, 'ID')
        x_text.insert(END, 'X')
        y_text.insert(END, 'Y')
        range_text.insert(END, 'Range')
        battery_text.insert(END, 'Battery')
        rate_text.insert(END, 'Recharge Rate')

        id_text.configure(state=DISABLED)
        x_text.configure(state=DISABLED)
        y_text.configure(state=DISABLED)
        range_text.configure(state=DISABLED)
        battery_text.configure(state=DISABLED)
        rate_text.configure(state=DISABLED)

        self.rows = []
        for i in range(len(self.energizers)):
            self.cols = []

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=0)
            tmp.insert(END, self.energizers[i].get_id())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=1)
            tmp.insert(END, self.energizers[i].get_x())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=2)
            tmp.insert(END, self.energizers[i].get_y())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=3)
            tmp.insert(END, self.energizers[i].get_range())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=4)
            tmp.insert(END, self.energizers[i].get_battery())
            self.cols.append(tmp)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=5)
            tmp.insert(END, self.energizers[i].get_rate())
            self.cols.append(tmp)

            self.rows.append(self.cols)

        self.submit_button = Button(self.master, text='Submit', command=self.submit)
        self.submit_button.grid(row=len(self.energizers)+1, column=2, pady=10, columnspan=2)

    def submit(self):
        tmp = []
        for r in self.rows:
            e = Energizer(r[0].get(), r[1].get(), r[2].get(), r[3].get(), r[4].get(), r[5].get())
            tmp.append(e)

        Controller.set_energizers(tmp)

        self.exit()

