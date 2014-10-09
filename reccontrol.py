# -*- coding: utf-8 -*-
import worktools, subprocess, config

logger = config.create_logger(__name__)

class RecognitionController:
	def __init__(self, fileDatalList, threads):
		self.fileDatalList = fileDatalList
		self.threads = threads

	def start(self):
		logger.info('Speech recognition in files..')
		logger.info('Starting WorkerController() with recog tasks...')
		self.controller = worktools.WorkerController(self.fileDatalList, recognition_func, max_workers=self.threads)
		self.controller.run()
		logger.info('Done')

def recognition_func(fileData):
	for part_info in fileData.content:
		audio_name = part_info['audio_file']
		new_filename = '.'.join(audio_name.split('.')[:-1]) + '.txt'
		cmd = '''pocketsphinx_continuous -infile %s%s \\
			-hmm ./tools/msu_ru_nsh.cd_cont_1000_8gau_16000 \\
			-dict ./tools/msu_ru_nsh.dic -lm ./tools/msu_ru_nsh.lm.dmp \\
				> %s%s''' % (config.AUDIO_PATH, audio_name, config.TEXT_PATH, new_filename) 	
		logger.debug(cmd)
		output_err = subprocess.PIPE
		process = subprocess.Popen(cmd, shell=True, stderr=output_err)
		process.wait()
		part_info['text_file'] = new_filename
