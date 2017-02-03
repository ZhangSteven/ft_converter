"""
Test the open_jpm.py
"""

import unittest2
from datetime import datetime
from os.path import join
from xlrd import open_workbook
from ft_converter.utility import get_current_path
from ft_converter.ft_main import read_transaction_file, show_row_in_error
from ft_converter.cash import filter_cash_transaction, to_geneva_cash_records



class TestCash(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCash, self).__init__(*args, **kwargs)

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



    def test_to_geneva_cash_records(self):
        file = join(get_current_path(), 'samples', 'sample_cash_fx.xlsx')
        transaction_list, row_in_error = read_transaction_file(file)
        show_row_in_error(row_in_error)
        records = to_geneva_cash_records(filter_cash_transaction(transaction_list))
        self.assertEqual(len(records), 26)
        self.verify_record1(records[0])
        self.verify_record2(records[2])
        self.verify_record3(records[4])
        # self.verify_record4(records[9])



    def verify_record1(self, record):
        self.assertEqual(len(record), 19)
        self.assertEqual(record['RecordType'], 'Withdraw')
        self.assertEqual(record['KeyValue'], '12229_2016-12-19_Cash_Withdraw_USD_10901250')
        self.assertEqual(record['Portfolio'], '12229')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['PriceDenomination'], 'USD')
        self.assertEqual(record['CounterInvestment'], 'USD')
        self.assertAlmostEqual(record['NetCounterAmount'], 109012.5)
        self.assertEqual(record['EventDate'], '2016-12-19')



    def verify_record2(self, record):
        self.assertEqual(len(record), 19)
        self.assertEqual(record['RecordType'], 'Deposit')
        self.assertEqual(record['UserTranId1'], '12229_2016-12-21_Cash_Deposit_USD_1000000000')
        self.assertEqual(record['Portfolio'], '12229')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['PriceDenomination'], 'USD')
        self.assertEqual(record['CounterInvestment'], 'USD')
        self.assertAlmostEqual(record['NetCounterAmount'], 10000000)
        self.assertEqual(record['ActualSettleDate'], '2016-12-21')




    def verify_record3(self, record):
        self.assertEqual(len(record), 19)
        self.assertEqual(record['RecordType'], 'Deposit')
        self.assertEqual(record['UserTranId1'], '12229_2016-12-28_Cash_Deposit_HKD_213164400')
        self.assertEqual(record['Portfolio'], '12229')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['PriceDenomination'], 'HKD')
        self.assertEqual(record['CounterInvestment'], 'HKD')
        self.assertAlmostEqual(record['NetCounterAmount'], 2131644)
        self.assertEqual(record['EventDate'], '2016-12-28')



    def verify_record4(self, record):
        self.assertEqual(len(record), 19)
        self.assertEqual(record['RecordType'], 'Withdraw')
        self.assertEqual(record['KeyValue'], '12229_2017-1-9_Cash_Withdraw_CNY_10383147790')
        self.assertEqual(record['Portfolio'], '12229')
        self.assertEqual(record['LocationAccount'], 'BOCHK')
        self.assertEqual(record['PriceDenomination'], 'CNY')
        self.assertEqual(record['CounterInvestment'], 'CNY')
        self.assertAlmostEqual(record['NetCounterAmount'], 103831477.9)
        self.assertEqual(record['ActualSettleDate'], '2017-1-9')