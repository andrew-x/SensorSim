__author__ = 'Andrew'

from datatypes.Energizer import *
from tests.TestCore import *
from core.Inventory import *
from gui.MainFrame import *

import unittest

if __name__ == '__main__':
    if Inventory.TEST_SWITCH is 1:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCore)
        unittest.TextTestRunner().run(suite)
    else:
        main_frame = MainFrame()
