import serial

class SerialArduino(object):
    def __init__(self,rate=115200):
        self.baud_rate = rate
        self.port = '/dev/ttyACM1' #can be either 0 or 1 depending on which port connected to Arduino
        self.ser = None

    def send(self, msg):
        try :
            self.ser.write(msg) #msg is in bytes form
        except Exception as e :
            print("\nError Message : %s",str(e))

    def recv(self):
        try:
            return self.ser.readline() #this requires Arduino side to send '\n' as EOL
        except Exception as e:
            print("\nError Message : %s",str(e))

    def init_connection(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate)
            print("Serial connected.")
        except Exception as e:
            print("Serial not connected: {}".format(e))