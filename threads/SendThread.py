import threading

def parse_msg(msg):
	dest_header = msg[0]
	payload = msg[1:]
	dest = []
	for i in range(8):
		if dest_header & 1 << i != 0:
			dest.append(i)
	return dest, payload

class SendThread (threading.Thread):
	def __init__(self, threadID, name, scheme, queue, log):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		# scheme is an array containing connections
		# All connections should be initialised already 
		# before being passed in
		self.scheme = scheme
		self.queue = queue
		self.log = log

	def run(self):
		while True:
			data = self.queue.get()
			self.send(data)

	def send(self, data):
		dest, payload = parse_msg(data)
		self.log("Sending to {}, Data: {}".format(dest, payload))

		for d in dest:
			self.scheme[d].send(payload)
