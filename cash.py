# coding=utf-8
# 
# Looks for Cash transactions from a list of FT transactions and generate 
# Geneva records from them.
#
# 1. IATCA, IATCW: inter account cash transfer (CA = deposit, CW = withdrawal)
# 2. CashAdd, CashWth: cash deposit and withdrawal.

from ft_converter.utility import logger, get_datemode
from ft_converter.ft_utility import convert_datetime_to_string, \
			get_LocationAccount, convert_float_to_datetime, \
			fix_duplicate_key_value, write_csv



def filter_cash_transaction(transaction_list):
	cash_transactions = []
	for transaction in transaction_list:
		if transaction['TRANTYP'] in ['IATCA', 'IATCW', 'CashAdd', 'CashWth']:
			cash_transactions.append(transaction)

	return cash_transactions



def create_cash_record_key_value(record):
	"""
	Geneva needs to have a unique key value associated with each record,
	so that different records won't overwrite each other, but the same
	record with different values will update itself.

	That means if we run the function over the same trade input file
	multiple times, a trade record must always be associated with the same
	key value.

	In this case the key value will be a string of the following format:

	<portfolio_code>_<trade_date>_FX_Buy_<buy_currency>_Sell_<sell_currency>_<value of buy amount>
	"""
	record['KeyValue'] = record['Portfolio']+ '_' + record['EventDate'] \
							+ '_Cash_' + record['RecordType'] \
							+ '_' + record['PriceDenomination'] \
							+ '_' + str(int(record['NetCounterAmount']*100))

	record['UserTranId1'] = record['KeyValue']



def to_geneva_cash_records(transaction_list):
	records = []
	for cash_transaction in filter_cash_transaction(transaction_list):
		records.append(create_cash_record(cash_transaction))

	return records



def get_cash_record_fields():
	"""
	Record fields in the upload file.
	"""
	return ['RecordType','RecordAction','KeyValue','KeyValue.KeyName',
			'UserTranId1','Portfolio','FundStructure','LocationAccount',
			'Strategy','EventDate','SettleDate','ActualSettleDate',
			'NetCounterAmount','PriceDenomination','CounterInvestment',
			'OEAccount','CounterTDateFx','CounterSDateFx','CounterFXDenomination']



def create_cash_record(cash_transaction):

	known_fields = {
		'RecordAction':'InsertUpdate',
		'KeyValue.KeyName':'UserTranId1',
		'Strategy':'Default',
		'FundStructure':'CALC',
		'OEAccount':'',
		'CounterTDateFx':'',
		'CounterSDateFx':'',
		'CounterFXDenomination':''
	}

	type_map = {
		'IATCA':'Deposit', 
		'IATCW':'Withdraw', 
		'CashAdd':'Deposit', 
		'CashWth':'Withdraw'
	}

	new_record = {}
	for fld in known_fields:
		new_record[fld] = known_fields[fld]

	new_record['RecordType'] = type_map[cash_transaction['TRANTYP']]
	new_record['Portfolio'] = cash_transaction['ACCT_ACNO']
	new_record['LocationAccount'] = get_LocationAccount(cash_transaction['ACCT_ACNO'])
	new_record['EventDate'] = convert_datetime_to_string(cash_transaction['TRDDATE'])
	new_record['SettleDate'] = convert_datetime_to_string(cash_transaction['STLDATE'])
	new_record['ActualSettleDate'] = new_record['SettleDate']
	new_record['NetCounterAmount'] = abs(cash_transaction['GROSSLCL'])
	new_record['PriceDenomination'] = cash_transaction['LCLCCY']
	new_record['CounterInvestment'] = new_record['PriceDenomination']

	create_cash_record_key_value(new_record)
	return new_record



def handle_cash(output_file, transaction_list):
	records = to_geneva_cash_records(filter_cash_transaction(transaction_list))
	fix_duplicate_key_value(records)
	write_csv(output_file, get_cash_record_fields(), records)
