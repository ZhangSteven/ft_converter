# coding=utf-8
# 
# The main program to convert FT transaction files to geneva records.

from ft_converter.utility import logger, get_datemode, get_input_directory, \
			get_output_directory
from ft_converter.ft_utility import convert_float_to_datetime
from ft_converter.validate import validate_line_info
from ft_converter.fx import handle_fx
from ft_converter.cash import handle_cash
from xlrd import open_workbook
from xlrd.xldate import xldate_as_datetime
from datetime import datetime



def read_transaction_file(filename):
	"""
	Read a transaction file, create a list of transactions based on the
	information read.
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



def handle_transactions(transaction_list):
	pass



def show_row_in_error(row_in_error):
	if len(row_in_error) > 0:
		print('The following rows are in error:')
		for row in row_in_error:
			print(row)




if __name__ == '__main__':
	"""
	Read a transaction file from FT, extract all transactions from it, then
	create output csv file based on the transactions.

	The user can supply a transaction type to handle, in that case, the program
	only search for this kind of transactions and ignore the rest. If no
	transaction type is supplied, then the program generates output for all
	transactions it can handle.
	"""
	import argparse
	parser = argparse.ArgumentParser(description='Read ft transaction file and create csv output for Geneva upload.')
	parser.add_argument('transaction_file')
	parser.add_argument('--type', help='handle a specific transaction type', required=False)
	args = parser.parse_args()

	import os, sys
	input_file = os.path.join(get_input_directory(), args.transaction_file)
	if not os.path.exists(input_file):
		print('{0} does not exist'.format(input_file))
		sys.exit(1)

	try:
		transaction_list, row_in_error = read_transaction_file(input_file)

		if not args.type is None:
			if args.type == 'fx':
				handler = handle_fx
			elif args.type == 'cash':
				handler = handle_cash
			else:
				print('unrecoginized transaction type: {0}'.format(args.type))
				sys.exit(1)

			handler(os.path.join(get_output_directory(), '{0}_upload.csv'.format(args.type)), 
							transaction_list)
		else:
			handle_transactions(transaction_list)

	except:
		logger.exception('ft_main():')
		print('Something goes wrong, check log file.')
	else:
		print('OK.')
	finally:
		show_row_in_error(row_in_error)

