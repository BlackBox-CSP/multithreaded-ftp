#!/usr/bin/python

import threading
import Queue
import time

class WorkerThread(threading.Thread) :
	def __init__(self, queue, id):
		threading.Thread.__init__(self)
		self.queue = queue
		self.id = str(id)
	
	def run(self):
		print "In worker thread"
		while True:
			counter = str(self.queue.get())
			print "worker " + self.id + " " + counter
			self.queue.task_done()

myqueue = Queue.Queue()


for x in range(10):
	worker = WorkerThread(myqueue, x)
	worker.setDaemon(True)
	worker.start()

for x in range(101):
	myqueue.put(x)

myqueue.join()

print "done!"
