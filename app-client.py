#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
from tkinter import *
import libclient
from tkinter import messagebox
from tkinter.ttk import *

global value


def kill():
    top.destroy()
    quit()

def send_bottle(message):
    global value
    value = message
    
        

    
top = Tk()
#top.attributes("-fullscreen",True)
top.title('Client')
defaultc = "status"
bottle = "waiting...0000"
count = 0


def main_func():
    global value
    global bottle
    global defaultc
    global count
    count = count + 1
    
    value = 'extendPadSwitchOn'
    sel = selectors.DefaultSelector()
    def create_request(action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value, encoding="utf-8"),
            )


    def start_connection(host, port, request):
        addr = (host, port)
        #print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(sel, sock, addr, request)
        sel.register(sock, events, data=message)

    #Host
    L1 = Label(top, text="Host")
    L1.grid(row=0, column=0)
    E1 = Entry(top)
    E1.insert(END, '130.18.64.135')
    E1.grid(row=0, column=1)

    #Port
    L2 = Label(top, text="Port")
    L2.grid(row=1, column=0)
    E2 = Entry(top)
    E2.insert(END, '65432')
    E2.grid(row=1, column=1)

    #Action
    E3 = "search"

    #Command
    #L4 = Label(top, text="Command")
    #L4.grid(row=2, column=0)
    #E4 = Entry(top)
    #E4.insert(END, defaultc)
    #E4.grid(row=2, column=1)    

    #Activity
    activity = bottle[:-5]

    if activity.isdigit():
        activity = 'good'
    
    L5 = Label(top, text=activity)
    L5.grid(row=4,column=1)

    status = bottle[-5:]
    status = "Door Status: " + status[0] + "\nRoof Status: " + status[1] + "\nBottom Pad Status: " + status[2] + "\nTop Pad Status: " + status[3] + "\nPower Status: " + status[4]

    L6 = Label(top, text=status)
    L6.grid(row=5,column=1)

    
    #Rows of Buttons
    var = IntVar()
    B1 = Button(top, text="Open Doors", command=lambda:[send_bottle("doorsSwitchOn"),var.set(1)])
    B1.grid(row=0,column=5)
    B2 = Button(top, text="Close Doors", command=lambda:[send_bottle("doorsSwitchOff"),var.set(1)])
    B2.grid(row=0,column=6)
    B3 = Button(top, text="Open Roof", command=lambda:[send_bottle("roofSwitchOn"),var.set(1)])
    B3.grid(row=0,column=7)
    B4 = Button(top, text="Close Roof", command=lambda:[send_bottle("roofSwitchOff"),var.set(1)])
    B4.grid(row=0,column=8)
    B5 = Button(top, text="Extend Pad", command=lambda:[send_bottle("extendPadSwitchOn"),var.set(1)])
    B5.grid(row=1,column=5)
    B6 = Button(top, text="Retract Pad", command=lambda:[send_bottle("extendPadSwitchOff"),var.set(1)])
    B6.grid(row=1,column=6)
    B7 = Button(top, text="Raise Pad", command=lambda:[send_bottle("raisePadSwitchOn"),var.set(1)])
    B7.grid(row=1,column=7)
    B8 = Button(top, text="Lower Pad", command=lambda:[send_bottle("raisePadSwitchOff"),var.set(1)])
    B8.grid(row=1,column=8)
    B9 = Button(top, text="Status", command=lambda:[send_bottle("status"),var.set(1)])
    B9.grid(row=2,column=8)
    B10 = Button(top, text="On/Off", command=lambda:[send_bottle("switchPower"),var.set(1)])
    B10.grid(row=2,column=7)

    var = IntVar()
    button = Button(top, text="Submit", command=lambda: var.set(1))
    

    exitb = Button(top, text="Exit", command=kill)
    exitb.grid(row=6, column=1)
    
    if count > 1:
        button.wait_variable(var)
    
    
    #assignments
    host = E1.get()

    E2 = E2.get()
    port = int(E2)

    action = E3

    #value = E4.get()
    
    defaultc = value
    
    request = create_request(action, value)
    start_connection(host, port, request)
    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    bottle = message.process_events(mask)
                except Exception:
                    #print(
                        #"main: error: exception for",
                        #f"{message.addr}:\n{traceback.format_exc()}",
                    #)
                    #messagebox.showinfo("Error","Traceback Error")
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        #print("caught keyboard interrupt, exiting")
        messagebox.showinfo("Error","Caught keyboard interrupt")
    finally:
        sel.close()

    L5.destroy()
        

main_func()

while True:
    main_func()

top.mainloop()
