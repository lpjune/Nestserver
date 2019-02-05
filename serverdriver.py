import sys
import socket
import traceback
from tkinter import *
from serverlib import *
import serial



top = Tk()
top.title('Server')

def kill():
    top.destroy()
    quit()

connect_mech()

# Get IP and Port from TextEdit
# or use default values
L1 = Label(top, text="Server")
L1.grid(row=0, column=0)
E1 = Entry(top, bd = 5)
E1.insert(END, '192.168.0.7')
E1.grid(row=0, column=1)

L2 = Label(top, text="Port")
L2.grid(row=1, column=0)
E2 = Entry(top, bd = 5)
E2.insert(END, '65432')
E2.grid(row=1, column=1)

# submit and exit buttons
var = IntVar()
button = Button(top, text="Submit", command=lambda: var.set(1))
button.grid(row=4, column=1)

exitb = Button(top, text="Exit", command=kill)
exitb.grid(row=5, column=2)

# wait for button response
button.wait_variable(var)

# start socket and bind to host and port from text input
host, port = E1.get(), int(E2.get())
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))

# listen to up to 5 devices
lsock.listen(5)
print("listening on", (host, port))
# close GUI window
top.destroy()

# accept connection
conn, address = lsock.accept()
lsock.setblocking(False)
print("accepted connection from", address)
sender(conn, "connected")

# listen for messages
running = True
while running:
    # receive and decode message
    received_message = receiver(conn)
    # close connection
    if received_message == "Closed Connection":
        break
    # match received message to response
    # check for errors
    # send command to machine
    # return response
    created_answer = create_response(received_message)
    # send response back to device
    sender(conn, created_answer)


top.mainloop()
