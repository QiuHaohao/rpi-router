import queue
import threading

from connections.libs.arrow_finder import ArrowFinder

def to_byte(i, length=1, byteorder="little"):
	return i.to_bytes(length,byteorder)

DEST_HEADER_TO_PC = to_byte(8)
SENDER_ADDR_FROM_RPI = to_byte(2)

CODE_CAPTURING_FINISHED = to_byte(21)
CODE_ARROW_DETECTED = to_byte(22)

class DetectionThread(threading.Thread):
	def __init__(self, got_msg, get_first_msg, on_finish_capturing, on_detected):
		threading.Thread.__init__(self)
		self.arrowFinder = ArrowFinder()
		self.got_msg = got_msg
		self.get_first_msg = get_first_msg
		self.on_finish_capturing = on_finish_capturing
		self.on_detected = on_detected

	def run(self):
		while True:
			if not self.got_msg():
				msg = self.get_first_msg()
				msg_payload = msg[1:]
				got_arrow = self.detect()
				if got_arrow:
					self.on_detected(msg_payload)

	def detect(self):
		return bool(
			self.arrowFinder.getArrows(
				after_capture = self.on_finish_capturing
			)
		)

class RpiConnection:
	def __init__(self):
		self.ready = False
		self.in_queue = queue.Queue()
		self.out_queue = queue.Queue()
		self.detech_thread = DetectionThread(
			got_msg=lambda: not self.in_queue.empty(),
			get_first_msg=self.in_queue.get,
			on_finish_capturing=self.put_capturing_finished,
			on_detected=self.put_arrow_detected
		)
		self.detech_thread.start()

	def send(self, msg):
		self.in_queue.put(msg)

	def recv(self):
		# block when there is nothing to be received
		while self.out_queue.empty():
			pass
		return self.out_queue.get()

	def put_capturing_finished(self):
		self.out_queue.put(
			DEST_HEADER_TO_PC
			+ SENDER_ADDR_FROM_RPI
			+ CODE_CAPTURING_FINISHED
		)

	def put_arrow_detected(self, msg_payload):
		self.out_queue.put(
			DEST_HEADER_TO_PC
			+ SENDER_ADDR_FROM_RPI
			+ CODE_ARROW_DETECTED
			+ msg_payload
		)

	def init_connection(self):
		# initialise detect_loop
		pass