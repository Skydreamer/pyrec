# -*- coding: utf-8 -*-
import Queue, threading, subprocess, config

logger = config.create_logger(__name__)

class WorkerController:
	def __init__(self, filelist, work_func, max_workers=2):
		self.workers = []
		self.filelist = filelist
		self.work_func = work_func
		self.max_workers = max_workers

	def generate_queue(self):
		logger.info('Generating task queue...')
		self.queue = Queue.Queue()
		for file in self.filelist:
			self.queue.put(file)
		self.queue.completed = 0
		self.queue.size = self.queue.qsize()
		logger.info('Queue size: %i' % self.queue.size)
	
	def start_workers(self):
		logger.info('Strating worker threads...')
		for _ in range(self.max_workers):
			worker = Worker(self.queue, self.work_func)
			self.workers.append(worker)
			worker.setDaemon(True)
			worker.start()	

	def stop_workers(self):
		logger.info('Closing worker threads...')
		for worker in self.workers:
			worker.active = False
			del worker
		
	def run(self):
		logger.info('Start WorkController()')
		self.generate_queue()
		self.start_workers()
		self.queue.join()
		self.stop_workers()

class Worker(threading.Thread):
	def __init__(self, queue, work_func):
		threading.Thread.__init__(self)
		self.work_queue = queue
		self.work_func = work_func
		self.active = True
			
	def run(self): 
		while self.active:
			file_struct = self.work_queue.get()
			self.work_func(file_struct)
			self.work_queue.completed += 1
			logger.info('Complete %i of %i (...%s)' % (self.work_queue.completed, self.work_queue.size, file_struct.index_filename))
			self.work_queue.task_done()
			

