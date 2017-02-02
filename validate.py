# coding=utf-8
# 
# Do validation for all types of transactions.

from ft_converter.utility import logger
from datetime import datetime



class InvalidLineInfo(Exception):
	pass

class InvalidTradeInfo(Exception):
	pass

class InvalidCashTransaction(Exception):
	pass



def validate_line_info(line_info):

	for fld in line_info:
		if fld in ['ACCT_ACNO', 'SCTYID_SMSEQ', 'SCTYID_SEDOL', 'SCTYID_CUSIP',
					'TRANTYP', 'TRANCOD', 'LCLCCY', 'SCTYID_ISIN'] \
				and not isinstance(line_info[fld], str):
			
			logger.error('validate_line_info(): field {0} should be string, value={1}'.
							format(fld, line_info[fld]))
			raise InvalidLineInfo()


		if fld in ['QTY', 'GROSSBAS', 'PRINB', 'RGLBVBAS', 'RGLCCYCLS',
					'ACCRBAS', 'TRNBVBAS', 'GROSSLCL', 'FXRATE', 'TRADEPRC'] \
				and not isinstance(line_info[fld], float):
			
			logger.error('validate_line_info(): field {0} should be float, value={1}'.
								format(fld, line_info[fld]))
			raise InvalidLineInfo()


		if fld in [ 'TRDDATE', 'STLDATE', 'ENTRDATE'] \
				and not isinstance(line_info[fld], datetime):
			logger.error('validate_line_info(): field {0} should be of type datetime, value={1}'.
								format(fld, line_info[fld]))
			raise InvalidLineInfo()		


		if line_info['STLDATE'] < line_info['TRDDATE'] or line_info['ENTRDATE'] < line_info['TRDDATE']:
			logger.error('validate_line_info(): invalid dates, trade date={0}, settle day={1}, enterday={2}'.
							format(line_info['TRDDATE'], line_info['STLDATE'], line_info['ENTRDATE']))
			raise InvalidLineInfo()

	
	# now validate further based on transaction type
	if line_info['TRANTYP'] in ['Purch', 'Sale']:
		validate_trade(line_info)
	elif line_info['TRANTYP'] in ['IATCW', 'IATCA', 'CashAdd', 'CashWth', 
									'FXSale', 'FXPurch']:
		validate_cash(line_info)



def validate_trade(line_info):
	"""
	Validate buy/sell transactions.
	"""

	if line_info['QTY'] > 0 and line_info['TRADEPRC'] > 0 and line_info['PRINB'] > 0 \
		and line_info['FXRATE'] > 0:
		pass
	else:
		logger.error('validate_trade(): quantity={0}, price={1}, prinb={2}, fx={3} is not valid'.
						format(line_info['QTY'], line_info['TRADEPRC'], 
								line_info['PRINB'], line_info['FXRATE']))
		raise InvalidTradeInfo()


	diff = abs(line_info['GROSSBAS'] * line_info['FXRATE'] - line_info['GROSSLCL'])
	if diff > 0.01:
		logger.error('validate_line_info(): FX validation failed, diff={0}'.format(diff))
		raise InvalidTradeInfo()


	# for equity trade
	diff2 = abs(line_info['PRINB']*line_info['FXRATE']) - line_info['QTY']*line_info['TRADEPRC']
	
	# for bond trade
	diff3 = abs(line_info['PRINB']*line_info['FXRATE']) - line_info['QTY']/100*line_info['TRADEPRC']
	# print('diff2={0}, diff3={1}'.format(diff2, diff3))
	if (abs(diff2) > 0.01 and abs(diff3) > 0.01):
		logger.error('validate_trade(): price validation failed')
		raise InvalidTradeInfo()



def validate_cash(line_info):
	"""
	Validate cash related transactions, namely:

	1. FXPurch, FXSale: buy one currency and sell another at the same time.
		They always occur in pairs.
	2. CashAdd: Cash deposit.
	3. CashWth: Cash withdrawal.
	4. IATCA, IATCW: cash transfers among accounts under FT control.
		These two transactions always occur in pairs.
	"""
	if line_info['GROSSBAS'] != 0 and line_info['PRINB'] != 0 and line_info['GROSSLCL'] != 0 \
		and line_info['FXRATE'] > 0:
		pass
	else:
		logger.error('validate_cash(): GROSSBAS={0}, PRINB={1}, GROSSLCL={2}, fx={3} is not valid'.
						format(line_info['GROSSBAS'], line_info['PRINB'], 
								line_info['GROSSLCL'], line_info['FXRATE']))
		raise InvalidCashTransaction()