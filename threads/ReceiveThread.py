import threading

class ReceiveThread (threading.Thread):
	def __init__(self, threadID, name, receiver, queue, log):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		# All receivers should be initialised already 
		# before being passed in
		self.receiver = receiver
		self.queue = queue
		self.log = log

	def run(self):
		while True:
			# the recv method is blocking
			data = self.receiver.recv()
			if not data:
				self.log("{} received an empty message, skipping".format(self.receiver))
			else:
				self.log("Received data: {} from {}".format(data, self.receiver))
				self.queue.put(data)
