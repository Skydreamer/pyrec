# -*- coding: utf-8 -*-
import MySQLdb, config

logger = config.create_logger(__name__)

HOST = 'localhost'
USER = 'skydreamer'
PASSWD = 'blogtwitter'
DB = 'pyrec_db'
CHARSET = 'utf8'

FILE_QUERY = 'INSERT INTO files (name, description, duration, path, hash, add_time) VALUES (%s, %s, %s, %s, %s, NOW())'
PART_QUERY = 'INSERT INTO parts (file_id, start_time, end_time, text) VALUES (%s, %s, %s, %s)'
CHECK_QUERY = 'SELECT COUNT(*) FROM files WHERE hash = %s'

class SQLConnector:
	def __init__(self):
		try:
			self.connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, charset=CHARSET)
			self.cursor = self.connection.cursor()
		except MySQLdb.Error:
			logger.exception('No database connection')

	def insert_files(self, filelist):
		logger.info('Loading data into the database..')
		for file in filelist:
			if not self.exist(file):
				self.cursor.execute(FILE_QUERY, (file.filename, file.description, file.audio_duration, file.index_filename, file.hash))
				file_insert_id = self.connection.insert_id()
				for part in file.content:
					with open(config.TEXT_PATH + part['text_file'], 'r') as text_file:
						rec_text = ' '.join([line[11:] for line in text_file])
					self.cursor.execute(PART_QUERY, (file_insert_id, part['start_time'], part['end_time'], rec_text))	
			else:
				logger.error('File already exists in database..')
		self.connection.commit()

	def exist(self, fileData):
		logger.info('Cheking hash matches..')
		self.cursor.execute(CHECK_QUERY, fileData.hash)
		return self.cursor.fetchall()[0][0] > 0

	
