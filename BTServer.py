from bluetooth import *

class BTServer(object):

        def __init__(self):
                self.server_socket = None
                self.client_socket = None
                self.bt_is_connected = False


        def close_connection(self):

                if self.client_socket:
                        self.client_socket.close()
                        print ("Closing client socket")
                if self.server_socket:
                        self.server_socket.close()
                        print ("Closing server socket")
                self.server_socket = None
                self.client_socket = None
                self.bt_is_connected = False


        def bt_is_connect(self):
                return self.bt_is_connected


        def init_connection(self):
                btport = 3
                try:
                        self.server_socket = BluetoothSocket(RFCOMM)
                        self.server_socket.bind(("", btport))
                        self.server_socket.listen(1)    
                        self.port = self.server_socket.getsockname()[1]
                        uuid = "00001101-0000-1000-8000-00805F9B34FB"

                        advertise_service( self.server_socket, "MDPGrp05",
                                           service_id = uuid,
                                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                                           profiles = [ SERIAL_PORT_PROFILE ],
                               )
                        print ("Waiting for BT connection on RFCOMM channel %d" % self.port)
                        # Accept requests
                        self.client_socket, client_address = self.server_socket.accept()
                        print ("Accepted connection from ", client_address)
                        self.bt_is_connected = True
                except KeyboardInterrupt:
                        sys.exit()
                        print("Bluetooth Service has been closed")
                except Exception as e:
                        print ("\nError Message: %s" %str(e))


        def send(self, message): #Send msg to device connected w bluetooth
                try:
                        self.client_socket.send(message) #message in bytes
                except BluetoothError:
                        print ("\nBluetooth Write Error. Connection was lost")
                        try :
                            self.close_bt_socket()
                            self.init_connection()       # Reestablish connection
                            print ("\nClosed and restarted Bluetooth connection successfully")
                        except Exception as e:
                            print("\Failed to restart Bluetooth connection and error Message : %s"%str(e))

                        
        def recv(self): #Receive msg from device connected w bluetooth
                try:
                        return self.client_socket.recv(1024) #receive in bytes
                except BluetoothError:
                        print ("\nBluetooth Read Error. Connection lost")
                        try :
                            self.close_bt_socket()
                            self.init_connection()       # Reestablish connection
                            print ("\nClosed and restarted Bluetooth connection successfully")
                        except Exception as e:
                            print("\Failed to restart Bluetooth connection and error Message : %s"%str(e))




if __name__ == "__main__":
    test = BTServer()
    test.init_connection()

    test.send("hi".encode('utf-8'))
    message = test.recv().decode('utf-8')
    print(message)
