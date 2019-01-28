import sys
import selectors
import json
import io
import struct
import time
import serial
from mechanical import *

# receive messages
# decode and strip whitespace/newlines
def receiver(socket):
    data = conn.recv(1024).decode().strip()
    print(data)
    return data

# send encoded message
def sender(socket, message):
    socket.send(message.encode())
    return
