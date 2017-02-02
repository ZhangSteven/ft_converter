"""
Test the open_jpm.py
"""

import unittest2
from datetime import datetime
from os.path import join
from xlrd import open_workbook
from ft_converter.utility import get_current_path
from ft_converter.ft_main import read_transaction_file, show_row_in_error
from ft_converter.fx import create_fx_pairs, to_geneva_fx_records



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



    def test_create_fx_pairs(self):
        file = join(get_current_path(), 'samples', 'sample_cash_fx.xlsx')
        transaction_list, row_in_error = read_transaction_file(file)
        show_row_in_error(row_in_error)
        fx_pairs = create_fx_pairs(transaction_list)
        self.assertEqual(len(fx_pairs), 4)
        self.verify_fx_pair1(fx_pairs[0])
        self.verify_fx_pair2(fx_pairs[3])



    def test_to_geneva_fx_records(self):
        file = join(get_current_path(), 'samples', 'sample_cash_fx.xlsx')
        transaction_list, row_in_error = read_transaction_file(file)
        show_row_in_error(row_in_error)
        records = to_geneva_fx_records(create_fx_pairs(transaction_list))
        self.assertEqual(len(records), 4)
        self.verify_record1(records[0])
        self.verify_record2(records[2])
        self.verify_record3(records[3])



    def verify_fx_pair1(self, fx_pair):
        fx_buy = fx_pair[0]
        fx_sell = fx_pair[1]
        self.assertEqual(fx_buy['TRDDATE'], datetime(2017,1,17))
        self.assertEqual(fx_sell['TRDDATE'], datetime(2017,1,17))
        self.assertEqual(fx_buy['LCLCCY'], 'USD')
        self.assertEqual(fx_sell['LCLCCY'], 'HKD')
        self.assertAlmostEqual(fx_buy['GROSSLCL'], 46150000)
        self.assertAlmostEqual(fx_sell['GROSSLCL'], -358243990)



    def verify_fx_pair2(self, fx_pair):
        fx_buy = fx_pair[0]
        fx_sell = fx_pair[1]
        self.assertEqual(fx_buy['TRDDATE'], datetime(2017,1,19))
        self.assertEqual(fx_sell['TRDDATE'], datetime(2017,1,19))
        self.assertEqual(fx_buy['LCLCCY'], 'HKD')
        self.assertEqual(fx_sell['LCLCCY'], 'USD')
        self.assertAlmostEqual(fx_buy['GROSSLCL'], 1230)
        self.assertAlmostEqual(fx_sell['GROSSLCL'], -158.83)



    def verify_record1(self, record):
        self.assertEqual(len(record), 20)
        self.assertEqual(record['RecordType'], 'SpotFX')
        self.assertEqual(record['KeyValue'], '12229_2017-1-17_FX_Buy_USD_Sell_HKD_4615000000')
        self.assertEqual(record['Portfolio'], '12229')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['Investment'], 'USD')
        self.assertEqual(record['CounterInvestment'], 'HKD')
        self.assertAlmostEqual(record['Quantity'], 46150000)
        self.assertAlmostEqual(record['NetCounterAmount'], 358243990)
        self.assertEqual(record['ContractFxRateNumerator'], 'USD')
        self.assertEqual(record['ContractFxRateDenominator'], 'HKD')
        self.assertEqual(record['EventDate'], '2017-1-17')



    def verify_record2(self, record):
        self.assertEqual(len(record), 20)
        self.assertEqual(record['RecordType'], 'SpotFX')
        self.assertEqual(record['KeyValue'], '12630_2017-1-19_FX_Buy_HKD_Sell_USD_123000')
        self.assertEqual(record['Portfolio'], '12630')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['Investment'], 'HKD')
        self.assertEqual(record['CounterInvestment'], 'USD')
        self.assertAlmostEqual(record['Quantity'], 1230)
        self.assertAlmostEqual(record['NetCounterAmount'], 158.82)
        self.assertEqual(record['ContractFxRateNumerator'], 'HKD')
        self.assertEqual(record['ContractFxRateDenominator'], 'USD')
        self.assertEqual(record['EventDate'], '2017-1-19')




    def verify_record3(self, record):
        self.assertEqual(len(record), 20)
        self.assertEqual(record['RecordType'], 'SpotFX')
        self.assertEqual(record['KeyValue'], '12630_2017-1-19_FX_Buy_HKD_Sell_USD_123000')
        self.assertEqual(record['Portfolio'], '12630')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['Investment'], 'HKD')
        self.assertEqual(record['CounterInvestment'], 'USD')
        self.assertAlmostEqual(record['Quantity'], 1230)
        self.assertAlmostEqual(record['NetCounterAmount'], 158.83)
        self.assertEqual(record['ContractFxRateNumerator'], 'HKD')
        self.assertEqual(record['ContractFxRateDenominator'], 'USD')
        self.assertEqual(record['EventDate'], '2017-1-19')
