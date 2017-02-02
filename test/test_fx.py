"""
Test the open_jpm.py
"""

import unittest2
from datetime import datetime
from os.path import join
from xlrd import open_workbook
from ft_converter.utility import get_current_path
from ft_converter.ft_main import read_transaction_file, show_row_in_error



class TestFX(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFX, self).__init__(*args, **kwargs)

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



    def test_read_line(self):
        file = join(get_current_path(), 'samples', 'sample_cash_fx.xlsx')
        transaction_list, row_in_error = read_transaction_file(file)
        show_row_in_error(row_in_error)
        # print(transaction_list)




    def verify_record1(self, record):
        self.assertEqual(len(record), 27)
        self.assertEqual(record['RecordType'], 'Buy')
        self.assertEqual(record['KeyValue'], '12229_2013-6-21_Buy_USY97279AB28_HTM_21632018100')
        self.assertEqual(record['Portfolio'], '12229')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['Investment'], 'USY97279AB28 HTM')
        self.assertEqual(record['SettleDate'], '2013-6-26')
        self.assertEqual(record['Quantity'], 300000)
        self.assertAlmostEqual(record['Price'], 92.942)
        self.assertAlmostEqual(record['CounterTDateFx'], 0.1288950475)
        self.assertEqual(record['CounterFXDenomination'], 'HKD')
        self.assertEqual(record['CounterInvestment'], 'USD')



    def verify_record2(self, record):
        self.assertEqual(len(record), 27)
        self.assertEqual(record['RecordType'], 'Sell')
        self.assertEqual(record['KeyValue'], '12548_2015-4-14_Sell_XS0545110354_HTM_43827946500')
        self.assertEqual(record['Portfolio'], '12548')
        self.assertEqual(record['LocationAccount'], 'JPM')
        self.assertEqual(record['Investment'], 'XS0545110354 HTM')
        self.assertEqual(record['SettleDate'], '2015-4-16')
        self.assertEqual(record['Quantity'], 500000)
        self.assertAlmostEqual(record['Price'], 113.1)
        self.assertAlmostEqual(record['CounterTDateFx'], 0.1290272635)
        self.assertEqual(record['CounterFXDenomination'], 'HKD')
        self.assertEqual(record['CounterInvestment'], 'USD')



    def verify_trade_info1(self, trade_info):
        """
        13th position in sample_FT.xlsx
        """
        self.assertEqual(trade_info['SCTYID_ISIN'], 'XS1328315723')
        self.assertEqual(trade_info['ENTRDATE'], datetime(2016,6,14))
        self.assertEqual(trade_info['QTY'], 1000000)
        self.assertEqual(trade_info['GROSSBAS'], -1003000)
        self.assertAlmostEqual(trade_info['ACCRBAS'], -25690.97)
        self.assertEqual(trade_info['LCLCCY'], 'USD')
        self.assertAlmostEqual(trade_info['TRADEPRC'], 100.3)
        self.assertAlmostEqual(trade_info['FXRATE'], 1)



    def verify_trade_info2(self, trade_info):
        """
        17th position in sample_FT.xlsx (BIDU US)
        """
        self.assertEqual(trade_info['SCTYNM'], 'BAIDU INC ADR NPV')
        self.assertEqual(trade_info['STLDATE'], datetime(2016,11,16))
        self.assertEqual(trade_info['QTY'], 35000)
        self.assertEqual(trade_info['ACCRBAS'], 0)
        self.assertAlmostEqual(trade_info['TRADEPRC'], 162.4842)
        self.assertAlmostEqual(trade_info['FXRATE'], 0.1288917245)



    def verify_trade_info3(self, trade_info):
        """
        2nd position in sample_FT_12229.xls
        """
        self.assertEqual(trade_info['SCTYID_SEDOL'], 'B8BTZG2')
        self.assertEqual(trade_info['TRDDATE'], datetime(2013,6,21))
        self.assertEqual(trade_info['QTY'], 300000)
        self.assertAlmostEqual(trade_info['GROSSBAS'], -2163201.81)
        self.assertAlmostEqual(trade_info['ACCRBAS'], -14818.26)
        self.assertEqual(trade_info['LCLCCY'], 'USD')
        self.assertAlmostEqual(trade_info['TRADEPRC'], 92.942)
        self.assertAlmostEqual(trade_info['FXRATE'], 0.1288950475)



    def verify_trade_info4(self, trade_info):
        """
        5th position in sample_FT_12229.xls
        """
        self.assertEqual(trade_info['SCTYID_ISIN'], 'XS0545110354')
        self.assertEqual(trade_info['STLDATE'], datetime(2015,4,16))
        self.assertEqual(trade_info['QTY'], 500000)
        self.assertEqual(trade_info['PRINB'], 4382794.65)
        self.assertAlmostEqual(trade_info['RGLCCYCLS'], -4106.51)
        self.assertEqual(trade_info['LCLCCY'], 'USD')
        self.assertAlmostEqual(trade_info['TRADEPRC'], 113.1)
        self.assertAlmostEqual(trade_info['FXRATE'], 0.1290272635)

