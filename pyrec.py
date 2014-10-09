#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse, logging, os, time, shutil
import convcontrol, reccontrol, filecheck, dbconn, config

def get_cmd_arguments():
	logger.info('Getting commandline arguments...')
	if len(sys.argv) < 2:
			logger.error('Not enough arguments!')
			sys.exit(1)

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', nargs='+', help='Path to audio files', default=[])
	parser.add_argument('-d', '--dir', '--directory', nargs='+', help='Path to directory with files', default=[])
	parser.add_argument('-f', '--formats', nargs='+', choices=['mp3','wav','avi'], default=['wav', 'mp3'], type=str)
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('-l', '--language', choices=['en','ru'], default='ru')
	parser.add_argument('--duration', choices=range(30, 3600), default=60)
	parser.add_argument('-rt', default=4, type=int)
	parser.add_argument('-ct', default=4, type=int)
	return parser.parse_args(sys.argv[1:])

class RecProgram:
    def __init__(self):
		self.filelist = []

    def start(self):
        start_time = time.time()
		logger.info('Started')
		config.self_check()
		self.args = get_cmd_arguments()
		self.filelist = filecheck.FileListMaker(folders=self.args.dir, files=self.args.input, formats=self.args.formats, part_duration=self.args.duration).process()

		if len(self.filelist) == 0:
			logger.error('There are no files to continue')
			sys.exit(1)

		convcontrol.ConvertionController(self.filelist, self.args.ct).start()
		reccontrol.RecognitionController(self.filelist, self.args.rt).start()
		dbconn.SQLConnector().insert_files(self.filelist)

		self.print_files()
		self.clean()
		logger.info('Operation time: %is' % (time.time() - start_time))

	def print_files(self):
		print '-' * 80
		self.filelist.sort()
		for file in self.filelist:
			print file

	def clean(self):
		logger.info('Remove trash files')
		for file in self.filelist:
			for part in file.content:
				os.remove(config.AUDIO_PATH + part['audio_file'])
				os.remove(config.TEXT_PATH + part['text_file'])

logger = config.create_logger(__name__)	

if __name__ == '__main__':
	program = RecProgram()
	program.start()
	#filecheck.remove_all_trash(result)
