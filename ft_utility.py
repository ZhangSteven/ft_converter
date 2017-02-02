# coding=utf-8
# 
# Command functions called by other modules go here.
# 

from datetime import datetime
from ft_converter.utility import logger



class LocationAccountNotFound(Exception):
	pass



def convert_float_to_datetime(value):
	"""
	the value is of type float, in the form of 'mmddyyyy' or 'mddyyyy'
	"""
	month = int(value/1000000)
	day = int((value - month*1000000)/10000)
	year = int(value - month*1000000 - day*10000)
	return datetime(year, month, day)



def convert_datetime_to_string(dt):
	"""
	convert a datetime object to string in the 'yyyy-mm-dd' format.
	"""
	return '{0}-{1}-{2}'.format(dt.year, dt.month, dt.day)



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



def fix_duplicate_key_value(records):
	"""
	Detect whether there are duplicate keyvalues for different records,
	if there are, modify the keyvalues to make all keys unique.
	"""
	keys = []
	for record in records:
		i = 1
		temp_key = record['KeyValue']
		while temp_key in keys:
			temp_key = record['KeyValue'] + '_' + str(i)
			i = i + 1

		record['KeyValue'] = temp_key
		record['UserTranId1'] = temp_key
		keys.append(record['KeyValue'])

	# check again
	keys = []
	for record in records:
		if record['KeyValue'] in keys:
			logger.error('fix_duplicate_key_value(): duplicate keys still exists, key={0}, investment={1}'.
							format(record['KeyValue'], record['Investment']))
			raise DuplicateKeys()

		keys.append(record['KeyValue'])
