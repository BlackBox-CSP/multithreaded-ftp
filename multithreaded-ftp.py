#!/usr/bin/python
import time
import threading
import Queue
import ftplib

numberofthreads = 10

class workerthread(threading.Thread):
	def __init__(self, input, id):
		threading.Thread.__init__(self)
		self.input = input
		self.id = id
	
	def run(self):
		while True:
			sitestring = self.input.get()
			print sitestring
			print "Thread %d processting %s"%(self.id,sitestring)
			q = self.id
			w = sitestring
			ftp = ftplib.FTP(sitestring)
			ftp.login()
			ftp.retrlines("LIST", lambda q, w=self.id, e=sitestring : callback(q, w, e))
			ftp.close()
			print "thread %d done"%self.id
			self.input.task_done()
		

def callback(data, number, sitestring):
#	print "number = %d"%number
#	print "data = " + str(data)
	txt = file(sitestring, "a")	
	txt.write(data + "\n")
	txt.close()
#	print "thread %d wrote a line for %s"%(number, sitestring) 
		
ftpsites =  ("ftp.cisco.com", "ftp.blackbox.com", "ftp.dell.com", "ftp.hp.com", "ftp.microsoft.com", "ftp.supermicro.com", "ftp.slackware.com")

queue = Queue.Queue()

for x in range(numberofthreads):
	worker = workerthread(queue,x)
	worker.setDaemon(True)
	worker.start()

for x in ftpsites:
	queue.put(x)

queue.join()
print "All done!"
