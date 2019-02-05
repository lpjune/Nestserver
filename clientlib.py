import sys
import selectors
import json
import io
import struct
import time
import serial
from mechanicalND import *

# receive messages
# decode and strip whitespace/newlines
def receiver(socket):
    data = str(socket.recv(4096).decode())
    print(data)
    return data

# send encoded message
def sender(socket, message):
    socket.send(message.encode())
    print(message)
    return
