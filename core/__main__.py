__author__ = 'Andrew'
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.TestCore import *
from gui.MainFrame import *
import plotly
import unittest

if Inventory.TEST_SWITCH is 1:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCore)
    unittest.TextTestRunner().run(suite)
else:
    plotly.tools.set_credentials_file(username='andrewxia', api_key='bzxz356iye') # Set credentials for Plotly
    main_frame = MainFrame()
