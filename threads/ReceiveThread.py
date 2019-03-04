import threading

class ReceiveThread (threading.Thread):
	def __init__(self, threadID, name, receiver, lock, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		# All receivers should be initialised already 
		# before being passed in
		self.receiver = receiver
		self.lock = lock
		self.queue = queue

	def run(self):
		while True:
			# the recv method is blocking
			data = self.receiver.recv()
			if not data:
				print("{} received an empty message, skipping".format(self.receiver))
				continue
			self.lock.acquire()
			self.queue.put(data)
			self.lock.release()