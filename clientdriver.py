import sys
import socket
from tkinter import *
from serverlib import *
from clientlib import *



top = Tk()
top.title('Client')

def kill():
    top.destroy()
    quit()

# starts socket connection with IP and Port from GUI
# returns socket
def connect():
    global sock
    host = E1.get()
    port = int(E2.get())
    addr = (host, port)
    print("starting connection to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)




L6 = Label(top, text=status)
L6.grid(row=5,column=1)
# IP TextEdit
L1 = Label(top, text="Server")
L1.grid(row=0, column=0)
E1 = Entry(top, bd = 5)
E1.insert(END, '192.168.0.7')
E1.grid(row=0, column=1)
# Port TextEdit
L2 = Label(top, text="Port")
L2.grid(row=1, column=0)
E2 = Entry(top, bd = 5)
E2.insert(END, '65432')
E2.grid(row=1, column=1)

# Submit Button
# connects to server
var = IntVar()
button = Button(top, text="Submit", command=lambda:[connect(), var.set(1)])
button.grid(row=2, column=1)

# Exit Button
exitb = Button(top, text="Exit", command=lambda:[exitb()])
exitb.grid(row=3, column=1)


# Rows of Buttons
# Send messages to server on click
# Open Door Button
B1 = Button(top, text="Open Doors", command=lambda:[sender(sock, "doorsSwitchOn"),var.set(1)])
B1.grid(row=0,column=5)

# Close Door Button
B2 = Button(top, text="Close Doors", command=lambda:[sender(sock, "doorsSwitchOff"),var.set(1)])
B2.grid(row=0,column=6)

# Open Roof Button
B3 = Button(top, text="Open Roof", command=lambda:[sender(sock, "roofSwitchOn"),var.set(1)])
B3.grid(row=0,column=7)

# Close Roof Button
B4 = Button(top, text="Close Roof", command=lambda:[sender(sock, "roofSwitchOff"),var.set(1)])
B4.grid(row=0,column=8)

# Extend Pad Button
B5 = Button(top, text="Extend Pad", command=lambda:[sender(sock, "extendPadSwitchOn"),var.set(1)])
B5.grid(row=1,column=5)

# Retract Pad Button
B6 = Button(top, text="Retract Pad", command=lambda:[sender(sock, "extendPadSwitchOff"),var.set(1)])
B6.grid(row=1,column=6)

# Raise Pad Button
B7 = Button(top, text="Raise Pad", command=lambda:[sender(sock, "raisePadSwitchOn"),var.set(1)])
B7.grid(row=1,column=7)

# Lower Pad Button
B8 = Button(top, text="Lower Pad", command=lambda:[sender(sock, "raisePadSwitchOff"),var.set(1)])
B8.grid(row=1,column=8)

# Update Status Button
B9 = Button(top, text="Status", command=lambda:[sender(sock, "status"),var.set(1)])
B9.grid(row=2,column=8)

# Power Button
B10 = Button(top, text="On/Off", command=lambda:[sender(sock, "switchPower"),var.set(1)])
B10.grid(row=2,column=7)
button.wait_variable()

running = True
while running:
    receiver(sock)


# continuously connect to server
# listen for response from server
