class SenderStub:
	def __init__(self, id=0):
		self.id = id

	def send(self, msg):
		print("Sender #{} sends: {}".format(self.id, msg))