__author__ = 'Andrew'

from tkinter import *
from core.Inventory import *

import sys
import py_compile
import webbrowser


class GenerateNodesFrame(Frame):
    master = None

    textArea = None

    base = []

    def __init__(self):
        self.master = Tk()
        super(GenerateNodesFrame, self).__init__(self.master)

        self.init_window()
        self.set_widgets()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.update_idletasks()
        self.master.title('Generate Nodes')

    def exit(self):
        self.master.destroy()

    def set_widgets(self):
        Button(self.master, text='Run', command=self.on_run).grid()
        Button(self.master, text='Edit', command=self.on_edit).grid()

    def on_run(self):
        os.system(("python " if os.name == 'nt' else "python3 ") + Inventory.GENERATE_NODES_PROTOCOL_FILENAME)
        Inventory.load_nodes()


    def on_edit(self):
        webbrowser.open(Inventory.GENERATE_NODES_PROTOCOL_FILENAME)
