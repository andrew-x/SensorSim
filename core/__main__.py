__author__ = 'Andrew'


from tests.TestCore import *
from gui.MainFrame import *

import unittest

if Inventory.TEST_SWITCH is 1:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCore)
    unittest.TextTestRunner().run(suite)
else:
    main_frame = MainFrame()
