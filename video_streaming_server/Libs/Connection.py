import cv2
import socket
import signal

class Connection(object):

    def __init__(self, connections):
        print(connections)
        self.url = connections[1].decode("utf-8")
        print(self.url)
        self.socket = []
        self.socket.append(connections[0])
        self.connections = connections
        # signal.signal(signal.SIGINT, signal_handler)
        self.connect()
        pass



    def connect(self):
        #cv2 Video Capture key
        self.connection = cv2.VideoCapture(0) #number dictates camera
        return self.connection

    def addConnection(self, client):
        self.socket.append(client)

    def capture(self, opened_cameras):
        self.opened_cameras = opened_cameras
        while 1:
            try:
                ret, frame = self.connection.read()
                #frame encoding, here is where you could do the byte encoding
                data = cv2.imencode('.jpg', frame)[1].tostring()
                if len(self.socket):
                    for c in self.socket:
                        #sending data until there is none left to send
                        self.send(c,data)
                else:
                    self.connection.release()
                    del self.opened_cameras[self.connections[1]]
                    exit(0)

                    # self.connections[1].close()
            except KeyboardInterrupt:
                self.signal_handler()

    def send(self,c, data):
        try:
            c.send(data)
            c.send(b"END!") # send param to end loop in client
        except socket.error:
            self.socket.remove(c)
