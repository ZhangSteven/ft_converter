# coding=utf-8
# 
# logging and config goes here.
# 

import configparser, os
from datetime import datetime
from config_logging.file_logger import get_file_logger



class InvalidDatamode(Exception):
	pass



def get_current_path():
	"""
	Get the absolute path to the directory where this module is in.

	This piece of code comes from:

	http://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python
	"""
	return os.path.dirname(os.path.abspath(__file__))



def _load_config(filename='ft.config'):
	"""
	Read the config file, convert it to a config object. The config file is 
	supposed to be located in the same directory as the py files, and the
	default name is "config".

	Caution: uncaught exceptions will happen if the config files are missing
	or named incorrectly.
	"""
	path = get_current_path()
	config_file = path + '\\' + filename
	# print(config_file)
	cfg = configparser.ConfigParser()
	cfg.read(config_file)
	return cfg



# initialized only once when this module is first imported by others
if not 'config' in globals():
	config = _load_config()



def get_base_directory():
	"""
	The directory where the log file resides.
	"""
	global config
	directory = config['logging']['directory']
	if directory == '':
		directory = get_current_path()

	return directory



def _setup_logging():
    fn = get_base_directory() + '\\' + config['logging']['log_file']
    log_level = config['logging']['log_level']
    return get_file_logger(fn, log_level)



# initialized only once when this module is first imported by others
if not 'logger' in globals():
	logger = _setup_logging()



def get_datemode():
	"""
	Read datemode from the config object and return it (in integer)
	"""
	global config, logger
	d = config['excel']['datemode']
	try:
		datemode = int(d)
	except:
		logger.error('get_datemode(): invalid datemode value: {0}'.format(d))
		raise InvalidDatamode()

	return datemode



def get_input_directory():
	"""
	Read directory from the config object and return it.
	"""
	global config
	directory = config['input']['directory']
	if directory.strip() == '':
		directory = get_current_path()

	return directory



def get_output_directory():
	"""
	Read directory from the config object and return it.
	"""
	global config
	directory = config['output']['directory']
	if directory.strip() == '':
		directory = get_input_directory()

	return directory
