__author__ = 'Andrew'

from tkinter import *
from gui.MainFrame import *
import unittest


if Inventory.TEST_SWITCH is 1:
    unittest.main()
else:
    root = Tk()
    main_frame = MainFrame(master=root)
    main_frame.mainloop()
    root.destroy()

