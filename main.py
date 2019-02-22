import queue
import threading

from ReceiveThread import ReceiveThread
from SendThread import SendThread

# using Stubs for now
from Stubs import ReceiverStub, SenderStub

queue_lock = threading.Lock()
data_queue = queue.Queue()

# initialising the connections 
receivers = [ReceiverStub(id=i) for i in range(3)]
senders = [SenderStub(id=i) for i in range(3)]

receive_threads = [
	ReceiveThread(threadID=i, 
					name="Receive_Thread_{}".format(i), 
					receiver=receivers[i], 
					lock=queue_lock, 
					queue=data_queue
				) 
	for i in range(3)
]

for t in receive_threads:
	t.start()

send_thread = SendThread(threadID=3, 
							name="Send_Thread", 
							scheme=senders, 
							lock=queue_lock, 
							queue=data_queue
						)

send_thread.start()