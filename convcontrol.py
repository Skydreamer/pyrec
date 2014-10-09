# -*- coding: utf-8 -*-
import worktools, subprocess, time, sys, config

logger = config.create_logger(__name__)

class ConvertionController:
	def __init__(self, fileDatalList, threads):
		self.fileDatalList = fileDatalList
		self.threads = threads

	def start(self):
		logger.info('Converting files to .wav and slice apart...')
		logger.info('Starting WorkerController() with conv tasks...')
		controller = worktools.WorkerController(self.fileDatalList, convertion_func, max_workers=self.threads)
		controller.run()

def convertion_func(fileData):
	for part_info in fileData.content:
		uniquilizer = config.generate_random_string()
		new_filename = fileData.filename + '_' + str(part_info['part_num']) + '_' + uniquilizer + '.wav'
		cmd = 'avconv -i %s -ss %i -t %i -ac %i -ar %i %s%s' % (
				config.INDEX_PATH + fileData.index_filename, 
				part_info['start_time'], 
				fileData.part_duration, 
				config.AUDIO_CHANNELS,
				config.AUDIO_RATE,
				config.AUDIO_PATH, 
				new_filename)
		logger.debug(cmd)
		output_err = subprocess.PIPE
		process = subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=output_err)
		process.wait()
		part_info['audio_file'] = new_filename
