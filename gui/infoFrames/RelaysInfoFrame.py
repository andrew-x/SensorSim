__author__ = 'Andrew'
__author__ = 'Andrew'

from tkinter import *
from core.Controller import *


class RelaysInfoFrame(Frame):

    master = None
    relays = None

    submit_button = None

    rows = []
    cols = []

    def __init__(self):
        self.master = Tk()
        super(RelaysInfoFrame, self).__init__(self.master)

        self.init_window()
        self.set_widgets()
        self.mainloop()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.update_idletasks()
        self.master.title('Relays Information')

    def exit(self):
        self.master.destroy()

    def set_widgets(self):
        self.relays = Inventory.RELAYS

        id_text = Entry(self.master, relief=RIDGE)
        x_text = Entry(self.master, relief=RIDGE)
        y_text = Entry(self.master, relief=RIDGE)
        range_text = Entry(self.master, relief=RIDGE)
        battery_text = Entry(self.master, relief=RIDGE)
        e_use_in_text = Entry(self.master, relief=RIDGE)
        e_use_out_text = Entry(self.master, relief=RIDGE)
        parent_text = Entry(self.master, relief=RIDGE)
        send_success_text = Entry(self.master, relief=RIDGE)
        receive_success_text = Entry(self.master, relief=RIDGE)
        energy_average_text = Entry(self.master, relief=RIDGE)

        id_text.grid(row=0, column=0, sticky=NSEW)
        x_text.grid(row=0, column=1, sticky=NSEW)
        y_text.grid(row=0, column=2, sticky=NSEW)
        range_text.grid(row=0, column=3, sticky=NSEW)
        battery_text.grid(row=0, column=4, sticky=NSEW)
        e_use_in_text.grid(row=0, column=5, sticky=NSEW)
        e_use_out_text.grid(row=0, column=6, sticky=NSEW)
        parent_text.grid(row=0, column=7, sticky=NSEW)
        send_success_text.grid(row=0, column=8, sticky=NSEW)
        receive_success_text.grid(row=0, column=9, sticky=NSEW)
        energy_average_text.grid(row=0, column=10, sticky=NSEW)


        id_text.insert(END, 'ID')
        x_text.insert(END, 'X')
        y_text.insert(END, 'Y')
        range_text.insert(END, 'Range')
        battery_text.insert(END, 'Battery')
        e_use_in_text.insert(END, 'Energy use in')
        e_use_out_text.insert(END, 'Energy use out')
        parent_text.insert(END, 'Parent')
        send_success_text.insert(END, 'Send success rate')
        receive_success_text.insert(END, 'Receive success rate')
        energy_average_text.insert(END, 'Battery average')

        id_text.configure(state=DISABLED)
        x_text.configure(state=DISABLED)
        y_text.configure(state=DISABLED)
        range_text.configure(state=DISABLED)
        battery_text.configure(state=DISABLED)
        e_use_in_text.configure(state=DISABLED)
        e_use_out_text.configure(state=DISABLED)
        parent_text.configure(state=DISABLED)
        send_success_text.configure(state=DISABLED)
        receive_success_text.configure(state=DISABLED)
        energy_average_text.configure(state=DISABLED)

        for i in range(len(self.relays)):
            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=0)
            tmp.insert(END, self.relays[i].get_id())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=1)
            tmp.insert(END, self.relays[i].get_x())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=2)
            tmp.insert(END, self.relays[i].get_y())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=3)
            tmp.insert(END, self.relays[i].get_range())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=4)
            tmp.insert(END, Inventory.f_str(self.relays[i].get_battery()))
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=5)
            tmp.insert(END, self.relays[i].get_e_use_in())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=6)
            tmp.insert(END, self.relays[i].get_e_use_out())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=7)
            tmp.insert(END, self.relays[i].get_parent())
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=8)
            tmp.insert(END, Inventory.f_str(self.relays[i].get_send_success_rate()))
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=9)
            tmp.insert(END, Inventory.f_str(self.relays[i].get_receive_success_rate()))
            tmp.configure(state=DISABLED)

            tmp = Entry(self.master, relief=RIDGE)
            tmp.grid(row=(i+1), column=10)
            tmp.insert(END, Inventory.f_str(self.relays[i].get_energy_average()))
            tmp.configure(state=DISABLED)