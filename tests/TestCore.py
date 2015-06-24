__author__ = 'Andrew'

import unittest

from core.Controller import Controller


class TestCore(unittest.TestCase):
    control = None

    def setUp(self):
        pass

    def test_upper(self):
        self.assertEqual(5, 5)
