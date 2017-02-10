# coding=utf-8
#

from ft_converter.utility import logger
from ft_converter.match import match_repeat


#
# To be completed. See small_program.match_transfer.py
#



# def refine_price(transaction_list):
# 	"""
# 	Refine the price for a transaction. When a transaction's price is zero, 
# 	i.e., absent from the FT file, its price will be calculated and saved. 

# 	1. For CSA and IATSA transactions, use the PRINB and FXRATE to calculate 
# 		the price.
# 	2. For CSW and IATSW transactions, match them to a CSA or IATSA transaction
# 		on the same day and for the same bond, then use the price of the
# 		CSA/IATSA transaction as the price.
# 	3. For those CSW, IATSW transactions that cannot be matched, leave the
# 		price as zero.

# 	Return the list of CSW and IATSW transactions that cannot be matched.
# 	"""
# 	transfer_in, transfer_out = filter_transfer_transactions(transaction_list)
# 	for transaction in transfer_in:
# 		transaction['TRADEPRC'] = abs(trade_info['PRINB']*trade_info['FXRATE']/trade_info['QTY']*100)

# 	matched, unmatched = match_repeat(transfer_out, transfer_in, map_transfer)
# 	for (transaction_out, transaction_in) in matched:
# 		transaction_out['TRADEPRC'] = transaction_in['TRADEPRC']
		
# 	return not_matched



# def filter_transfer_transaction(transaction_list):
# 	transfer_in = []
# 	transfer_out = []
# 	for transaction in transaction_list:
# 		if transaction['TRADEPRC'] > 0:
# 			logger.info('filter_transfer_transaction(): transaction {0} on {1} for bond {2} has a price {3}'.
# 						format(transaction['TRANTYP'], transaction['TRDDATE'], 
# 								transaction['SCTYID_ISIN'], transaction['TRADEPRC']))
# 			continue

# 		if transaction['TRANTYP'] in ['CSA', 'IATSA']:
# 			transfer_in.append(transaction)
# 		elif transaction['TRANTYP'] in ['CSW', 'IATSW']:
# 			transfer_out.append(transaction)
	
# 	return transfer_in, transfer_out



# def map_transfer(transfer_out, transfer_in):
# 	"""
# 	Map a transfer out transaction (CSW, IATSW) to a transfer in (CSA, IATSA).
# 	"""
# 	if transfer_out['EventDate'] == transfer_in['EventDate'] \
# 		and transfer_out['SCTYID_ISIN'] == transfer_in['SCTYID_ISIN'] \
# 		and transaction_out['SCTYID_ISIN'] != '':
# 		return True

# 	return False