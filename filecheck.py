# -*- coding: utf-8 -*-
import os, wave, math, subprocess, hashlib, shutil, time
import config

logger = config.create_logger(__name__)

class FileListMaker:
	def __init__(self, folders, files, formats, part_duration):
		self.folders = folders
		self.files = files
		self.formats = formats
		self.part_duration = part_duration
		self.filelist = []
	
	def check_files(self, files):
		logger.info('Checking single files...')
		for file in files:
			if os.path.isfile(file) and self.check_extension(file):
					filedata = FileData(file)	 
					self.filelist.append(filedata)
			else:
				logger.debug('%s not a file or has unsupported format' % file)

	def check_extension(self, file):
		extension = os.path.splitext(file)[1][1:]
		return extension in self.formats
		
	def check_dirs(self, dirs):
		logger.info('Checking files in folders...')
		supp_files = []
		for dir in dirs:
			if os.path.isdir(dir):
				supp_files = map(lambda f: os.path.join(dir, f), os.listdir(dir))
				supp_files = filter(os.path.isfile, supp_files)
			else:
				logger.debug('%s not a directory')
		return supp_files

	def remove_duplicates(self):
		logger.info('Removing duplicates...')
		self.filelist = list(set(self.filelist))

	def copy_files_to_index(self):
		logger.info('Copying files to index folder...')
		for file in self.filelist:
			logger.debug('Copying %s to %s...' % (file.src_fullname, config.INDEX_PATH))
			index_filename = os.path.basename(file.src_fullname)
			#index_filename = config.generate_random_string() + '.wav'
			shutil.copy2(file.src_fullname, config.INDEX_PATH + index_filename)
			file.index_filename = index_filename

	def get_audio_duration(self):
		logger.info('Receiving audio duration...')
		for file in self.filelist:
			#if file.extension == 'wav':
			#	wave_file = wave.open(config.INDEX_PATH + file.index_filename, 'r')
			#	time = wave_file.getnframes() / wave_file.getframerate()
			#	file.audio_duration = time
			cmd = "avconv -i %s%s 2>&1 | awk '/Duration/{print $2}' | sed 's/,//g'" % (config.INDEX_PATH, file.index_filename)
			output_cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()			
			file.audio_duration = parse_format_time(output_cmd[0])
			print file.audio_duration

	def generate_content(self):
		logger.info('Generating content templ...')
		content_fields = ['part_num', 'start_time', 'end_time', 'audio_file', 'text_file']
		for file in self.filelist:
			file.part_duration = self.part_duration
			file.parts = int(math.ceil(1.0 * file.audio_duration / self.part_duration))
			#fileData.content = [[format_time(part * PART_DURATION), format_time((part + 1) * PART_DURATION), None, None] for part in range(fileData.parts)]
			for part in range(file.parts):
				start_time = part * self.part_duration
				end_time = (part + 1) * self.part_duration
				part_info = dict(zip(content_fields, [part, start_time, end_time, None, None]))
				file.content.append(part_info)
				
	def process(self):
		logger.info('Preparing a list of files...')
		files_from_folders = self.check_dirs(self.folders)
		self.check_files(self.files + files_from_folders)
		self.remove_duplicates()
		self.copy_files_to_index()
		self.get_audio_duration()
		self.generate_content()
		return self.filelist

class FileData:
	def __init__(self, src_fullname):
		self.src_fullname = src_fullname
		self.filename, self.extension =  os.path.splitext(os.path.basename(self.src_fullname))
		self.extension = self.extension[1:-1]
		self.index_filename = ''
		self.hash = get_md5_hash(self.src_fullname)
		self.description = ''
		self.audio_duration = 0
		self.part_duration = 0
		self.parts = 0
		self.content = [] 
	
	def __str__(self):
		return '''Filename: %s
Index filename: %s
Extension: %s2
Source: %s
Duration: %i sec.
Part duration: %s
Parts: %i
Content: %s
Hash: %s
''' % (self.filename, self.index_filename, self.extension, self.src_fullname, self.audio_duration, self.part_duration, self.parts, self.content, self.hash)

def parse_format_time(str_time):
	logger.debug('Convertint time string: %s' % str_time)
	seconds = 0	
	times = str_time[:8].split(':')
	#print times
	#times = [t for t in times if t]
	#print times
	vals = [3600, 60, 1]
	seconds = sum([int(t) * v for t,v in zip(times, vals)])
	logger.debug('Result: %i' % seconds)
	return seconds

def get_md5_hash(filename):
	with open(filename) as file_to_hash:
		data = file_to_hash.read()
		return hashlib.md5(data).hexdigest()
