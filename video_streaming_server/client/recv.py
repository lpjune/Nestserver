### Written by Luke Redwine at Impress Labs
### This file recieves the encoded string, converts it into an int
### and reencodes it for OPENCV to see

#py recv.py ipv4_address local
# cd nestserver/video_streaming_server/client
#py recv.py 192.168.0.7 local

#!/usr/bin/python
import socket
import cv2
import numpy
import random
import sys

#system arguements
host = sys.argv[1] # e.g. localhost, 192.168.1.123
cam_url = sys.argv[2] # rtsp://user:pass@url/live.sdp , http://url/video.mjpg ...
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#connection made
client_socket.connect((host, 5005))

name = "Video"

#socket encoding for video address
client_socket.send(str.encode(cam_url))
print(cam_url)

def rcv():
    data = b''
    while 1:
        
        try:
            r = client_socket.recv(90456)
            if len(r) == 0:
                exit(0)
            a = r.find(b'END!')
            if a != -1:
                data += r[:a]
                break
            data += r
        except Exception as e:
            print(e)
            continue
    nparr = numpy.fromstring(data, numpy.uint8)
    #opecv frame capture
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if type(frame) is type(None):
        pass
    else:
        try:
            #display frame to user
            cv2.imshow(name,frame)
            
            #kill key
            if cv2.waitKey(10) == ord('q'):
                client_socket.close()
                sys.exit()
        except:
            client_socket.close()
            exit(0)

while 1:
    rcv()
