import queue
import threading

from connections.libs.arrow_finder import ArrowFinder


def to_byte(i, length=1, byteorder="little"):
	return i.to_bytes(length,byteorder)

DEST_HEADER_TO_PC = to_byte(8)
SENDER_ADDR_FROM_RPI = to_byte(2)

CODE_CAPTURING_FINISHED = to_byte(21)
CODE_ARROW_DETECTED = to_byte(22)

class RpiConnection:
	class DetectThread(threading.Thread)：
		def __init__(self, in_queue, detect, on_detected):
			self.in_queue = in_queue
			self.detect = detect
			self.on_detected = on_detected
		def run(self):
			while True:
				if not self.in_queue.empty():
					msg = self.in_queue.get()
					msg_payload = msg[1:]
					got_arrow = self.detect()
					if got_arrow:
						self.on_detected(msg_payload)

	def __init__(self):
		self.arrowFinder = ArrowFinder()
		self.ready = False
		self.in_queue = queue.Queue()
		self.out_queue = queue.Queue()
		self.detech_thread = DetectThread(
			in_queue=self.in_queue,
			detect=self.detect,
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

	def detect(self):
		return bool(
			self.arrowFinder.getArrows(
				after_capture = self.put_capturing_finished
			)
		)

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