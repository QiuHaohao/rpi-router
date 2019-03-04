import queue
import threading

from tcp import TCPServer
from BTServer import BTServer
from SerialArduino import SerialArduino
from ReceiveThread import ReceiveThread
from SendThread import SendThread

queue_lock = threading.Lock()
data_queue = queue.Queue()

bt = BTServer()
ser = SerialArduino()
pc = TCPServer()

bt.init_connection()
pc.init_connection()

print("All Connections Up! Waiting for message...")

# # using Stubs for now
# from Stubs import ReceiverStub, SenderStub

# # initialising the connections 
# receivers = [ReceiverStub(id=i) for i in range(3)]
# senders = [SenderStub(id=i) for i in range(3)]

connections = [ser,None,bt,pc]

receive_threads = [
	ReceiveThread(threadID=i, 
					name="Receive_Thread_{}".format(i), 
					receiver=connections[i], 
					lock=queue_lock, 
					queue=data_queue
				) 
	for i in range(3)
]

for t in receive_threads:
	t.start()

send_thread = SendThread(threadID=3, 
							name="Send_Thread", 
							scheme=connections, 
							lock=queue_lock, 
							queue=data_queue
						)

send_thread.start()