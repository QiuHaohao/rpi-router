from random import uniform
import time

def get_dest_header(dest):
	bits = [1 << i for i in dest]
	dest_header = sum(bits).to_bytes(length=1,byteorder="little")
	return dest_header

class ReceiverStub:
	def __init__(self, id=0, min_interval=0.1, max_interval=3, n_connection=3):
		self.min_interval = min_interval
		self.max_interval = max_interval
		self.n_connection = n_connection
		self.id = id

	def recv(self):
		interval = uniform(self.min_interval, self.max_interval)
		time.sleep(interval)
		dest = [i for i in range(self.n_connection) if uniform(0,1)<0.5]
		dest_header = get_dest_header(dest)
		payload = "test_message_{}".format(interval).encode("UTF-8")
		print("Receiver #{} receives: {}, sending to {}".format(self.id, payload, dest))
		return dest_header + payload