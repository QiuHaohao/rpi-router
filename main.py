import queue
import threading
import logging
import time

from connections.tcp import TCPServer
from connections.BTServer import BTServer
from connections.SerialArduino import SerialArduino
from connections.RpiConnection import RpiConnection

from threads.ReceiveThread import ReceiveThread
from threads.SendThread import SendThread

FORMAT = 'Time: %(time_from_start)dms - %(message)s'
logging.basicConfig(format=FORMAT)

def log_with_time(msg, lvl=logging.WARNING):
	time_from_start = time.time() - starting_time
	l.log(lvl, msg, extra={'time_from_start': time_from_start*1000})

l = logging.getLogger(__name__)

data_queue = queue.Queue()

connections = {
	0: SerialArduino(),
	1: BTServer(),
	2: TCPServer(),
	3: RpiConnection()
}

for c in connections:
	connections[c].init_connection()

starting_time = time.time()

log_with_time("All Connections Up! Waiting for message...")

receive_threads = [
	ReceiveThread(threadID=i, 
					name="Receive_Thread_{}".format(i), 
					receiver=connections[i], 
					queue=data_queue,
					log=log_with_time
				) 
	for i in connections
]

for t in receive_threads:
	t.start()

send_thread = SendThread(threadID=len(connections), 
							name="Send_Thread", 
							scheme=connections, 
							queue=data_queue,
							log=log_with_time
						)

send_thread.start()