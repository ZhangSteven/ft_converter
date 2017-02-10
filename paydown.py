# coding=utf-8
# 
# Looks for Paydown transactions from a list of FT transactions and generate 
# Geneva records from them.
#

from datetime import datetime
from ft_converter.utility import logger, get_datemode, get_current_path
from ft_converter.ft_utility import convert_datetime_to_string, \
			fix_duplicate_key_value, write_csv, get_geneva_investment_id
from investment_lookup.id_lookup import get_investment_Ids



class InvalidPaydownType(Exception):
	pass

class HoldingInfoNotFound(Exception):
	pass

class InconsistentPaydownFactor(Exception):
	pass



def filter_paydown_transaction(transaction_list):
	cash_transactions = []
	for transaction in transaction_list:
		if transaction['TRANTYP'] == 'PAYDOWN':
			cash_transactions.append(transaction)

	return cash_transactions



def create_paydown_record_key_value(record):
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
	record['KeyValue'] = record['Paydown']+ '_' + record['EventDate'] \
							+ '_' + record['Portfolio'] \
							+ '_' + record['Investment'].replace(' ', '_')
	record['UserTranId1'] = record['KeyValue']



def to_geneva_paydown_records(transaction_list):
	records = []
	transactions = filter_paydown_transaction(transaction_list)


	for paydown_transaction in transactions:
		records.append(create_paydown_record(paydown_transaction))

	return records



def find_paydown_factor(paydown):
	"""
	Find factor for a paydown transaction.
	"""
	if abs(paydown['QTY']/paydown['GROSSLCL'] - 1) > 0.000001:
		# pay amount != quantity, then the bond is not repaying at par, 
		# so pay down loss type cannot be 'no loss'.
		logger.error('find_paydown_factors(): not repaying at par, isin={0}, on {1}'.
						format(paydown['SCTYID_ISIN'], paydown['TRDDATE']))
		raise InvalidPaydownType()
	
	holding = get_holding(paydown['ACCT_ACNO'], paydown['SCTYID_ISIN'], paydown['TRDDATE'])
	factor = (holding - paydown['QTY'])/holding
	if abs(factor - get_factor_Bloomberg(paydown['SCTYID_ISIN'], paydown['TRDDATE'])) > 0.0001:
		logger.error('find_paydown_factors(): paydown factor {0} differs from Bloomberg {1}'.
						format(factor, get_factor_Bloomberg(paydown['SCTYID_ISIN'], paydown['TRDDATE'])))
		raise InconsistentPaydownFactor()

	return factor



def read_schedule_file():
	"""
	Load Bloomberg paydown schedule from a file. The file should contain
	one or more sheets, each sheet containing paydown schedule for a bond,
	with the sheet name being the bond isin code.
	"""
	wb = open_workbook(filename=get_current_path() + '\\paydown_schedule.xlsx')
	output = {}
	for st_name in wb.sheet_names():
		ws = wb.sheet_by_name(st_name)
		output[st_name] = []
		row = 1

		while row < ws.nrows:
			if is_blank_line(ws, row):
				break

			output[st_name].append(read_line(ws, row, ['Date', 'Factor', 'Coupon']))
			row = row + 1
		# end of while loop

		return output



def read_line(ws, row, fields):
	"""
	Read a line from the Bloomberg schedule file.
	"""
	line_info = {}
	column = 0

	for fld in fields:
		logger.debug('read_line(): row={0}, column={1}'.format(row, column))

		cell_value = ws.cell_value(row, column)
		if isinstance(cell_value, str):
			cell_value = cell_value.strip()

		if fld == 'Date':
			cell_value = convert_date_value(cell_value)
		
		line_info[fld] = cell_value
		column = column + 1
	# end of for loop

	return line_info



def convert_date_value(date_value):
	"""
	In Bloomberg schedule file, the date value is a string consisting of
	month and year in the format 'month/year', we return a tuple (year, month).
	"""
	tokens = date_value.split('/')
	return (int(tokens[1]), int(tokens[0]))



def get_holding(portfolio_id, isin, holding_date):
	"""
	Get the quantity of holding of a position which needs paydown in a portfolio, 
	as of certain date.
	"""
	if portfolio_id == '12229' and holding_date > datetime(2015,10,8) \
		and holding_date < datetime(2017,1,16) and isin == 'USG8116KAB82':
		# this bond was bought on 2015-10-9, no other buy/sell or transfers
		# occurred after that, before 2017-1-16
		return 5320000

	# information not found
	logger.error('get_holding(): could not find holding info for portfolio {0}, isin {1}, on {2}'.
					format(portfolio_id, isin, holding_date))
	raise HoldingInfoNotFound()



def get_paydown_record_fields():
	"""
	Record fields in the upload file.
	"""
	return ['RecordType','RecordAction','KeyValue','KeyValue.KeyName',
			'UserTranId1','Portfolio','Investment','EventDate',
			'SettleDate','ActualSettleDate','Comments','Payment',
			'PaydownLossType','PerShareAmount']



def create_paydown_record(paydown_transaction):

	known_fields = {
		'RecordType':'Paydown',
		'RecordAction':'InsertUpdate',
		'KeyValue.KeyName':'UserTranId1',
		'Comments':'',
		'Payment':'AlwaysInCash',
		'PaydownLossType':'No Loss'
	}

	new_record = {}
	for fld in known_fields:
		new_record[fld] = known_fields[fld]

	new_record['Portfolio'] = paydown_transaction['ACCT_ACNO']
	new_record['Investment'] = get_geneva_investment_id(paydown_transaction)
	new_record['EventDate'] = convert_datetime_to_string(paydown_transaction['TRDDATE'])
	new_record['SettleDate'] = convert_datetime_to_string(paydown_transaction['STLDATE'])
	new_record['ActualSettleDate'] = new_record['SettleDate']
	new_record['PerShareAmount'] = find_paydown_factor(paydown_transaction)

	create_paydown_record_key_value(new_record)
	return new_record



def handle_paydown(output_file, transaction_list):
	records = to_geneva_paydown_records(transaction_list)
	fix_duplicate_key_value(records)
	write_csv(output_file, get_paydown_record_fields(), records)
