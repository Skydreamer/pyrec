# -*- coding: utf-8 -*-
import logging, os, random, string

CONTENT_PATH = r'./content/'
INDEX_PATH = r'./index/'
AUDIO_PATH = CONTENT_PATH + r'audio/'
TEXT_PATH = CONTENT_PATH + r'text/'
LOG_PATH = r'./logs/'

CONTENT_DIRS = [INDEX_PATH, CONTENT_PATH, AUDIO_PATH, TEXT_PATH, LOG_PATH]
REQUIRED_FILES = ['./tools/msu_ru_nsh.cd_cont_1000_8gau_16000', 
                 './tools/msu_ru_nsh.dic', 
                 './tools/msu_ru_nsh.lm.dmp']

MONO = 1
STEREO = 2
AUDIO_CHANNELS = MONO
AUDIO_RATE = 16000

class CustomStreamHandler(logging.StreamHandler):

    def emit(self, record):
        msg = record.msg.decode('utf-8', errors='replace')
        logging.StreamHandler.emit(self, record)

def create_logger(logger_name):
	logger = logging.getLogger(logger_name)
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter(fmt=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	
	stream_handler = CustomStreamHandler()#logging.StreamHandler()
	stream_handler.setLevel(logging.DEBUG)
	stream_handler.setFormatter(formatter)
	logger.addHandler(stream_handler)

	if not os.path.exists(LOG_PATH):
                os.makedirs(LOG_PATH)
	file_handler = logging.FileHandler(LOG_PATH + 'main.log', 'a', 'utf8', 0)
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	
	return logger

def self_check():
	logger.info('Check dirs...')
	for dir in CONTENT_DIRS:
		if os.path.exists(dir):
			logger.debug(dir + ' exist')
		else:
			logger.warning(dir + ' not found, creating...')
			os.makedirs(dir)
			logger.debug(dir + ' created')

	logger.info('Check files...')
	for file in REQUIRED_FILES:
		if os.path.exists(file):
			logger.debug(file + ' exist')
		else:
			logger.error(file + ' not found')	
			logger.debug('Terminating...')
			sys.exit(1)

def generate_random_string(length=10):
	return ''.join([random.choice(string.letters + string.digits) for _ in xrange(10)])

logger = create_logger(__name__)
