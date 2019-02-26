import serial


class SerialArduino(object):
    def __init__(self,rate=9600):
                self.baudrate = rate
                self.port = '/dev/ttyACM0' #can be either 0 or 1 depending on which port connected to Arduino
   
    def send(self, msg):
		try :
			self.write(msg) #msg is in bytes form
		except Exception as e :
			print("\nError Message : %s",str(e))


    def recv(self):
		try:
            #return ser.read(1)
			return self.readline() #this requires Arduino side to send '\n' as EOL
		except Exception as e:
			print("\nError Message : %s",str(e))
