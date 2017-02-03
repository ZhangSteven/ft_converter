# coding=utf-8
# 
# Looks for FX transactions from a list of FT transactions and generate 
# Geneva records from them.
#
# FXPurch, FXSale: buy one currency and sell another at the same time, they
# always occur in pairs.

from ft_converter.utility import logger, get_datemode
from ft_converter.ft_utility import convert_datetime_to_string, \
			get_LocationAccount, convert_float_to_datetime, \
			fix_duplicate_key_value, write_csv
from ft_converter.match import match



class InconsistentFXTrades(Exception):
	pass



def create_fx_pairs(transaction_list):
	"""
	Since FXPurch/FXSale always occur in pairs, read the transaction_list,
	create a list of such fx buy/sell pairs.
	"""
	buy_list, sell_list = filter_fx_trade_list(transaction_list)
	if len(buy_list) != len(sell_list):
		logger.error('create_fx_pairs(): {0} fx buy, {1} fx sell, not equal'.
						format(len(buy_list), len(sell_list)))
		raise InconsistentFXTrades()

	return match(buy_list, sell_list, is_fx_trade_pair)



def filter_fx_trade_list(transaction_list):
	"""
	From the list of transactions, filter out the fx buy trades and fx
	sell trades.
	"""
	buy_list = []
	sell_list = []
	for transaction in transaction_list:
		if transaction['TRANTYP'] == 'FXPurch':
			buy_list.append(transaction)
		elif transaction['TRANTYP'] == 'FXSale':
			sell_list.append(transaction)

	return buy_list, sell_list



def is_fx_trade_pair(fx_buy, fx_sell):
	"""
	Determine whether a FX buy trade forms a pair with a FX sell trade.
	FT records use two transactions to book a FX trade, say buy HKD
	sell USD, meaning sell some USD to exchange some HKD. The sell
	and buy amount are booked into the sell/buy trades respectively.
	"""
	if fx_buy['ACCT_ACNO'] == fx_sell['ACCT_ACNO'] \
		and fx_buy['TRDDATE'] == fx_sell['TRDDATE'] \
		and fx_buy['STLDATE'] == fx_sell['STLDATE'] \
		and abs(fx_buy['GROSSBAS'] + fx_sell['GROSSBAS']) < 0.001:

		return True

	return False



def create_fx_record_key_value(record):
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
							+ '_FX_Buy_' + record['Investment'] \
							+ '_Sell_' + record['CounterInvestment'] \
							+ '_' + str(int(record['Quantity']*100))

	record['UserTranId1'] = record['KeyValue']



def to_geneva_fx_records(fx_pair_list):
	records = []
	record_fields = get_fx_record_fields()
	for (fx_buy, fx_sell) in fx_pair_list:
		records.append(create_fx_record(fx_buy, fx_sell, record_fields))

	return records



def get_fx_record_fields():
	"""
	Record fields in the upload file.
	"""
	return ['RecordType','RecordAction','KeyValue','KeyValue.KeyName',
			'UserTranId1','Portfolio','LocationAccount','Strategy',
			'Broker','EventDate','SettleDate','ActualSettleDate',
			'FundStructure','Investment','CounterInvestment','Quantity',
			'NetCounterAmount','ContractFxRateNumerator',
			'ContractFxRateDenominator','ContractFxRate']



def create_fx_record(fx_buy, fx_sell, record_fields):

	known_fields = {
		'RecordType':'SpotFX',
		'RecordAction':'InsertUpdate',
		'KeyValue.KeyName':'UserTranId1',
		'Strategy':'Default',
		'FundStructure':'CALC',
		'ContractFxRate':'CALC'
	}

	new_record = {}
	for record_field in record_fields:
		if record_field in known_fields:
			new_record[record_field] = known_fields[record_field]
		elif record_field == 'Portfolio':
			new_record[record_field] = fx_buy['ACCT_ACNO']
		elif record_field == 'LocationAccount':
			new_record[record_field] = get_LocationAccount(fx_buy['ACCT_ACNO'])
		elif record_field == 'Broker':
			new_record[record_field] = new_record['LocationAccount']
		elif record_field == 'EventDate':
			new_record[record_field] = convert_datetime_to_string(fx_buy['TRDDATE'])
		elif record_field == 'SettleDate':
			new_record[record_field] = convert_datetime_to_string(fx_buy['STLDATE'])
		elif record_field == 'ActualSettleDate':
			new_record[record_field] = new_record['SettleDate']
		elif record_field == 'Investment':
			new_record[record_field] = fx_buy['LCLCCY']
		elif record_field == 'CounterInvestment':
			new_record[record_field] = fx_sell['LCLCCY']
		elif record_field == 'Quantity':
			new_record[record_field] = fx_buy['GROSSLCL']
		elif record_field == 'NetCounterAmount':
			new_record[record_field] = abs(fx_sell['GROSSLCL'])
		elif record_field == 'ContractFxRateNumerator':
			new_record[record_field] = new_record['Investment']
		elif record_field == 'ContractFxRateDenominator':
			new_record[record_field] = new_record['CounterInvestment']
	# end of for loop

	create_fx_record_key_value(new_record)
	return new_record
	


def handle_fx(output_file, transaction_list):
	records = to_geneva_fx_records(create_fx_pairs(transaction_list))
	fix_duplicate_key_value(records)
	write_csv(output_file, get_fx_record_fields(), records)
