# coding=utf-8
# 
# The main program to convert FT transaction files to geneva records.

from trade_converter.utility import logger, get_datemode, convert_datetime_to_string, \
									get_input_directory
from trade_converter.match import match
from trade_converter.validate import validate_line_info
from xlrd import open_workbook
from xlrd.xldate import xldate_as_datetime
from datetime import datetime



class LocationAccountNotFound(Exception):
	pass



def read_transaction_file(filename):
	"""
	Note: Read the transaction file for cash transactions, a cash transaction
	includes:

	1. FXPurch, FXSale: buy one currency and sell another at the same time.
		These two transactions always occur in pairs.
	2. CashAdd: Cash deposit.
	3. CashWth: Cash withdrawal.
	4. IATCA, IATCW: cash transfers among accounts under FT control.
		These two transactions always occur in pairs.
	"""
	logger.debug('read_transaction_file(): {0}'.format(filename))

	wb = open_workbook(filename=filename)
	ws = wb.sheet_by_index(0)

	fields = read_data_fields(ws, 0)
	
	row = 1
	output = []
	row_in_error = []
	while row < ws.nrows:
		if is_blank_line(ws, row):
			break

		line_info = read_line(ws, row, fields)
		try:
			validate_line_info(line_info)
			output.append(line_info)
		except:
			row_in_error.append(row)

		row = row + 1
	# end of while loop

	return output, row_in_error



def read_line(ws, row, fields):
	"""
	Read a line, create a line_info object with the information read.
	"""
	line_info = {}
	column = 0

	for fld in fields:
		logger.debug('read_line(): row={0}, column={1}'.format(row, column))

		cell_value = ws.cell_value(row, column)
		if isinstance(cell_value, str):
			cell_value = cell_value.strip()

		if fld in ['ACCT_ACNO', 'SCTYID_SMSEQ', 'SCTYID_SEDOL', 'SCTYID_CUSIP'] \
			and isinstance(cell_value, float):
			cell_value = str(int(cell_value))
		
		if fld in ['TRDDATE', 'STLDATE', 'ENTRDATE']:
			# some FT files uses traditional excel date, some uses
			# a float number to represent date.
			# cell_value = xldate_as_datetime(cell_value, get_datemode())
			cell_value = convert_float_to_datetime(cell_value)

		if fld in ['QTY', 'GROSSBAS', 'PRINB', 'RGLBVBAS', 'RGLCCYCLS',
					'ACCRBAS', 'TRNBVBAS', 'GROSSLCL', 'FXRATE', 'TRADEPRC'] \
					and isinstance(cell_value, str) and cell_value.strip() == '':	
			cell_value = 0.0
		
		line_info[fld] = cell_value
		column = column + 1
	# end of for loop

	return line_info



def read_data_fields(ws, row):
	column = 0
	fields = []
	while column < ws.ncols:
		cell_value = ws.cell_value(row, column)
		if is_empty_cell(ws, row, column):
			break

		fields.append(cell_value.strip())
		column = column + 1

	return fields



def get_LocationAccount(portfolio_id):
	boc_portfolios = ['12229', '12366', '12528', '12630', '12732', '12733']
	jpm_portfolios = ['12548']

	if portfolio_id in boc_portfolios:
		return 'BOCHK'
	elif portfolio_id in jpm_portfolios:
		return 'JPM'
	else:
		logger.error('get_LocationAccount(): no LocationAccount found for portfolio id {0}'.
						format(portfolio_id))
		raise LocationAccountNotFound()



def convert_float_to_datetime(value):
	"""
	the value is of type float, in the form of 'mmddyyyy' or 'mddyyyy'
	"""
	month = int(value/1000000)
	day = int((value - month*1000000)/10000)
	year = int(value - month*1000000 - day*10000)
	return datetime(year, month, day)



def is_blank_line(ws, row):
	for i in range(5):
		if not is_empty_cell(ws, row, i):
			return False

	return True



def is_empty_cell(ws, row, column):
	cell_value = ws.cell_value(row, column)
	if not isinstance(cell_value, str) or cell_value.strip() != '':
		return False
	else:
		return True




if __name__ == '__main__':
	
	
