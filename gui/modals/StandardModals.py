__author__ = 'Andrew'

from tkinter import *


class StandardModals():

    def __init__(self):
        pass

    @staticmethod
    def error_message(message):
        top = Toplevel(master=None, width=50)
        top.title("Error")
        msg = Message(top, text=message, anchor=CENTER)
        msg.pack()
        button = Button(top, text="Ok", command=top.destroy)
        button.pack()

    @staticmethod
    def message(message):
        top = Toplevel(master=None, width=100)
        top.title("Message")
        msg = Message(top, text=message, anchor=CENTER)
        msg.pack()
        button = Button(top, text="Ok", command=top.destroy)
        button.pack()