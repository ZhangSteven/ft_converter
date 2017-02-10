"""
Test the open_jpm.py
"""

import unittest2
from datetime import datetime
from os.path import join
from xlrd import open_workbook
from ft_converter.utility import get_current_path
from ft_converter.ft_main import read_transaction_file, show_row_in_error
from ft_converter.transfer import refine_price



class TestTransfer(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTransfer, self).__init__(*args, **kwargs)

    def setUp(self):
        """
            Run before a test function
        """
        pass

    def tearDown(self):
        """
            Run after a test finishes
        """
        pass



    def test_refine_price(self):
        """
        Not tested yet.
        """
        self.assertEqual(1, 0)
